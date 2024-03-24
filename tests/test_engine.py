import unittest
import rbloom
import numpy as np

from eeg_bloom_template.backend import BaseBloomFilterHashBackend
from eeg_bloom_template.engine import EEGBloomFilterTemplateEngine


class DummyBloomFilterHashBackend(BaseBloomFilterHashBackend):
    def run_hash_function(self, data: bytes) -> int:
        return hash(data)


class BloomFilterTemplateEngineTestCase(unittest.TestCase):
    def test_generates_bloom_filters(self):
        data_frames = [np.random.rand(10) for _ in range(10)]
        engine = EEGBloomFilterTemplateEngine(
            DummyBloomFilterHashBackend(),
            0.25,
            0.1
        )

        filters = engine.create_template_data(data_frames)

        self.assertEqual(len(filters), 5)
        for bloom_filter in filters:
            self.assertIsInstance(bloom_filter, rbloom.Bloom)
