import unittest
import string
import random
import numpy as np

from eeg_bloom_template.utils.iteration import iter_ratio_slices
from eeg_bloom_template.utils.number_values import convert_unsigned_128_to_signed
from eeg_bloom_template.utils.orthonormalization import TokenDataGenerator, TokenMatrixNormalization


class DummyTokenDataGenerator(TokenDataGenerator):
    def generate_matrix(self, dimension: int) -> np.ndarray:
        return np.array([[2] * dimension] * dimension)


class UtilsTestCase(unittest.TestCase):
    def test_iter_ratio_slices(self):
        ratio = 0.25
        collection = list(i for i in range(10))
        expected = [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
        actual = [collection_slice for collection_slice in iter_ratio_slices(collection, ratio)]

        self.assertListEqual(expected, actual)

    def test_convert_max_unsigned_128_integer(self):
        max_unsigned_128 = 1 << 127
        signed_overflow = -(2**127)
        actual = convert_unsigned_128_to_signed(max_unsigned_128)

        self.assertEqual(signed_overflow, actual)

    def test_convert_value_within_signed_128_range(self):
        max_signed_128 = (2**127) - 1
        actual = convert_unsigned_128_to_signed(max_signed_128)

        self.assertEqual(max_signed_128, actual)

    def test_orthonormalization_method(self):
        test_data = np.ones((2,))
        generator = DummyTokenDataGenerator('fake')
        normalizer = TokenMatrixNormalization(generator)
        expected_output = np.array([4, 4])

        normalized_data = normalizer.normalize(test_data)

        self.assertEqual(len(normalized_data), len(expected_output))
        for actual, expected in zip(normalized_data, expected_output):
            self.assertEqual(actual, expected)

    def test_invalid_orthonormalization_mixing(self):
        test_data = np.ones((10,))
        matrix_data = np.ones((5, 5))

        def run_mixing():
            return TokenMatrixNormalization.mix_token_matrix(test_data, matrix_data)

        self.assertRaises(ValueError, run_mixing)

    def test_random_token_generation(self):
        test_size = 256
        token = TokenDataGenerator.generate_random_token(size=test_size)

        self.assertIsInstance(token, str)
        # The hex token generation doubles the size used, so we expect the token to be double the given size.
        self.assertEqual(len(token), test_size * 2)

    def test_random_matrix_generation(self):
        token = ''.join(random.choice(string.ascii_lowercase) for _ in range(32))
        generator = TokenDataGenerator(token)

        matrix = generator.generate_matrix(4)

        self.assertEqual(matrix.shape, (4, 4))
