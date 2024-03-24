import typing
import numpy as np

from . import base, engine, comparison, backend, serialization


class EEGTemplate(base.BaseEEGTemplateData):
    """
    EEG template implementation, based on bloom filters.
    """
    @classmethod
    def make_template(cls,
                      feature_data: typing.List[np.ndarray],
                      hash_backend: backend.BaseBloomFilterHashBackend,
                      segment_ratio: float,
                      false_positive_ratio: float) -> 'EEGTemplate':
        """
        Generates an EEG template instance using given feature data, a hashing backend, segment ratio, and false
        positive rate.

        :param feature_data: The processed feature data to use to create the template.
        :param hash_backend: The hash backend to use for the Bloom Filters in the template.
        :param segment_ratio: The segment ratio to use in the template.
        :param false_positive_ratio: The false positive rate to use in the Bloom Filters.
        :returns: The template instance.
        """
        if not 0 < false_positive_ratio < 1:
            raise ValueError(f'False positive ratio must be between 0 and 1 (got {false_positive_ratio}).')
        data_engine = engine.EEGBloomFilterTemplateEngine(hash_backend, segment_ratio, false_positive_ratio)
        template_data = data_engine.create_template_data(feature_data)
        return cls(bloom_filters=template_data, segment_ratio=segment_ratio)

    def compare(self, data: typing.List[np.ndarray]) -> comparison.ComparisonResult:
        """
        Compares the current template against a given matrix of EEG feature data. This is essentially a wrapper
        around the EEG template data checker class implementation.

        :param data: The EEG feature data to compare the template against.
        :returns: The comparison result.
        """
        checker = comparison.EEGTemplateDataChecker(self)
        return checker.check(data)

    def serialize(self) -> str:
        """
        Wrapper around the instantiation and usage of a serializer class, which returns the current EEG template
        in a serialized string format.

        :returns: The EEG template, as a string.
        """
        serializer = serialization.EEGTemplateDataSerializer(self.__class__)
        return serializer.serialize(self)

    @classmethod
    def deserialize(cls, data: str) -> 'EEGTemplate':
        """
        Wrapper around the instantiation and usage of a serializer class, which returns an EEG template instance
        from a serialized data string.

        :param data: The data string containing serialized EEG template data.
        :returns: The EEG template instance, instantiated from the data string.
        :raises InvalidSerializationFormat: If the data string is in the wrong format for deserialization.
        """
        serializer = serialization.EEGTemplateDataSerializer(cls)
        return serializer.deserialize(data)
