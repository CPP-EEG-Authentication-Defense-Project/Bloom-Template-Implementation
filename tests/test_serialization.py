import unittest
import rbloom

from eeg_bloom_template.backend import BaseBloomFilterHashBackend
from eeg_bloom_template.base import BaseEEGTemplateData
from eeg_bloom_template.serialization import EEGTemplateDataSerializer


class DummyBloomFilterHashBackend(BaseBloomFilterHashBackend):
    def run_hash_function(self, data: bytes) -> int:
        return hash(data)

    @property
    def hash_function_name(self) -> str:
        return 'hash'


class DummyEEGTemplateData(BaseEEGTemplateData):
    pass


class EEGTemplateDataSerializerTestCase(unittest.TestCase):
    def test_serialize_data(self):
        template = DummyEEGTemplateData(
            [rbloom.Bloom(10, 0.01, DummyBloomFilterHashBackend())],
            0.5
        )
        serializer = EEGTemplateDataSerializer(DummyEEGTemplateData)
        data_string = serializer.serialize(template)
        restored = serializer.deserialize(data_string)

        self.assertIsInstance(data_string, str)
        self.assertEqual(template, restored)
