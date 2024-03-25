import base64
import re
import rbloom
import numbers
import typing
import json

from . import base, backend, exceptions


D = typing.TypeVar('D', bound=base.BaseEEGTemplateData)


class EEGTemplateDataSerializer(typing.Generic[D]):
    """
    Serializer for EEG template data. Capable of storing the data in a string format, and then recovering the stored
    data back into a template instance.
    """
    SERIALIZATION_ENCODING = 'utf-8'
    SERIALIZE_FILTER_KEY = 'filters'
    SERIALIZE_SEGMENT_RATIO_KEY = 'segment_ratio'
    SERIALIZED_FILTER_PATTERN = r'^(?P<filter_bytes>[^:]+):(?P<hash_backend>[a-z]+)$'

    def __init__(self, constructor: typing.Type[D]):
        self._filter_data_regex = re.compile(self.SERIALIZED_FILTER_PATTERN)
        self._constructor = constructor

    def serialize(self, data: D) -> str:
        """
        Serializes the given template data into a string.

        :param data: The data to serialize.
        :returns: A serialized template data string.
        """
        data_map = {
            self.SERIALIZE_FILTER_KEY: self._serialize_filters(data.bloom_filters),
            self.SERIALIZE_SEGMENT_RATIO_KEY: data.segment_ratio
        }
        return json.dumps(data_map)

    def deserialize(self, data: str,  backend_kwargs: dict = None) -> D:
        """
        Recovers the given serialized template data string into a template data instance.

        :param data: The serialized template data string.
        :param backend_kwargs: Additional keyword arguments to pass down to the hashing backend(s) that are initialized.
        :returns: The template data instance.
        """
        if backend_kwargs is None:
            backend_kwargs = {}
        parsed_data = json.loads(data)
        self.validate_serialized_data(parsed_data)
        bloom_filters = self._deserialize_filters(parsed_data[self.SERIALIZE_FILTER_KEY], **backend_kwargs)
        segment_ratio = float(parsed_data[self.SERIALIZE_SEGMENT_RATIO_KEY])
        return self._constructor(bloom_filters=bloom_filters, segment_ratio=segment_ratio)

    def validate_serialized_data(self, serialization_data: str):
        """
        Checks that the given serialized data matches the expected format for serialized EEG template data.

        :param serialization_data: The data to check.
        :raises InvalidSerializationFormat: if the data does not match the expected format.
        """
        if not isinstance(serialization_data, dict):
            raise exceptions.InvalidSerializationFormat(
                f'Expected serialized data to be an object, got {type(serialization_data)}.'
            )
        if (self.SERIALIZE_FILTER_KEY not in serialization_data or
                self.SERIALIZE_SEGMENT_RATIO_KEY not in serialization_data):
            raise exceptions.InvalidSerializationFormat(
                f'Expected serialized data to contain the two top level keys: '
                f'{self.SERIALIZE_FILTER_KEY} and {self.SERIALIZE_SEGMENT_RATIO_KEY}.'
            )
        if not isinstance(serialization_data[self.SERIALIZE_FILTER_KEY], list):
            raise exceptions.InvalidSerializationFormat(
                f'Expected filter data to be a list, got {type(serialization_data[self.SERIALIZE_FILTER_KEY])}.'
            )
        if not isinstance(serialization_data[self.SERIALIZE_SEGMENT_RATIO_KEY], numbers.Number):
            raise exceptions.InvalidSerializationFormat(
                f'Expected segment ratio to a number, got {type(serialization_data[self.SERIALIZE_SEGMENT_RATIO_KEY])}.'
            )

    def _serialize_filters(self, bloom_filters: typing.List[rbloom.Bloom]) -> typing.List[str]:
        """
        Helper method which serializes the given list of Bloom Filters into a series of data strings.

        :param bloom_filters: The filters to serialize.
        :returns: A series of data strings, representing the serialized Bloom Filters.
        """
        bloom_filter_data = []
        for bloom_filter in bloom_filters:
            bloom_filter_data.append(self._serialize_bloom_data(bloom_filter))
        return bloom_filter_data

    def _serialize_bloom_data(self, bloom_filter: rbloom.Bloom) -> str:
        """
        Serializes the given Bloom Filter into a data string, which is: the base64 encoded bytes of the filter and
        the name of the hashing backend used for the filter. This allows for the Bloom Filter to be instantiated
        with the same data as it originally had, including the hashing implementation used.

        :param bloom_filter: The Bloom Filter to be serialized.
        :returns: The data string corresponding to the Bloom Filter.
        """
        filter_bytes = bloom_filter.save_bytes()
        bytes_b64 = base64.b64encode(filter_bytes)
        serialized_filter = bytes_b64.decode(self.SERIALIZATION_ENCODING)
        hash_backend = type(bloom_filter.hash_func)
        if not issubclass(hash_backend, backend.BaseBloomFilterHashBackend):
            raise ValueError(
                f'Bloom filter hash backends not derived from {backend.BaseBloomFilterHashBackend.__name__} '
                f'are not supported for serialization.'
            )
        backend_implementation_key = backend.BaseBloomFilterHashBackend.get_implementation_key(hash_backend)
        return f'{serialized_filter}:{backend_implementation_key}'

    def _deserialize_filters(self, bloom_filter_data: typing.List[str], **kwargs) -> typing.List[rbloom.Bloom]:
        """
        Re-creates a list of Bloom Filters from the given list of Bloom Filter data strings.

        :param bloom_filter_data: List of data strings representing the Bloom Filters to be instantiated.
        :param kwargs: Additional keyword arguments to be passed to the Bloom Filter deserialization method.
        :returns: The list of Bloom Filters.
        """
        bloom_filters = []
        for serialized_filter in bloom_filter_data:
            bloom_filters.append(self._deserialize_bloom_data(serialized_filter, **kwargs))
        return bloom_filters

    def _deserialize_bloom_data(self, serialized_data: str, **kwargs) -> rbloom.Bloom:
        """
        Re-creates a Bloom Filter using the given data string.

        :param serialized_data: The data string to use to re-create the Bloom Filter.
        :param kwargs: Additional keyword arguments to pass to the hash backend used in the Bloom Filter.
        :returns: The re-created Bloom Filter.
        """
        filter_data = self._filter_data_regex.match(str(serialized_data))
        if not filter_data:
            raise ValueError('Invalid filter data format.')
        bloom_bytes = base64.b64decode(filter_data.group('filter_bytes'))
        backend_key = filter_data.group('hash_backend')
        backend_cls = backend.BaseBloomFilterHashBackend.get_implementation(backend_key)
        filter_backend = backend_cls(**kwargs)
        return rbloom.Bloom.load_bytes(bloom_bytes, filter_backend)
