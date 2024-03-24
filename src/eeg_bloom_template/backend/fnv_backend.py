from .base import BaseBloomFilterHashBackend
from ..utils import convert_unsigned_128_to_signed


class FNVBloomFilterBackend(BaseBloomFilterHashBackend):
    """
    A Bloom Filter hash backend which uses the 128 bit FNV-1a hash algorithm in order to compute hash codes.
    There is only one slight modification to the algorithm,
    that being the result is converted to a signed 128-bit number.
    """
    FNV_PRIME_128 = 0x0000000001000000000000000000013B
    FNV_OFFSET_128 = 0x6c62272e07bb014262b821756295c58d

    def run_hash_function(self, data: bytes) -> int:
        hash_value = self.FNV_OFFSET_128

        for byte_value in data:
            hash_value = hash_value ^ byte_value
            hash_value = hash_value * self.FNV_PRIME_128

        # Use 128-bit signed value, as this is the acceptable range for the Bloom filter implementation.
        return convert_unsigned_128_to_signed(hash_value)
