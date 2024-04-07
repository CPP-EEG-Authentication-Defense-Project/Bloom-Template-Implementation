import unittest
import rbloom
import numpy as np

from eeg_bloom_template import template, backend, comparison


class DummyHashBackend(backend.BaseBloomFilterHashBackend):
    def run_hash_function(self, data: bytes) -> int:
        return hash(data)

    @property
    def hash_function_name(self):
        return 'hash'


class EEGTemplateTestCase(unittest.TestCase):
    def test_make_template(self):
        dummy_data = [np.random.rand(5) for _ in range(10)]
        hash_backend = DummyHashBackend()

        eeg_template = template.EEGTemplate.make_template(
            dummy_data, hash_backend, 0.5, 0.01
        )

        self.assertIsInstance(eeg_template.bloom_filters, list)
        self.assertEqual(len(eeg_template.bloom_filters), 2)
        self.assertIsInstance(eeg_template.bloom_filters[0], rbloom.Bloom)
        self.assertIsInstance(eeg_template.bloom_filters[1], rbloom.Bloom)

    def test_make_column_template(self):
        # Order of dimensions is flipped from row-wise template, result should be same number of filters.
        dummy_data = [np.random.rand(10) for _ in range(5)]
        hash_backend = DummyHashBackend()

        eeg_template = template.EEGTemplate.make_template(
            dummy_data, hash_backend, 0.5, 0.01, row_wise=False
        )

        self.assertIsInstance(eeg_template.bloom_filters, list)
        self.assertEqual(len(eeg_template.bloom_filters), 2)

    def test_comparison(self):
        dummy_data = [np.random.rand(5)]
        bloom_filter = rbloom.Bloom(10, 0.01)
        for element in dummy_data[0]:
            bloom_filter.add(element)
        eeg_template = template.EEGTemplate([bloom_filter], 1)

        comparison_result = eeg_template.compare(dummy_data)

        self.assertIsInstance(comparison_result, comparison.ComparisonResult)
        self.assertEqual(comparison_result.elements_total, 5)
        self.assertEqual(comparison_result.hit_ratio, 1)

    def test_serialization(self):
        dummy_data = [np.random.rand(5) for _ in range(10)]
        hash_backend = DummyHashBackend()

        eeg_template = template.EEGTemplate.make_template(
            dummy_data, hash_backend, 0.5, 0.01
        )

        serialized = eeg_template.serialize()
        deserialized = template.EEGTemplate.deserialize(serialized)

        self.assertIsInstance(serialized, str)
        self.assertIsInstance(deserialized, template.EEGTemplate)
