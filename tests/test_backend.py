import unittest

from eeg_bloom_template.backend.fnv_backend import FNVBloomFilterBackend
from eeg_bloom_template.backend.mmh3_backend import MMH3BloomFilterBackend


class BackendTestCase(unittest.TestCase):
    def test_fnv_backend(self):
        test_value = 42
        expected = int(
            '0x37b71b74346361a5f15aeb81947009623463d58a26809f44747eb805107'
            '3cc7b4cccddd9f8385609f056f97df4be16a237b23f393b81fc6dceb63999'
            '7b52bcd91c5914713b4e6caeb2d161f74cf993f',
            16
        )
        backend = FNVBloomFilterBackend()

        hashed_value = backend.hash_data(test_value)

        self.assertEqual(hashed_value, expected)

    def test_mmh3_backend(self):
        test_value = 42
        expected = 125910445295375924307876186304187122577
        backend = MMH3BloomFilterBackend()

        hashed_value = backend.hash_data(test_value)

        self.assertEqual(hashed_value, expected)
