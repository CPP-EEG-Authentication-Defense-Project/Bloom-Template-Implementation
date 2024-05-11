import unittest
import unittest.mock
import struct

from eeg_bloom_template.backend.fnv_backend import FNVBloomFilterBackend
from eeg_bloom_template.backend.mmh3_backend import MMH3BloomFilterBackend
from eeg_bloom_template.backend.token_backend import TokenBackend


class BackendTestCase(unittest.TestCase):
    def test_fnv_backend(self):
        test_value = 42.1
        expected = 140121297216442123210317922797979092383
        backend = FNVBloomFilterBackend()

        hashed_value = backend.hash_data(test_value)

        self.assertEqual(hashed_value, expected)

    def test_mmh3_backend(self):
        test_value = 42.1
        expected = 125910445295375924307876186304187122577
        backend = MMH3BloomFilterBackend()

        hashed_value = backend.hash_data(test_value)

        self.assertEqual(hashed_value, expected)

    def test_token_backend(self):
        test_value = 42.1
        test_vector = [data for data in struct.pack('f', test_value)]
        expected = sum(test_vector)

        with unittest.mock.patch('eeg_bloom_template.utils.orthonormalization.normalize_cached') as fake_normalize:
            fake_normalize.return_value = test_vector
            backend = TokenBackend('fake')
            hashed_value = backend.hash_data(test_value)

        self.assertEqual(hashed_value, expected)

    def test_token_backend_cache_flag(self):
        test_value = 42.1
        test_vector = [data for data in struct.pack('f', test_value)]
        cached_path = 'eeg_bloom_template.utils.orthonormalization.normalize_cached'
        normalizer_path = 'eeg_bloom_template.utils.orthonormalization.TokenMatrixNormalization'

        with unittest.mock.patch(cached_path) as fake_normalize:
            fake_normalize.return_value = test_vector
            backend = TokenBackend('fake', use_cache=True)
            backend.run_hash_function(b'1')
            cached_called = fake_normalize.called
        with unittest.mock.patch(normalizer_path) as fake_normalizer:
            fake_normalizer.return_value.normalize.return_value = test_vector
            backend = TokenBackend('fake', use_cache=False)
            backend.run_hash_function(b'1')
            normalizer_called = fake_normalizer.called

        self.assertTrue(cached_called)
        self.assertTrue(normalizer_called)
