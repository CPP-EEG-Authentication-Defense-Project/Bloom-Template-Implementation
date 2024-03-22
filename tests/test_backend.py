import unittest

from eeg_bloom_template.backend.fnv_backend import FNVBloomFilterBackend
from eeg_bloom_template.backend.mmh3_backend import MMH3BloomFilterBackend


class BackendTestCase(unittest.TestCase):
    def test_fnv_backend(self):
        test_value = 42
        expected = 140121297216442123210317922797979092383
        backend = FNVBloomFilterBackend()

        hashed_value = backend.hash_data(test_value)

        self.assertEqual(hashed_value, expected)

    def test_mmh3_backend(self):
        test_value = 42
        expected = 125910445295375924307876186304187122577
        backend = MMH3BloomFilterBackend()

        hashed_value = backend.hash_data(test_value)

        self.assertEqual(hashed_value, expected)
