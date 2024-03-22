import unittest

from eeg_bloom_template.utils import iter_ratio_slices


class UtilsTestCase(unittest.TestCase):
    def test_iter_ratio_slices(self):
        ratio = 0.25
        collection = list(i for i in range(10))
        expected = [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
        actual = [collection_slice for collection_slice in iter_ratio_slices(collection, ratio)]

        self.assertListEqual(expected, actual)
