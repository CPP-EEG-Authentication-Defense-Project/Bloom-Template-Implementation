import mmh3

from .base import BaseBloomFilterHashBackend


class MMH3BloomFilterBackend(BaseBloomFilterHashBackend):
    """
    A Bloom Filter hash backend which uses the MurmurHash3 hash algorithm to compute hash codes. Optionally, can
    be given a seed value for the MurmurHash3 hash function.
    """
    def __init__(self, seed: int = 0):
        super().__init__()
        self._seed = seed

    def run_hash_function(self, data: bytes) -> int:
        hasher = mmh3.mmh3_x64_128(seed=self._seed)
        hasher.update(data)
        return hasher.sintdigest()

    @property
    def hash_function_name(self) -> str:
        return 'mmh3'
