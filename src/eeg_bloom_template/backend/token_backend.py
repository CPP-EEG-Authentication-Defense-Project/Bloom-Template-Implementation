import typing
import numpy as np

from .base import BaseBloomFilterHashBackend
from ..utils import number_values, orthonormalization


class TokenBackend(BaseBloomFilterHashBackend):
    """
    Bloom filter backend which uses a token to orthonormalize data and compute pseudo-hash values.
    """
    def __init__(self, token: typing.Union[int, str, float]):
        self._token = token
        super().__init__()

    def run_hash_function(self, data: bytes) -> int:
        data_vector = np.array([b for b in data])
        normalized_vector = orthonormalization.normalize_cached(self._token, data_vector)
        data_sum = np.sum(normalized_vector)
        clamped_sum = number_values.clamp_value(data_sum, -2**127, 2**127)
        # Ensure an int is returned
        return round(clamped_sum)
