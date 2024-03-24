import abc
import struct
import typing

from ..exceptions import InvalidImplementation


class BaseBloomFilterHashBackend(abc.ABC):
    """
    Abstract base class defining the interface for a hash backend used for bloom filters.
    """
    _implementations: typing.Dict[str, typing.Type['BaseBloomFilterHashBackend']] = {}

    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def run_hash_function(self, data: bytes) -> int:
        """
        Executes a hash function on the given data, returning an integer hash code.

        :param data: The data to hash.
        :returns: The hashed data.
        """
        pass

    @property
    @abc.abstractmethod
    def hash_function_name(self) -> str:
        """
        Retrieves the name to use for the hash function backend. This is used for equality checks.

        :returns: The hash function name.
        """
        pass

    def hash_data(self, data: typing.Union[int, float]) -> int:
        """
        Hashes input data.

        :param data: The data to hash.
        :returns: The hash code produced.
        """
        if isinstance(data, int):
            # Enforce only float data
            data = data + 0.1
        data_bytes = struct.pack('f', data)
        return self.run_hash_function(data_bytes)

    @classmethod
    def get_implementation(cls, implementation_key: str) -> typing.Type['BaseBloomFilterHashBackend']:
        """
        Retrieves a hash backend implementation from the given implementation key.

        :param implementation_key: The key to use to retrieve the implementation.
        :returns: The implementation.
        """
        implementation = cls._implementations.get(implementation_key.lower(), None)
        if implementation is None:
            raise InvalidImplementation(f'No registered implementation for "{implementation_key}"')
        return implementation

    @classmethod
    def __init_subclass__(cls, **kwargs):
        # Register new subclasses
        super().__init_subclass__(**kwargs)
        BaseBloomFilterHashBackend._implementations[cls.get_implementation_key(cls)] = cls

    @classmethod
    def get_implementation_key(cls, implementation: typing.Type['BaseBloomFilterHashBackend']) -> str:
        """
        Retrieves the key to use for retrieving the given implementation type at runtime from the subclass registry.

        :param implementation: The implementation (i.e., the type) to retrieve the implementation key from.
        :returns: The implementation key.
        """
        return implementation.__name__.lower()

    def __call__(self, data: typing.Union[int, float]) -> int:
        # In order to be compatible with the bloom filter implementation, the backend must be callable.
        return self.hash_data(data)

    def __eq__(self, other: 'BaseBloomFilterHashBackend') -> bool:
        return self.hash_function_name == other.hash_function_name
