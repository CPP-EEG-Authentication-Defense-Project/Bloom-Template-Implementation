import unittest
import rbloom

from eeg_bloom_template.backend import BaseBloomFilterHashBackend
from eeg_bloom_template.base import BaseEEGTemplateData
from eeg_bloom_template.serialization import EEGTemplateDataSerializer


class DummyBloomFilterHashBackend(BaseBloomFilterHashBackend):
    def run_hash_function(self, data: bytes) -> int:
        return hash(data)


class DummyEEGTemplateData(BaseEEGTemplateData):
    pass


class EEGTemplateDataSerializerTestCase(unittest.TestCase):
    def test_serialize_data(self):
        template = DummyEEGTemplateData(
            [rbloom.Bloom(10, 0.01, DummyBloomFilterHashBackend())],
            0.5,
            row_wise=True
        )
        serializer = EEGTemplateDataSerializer(DummyEEGTemplateData)
        data_string = serializer.serialize(template)
        restored = serializer.deserialize(data_string)

        self.assertIsInstance(data_string, str)
        self.assertEqual(len(template.bloom_filters), len(restored.bloom_filters))
        self.assertEqual(template.segment_ratio, restored.segment_ratio)
        self.assertEqual(template.row_wise, restored.row_wise)
        a: rbloom.Bloom
        b: rbloom.Bloom
        for a, b in zip(template.bloom_filters, restored.bloom_filters):
            self.assertEqual(a.hash_func, b.hash_func)
