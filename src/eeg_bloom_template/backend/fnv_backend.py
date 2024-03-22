from .base import BaseBloomFilterHashBackend


class FNVBloomFilterBackend(BaseBloomFilterHashBackend):
    """
    A Bloom Filter hash backend which uses the 128 bit FNV-1a hash algorithm in order to compute hash codes.
    There is only one slight modification to the algorithm, in that the result is converted to a signed 128 bit number.
    """
    FNV_PRIME_128 = 0x6c62272e07bb014262b821756295c58d

    def run_hash(self, data: bytes) -> int:
        hash_value = self.FNV_PRIME_128

        for byte_value in data:
            hash_value = hash_value ^ byte_value
            hash_value = hash_value * self.FNV_PRIME_128

        # Converting hash value to signed 128-bit number compatible with bloom filter implementation.
        return hash_value - 2**127
