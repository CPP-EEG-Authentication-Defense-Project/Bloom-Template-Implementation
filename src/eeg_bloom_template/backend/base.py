import abc
import struct
import typing


class BaseBloomFilterHashBackend(abc.ABC):
    """
    Abstract base class defining the interface for a hash backend used for bloom filters.
    """
    @abc.abstractmethod
    def run_hash(self, data: bytes) -> int:
        """
        Executes a hash function on the given data, returning an integer hash code.

        :param data: The data to hash.
        :returns: The hashed data.
        """
        pass

    def hash_data(self, data: typing.Union[int, float]) -> int:
        """
        Hashes input data.

        :param data: The data to hash.
        :returns: The hash code produced.
        """
        if isinstance(data, int):
            # Avoid integers, as they are hashed as themselves
            data = data + 0.1
        data_bytes = struct.pack('f', data)
        return self.run_hash(data_bytes)
