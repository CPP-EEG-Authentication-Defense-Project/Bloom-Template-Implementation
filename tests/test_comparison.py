import unittest
import rbloom
import typing
import numpy as np

from eeg_bloom_template.base import BaseEEGTemplateData
from eeg_bloom_template.comparison import EEGTemplateDataChecker


class DummyEEGTemplateData(BaseEEGTemplateData):
    pass


class EEGTemplateDataCheckerTestCase(unittest.TestCase):
    def test_equal_data(self):
        test_data = np.random.rand(5)
        test_bloom_filters = self._make_test_bloom_filter(test_data)
        test_template = DummyEEGTemplateData(test_bloom_filters, 1)
        checker = EEGTemplateDataChecker(test_template, 0)

        equality_check = checker.check([test_data])

        self.assertTrue(equality_check)

    def test_non_equal_data(self):
        test_data_a = np.random.rand(5)
        test_data_b = np.random.rand(5)
        test_bloom_filters = self._make_test_bloom_filter(test_data_a)
        test_template = DummyEEGTemplateData(test_bloom_filters, 1)
        checker = EEGTemplateDataChecker(test_template, 0)

        equality_check = checker.check([test_data_b])

        self.assertFalse(equality_check)

    def test_semi_equal_data(self):
        # Test data B is half equal to test data A and the tolerance is 0.5, so result should be that the two are
        # considered equal by the checker.
        test_data_a = np.random.rand(10)
        test_data_b = np.concatenate((test_data_a[0:5], np.random.rand(5)))
        test_bloom_filters = self._make_test_bloom_filter(test_data_a)
        test_template = DummyEEGTemplateData(test_bloom_filters, 1)
        checker = EEGTemplateDataChecker(test_template, 0.5)

        equality_check = checker.check([test_data_b])

        self.assertTrue(equality_check)

    @staticmethod
    def _make_test_bloom_filter(data: np.ndarray) -> typing.List[rbloom.Bloom]:
        bloom_filter = rbloom.Bloom(len(data) * 2, 0.01)

        for element in data:
            bloom_filter.add(element)

        return [bloom_filter]
