import unittest

from eeg_bloom_template.utils.iteration import iter_ratio_slices
from eeg_bloom_template.utils.conversion import convert_unsigned_128_to_signed


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
