import mmh3

from .base import BaseBloomFilterHashBackend


class MMH3BloomFilterBackend(BaseBloomFilterHashBackend):
    """
    A Bloom Filter hash backend which uses the MurmurHash3 hash algorithm to compute hash codes. Optionally, can
    be given a seed value for the MurmurHash3 hash function.
    """
    def __init__(self, seed: int = 0):
        super().__init__()
        self._hasher = mmh3.mmh3_x64_128(seed=seed)

    def run_hash(self, data: str) -> int:
        return self._hasher.sintdigest()
