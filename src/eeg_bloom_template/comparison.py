import typing
import rbloom
import numpy as np

from .base import BaseEEGTemplateData
from .utils import iter_ratio_slices


class EEGTemplateDataChecker:
    """
    Class which implements comparison operations for EEG templates against EEG feature data vectors. A tolerance
    value is used to indicate at which point the EEG data is to be considered a non-match for the template.
    """
    def __init__(self, template: BaseEEGTemplateData, tolerance: float):
        if not 0 <= tolerance <= 1:
            raise ValueError(f'Tolerance must be between 0 and 1 inclusive (got {tolerance}).')
        self.template = template
        self.tolerance = tolerance

    def check(self, eeg_data: typing.List[np.ndarray]) -> bool:
        """
        Checks the given EEG feature data vectors to see if they are approximately a match for the template data.

        :param eeg_data: A list of EEG feature data vectors to check.
        :returns: A flag indicating whether the EEG feature data vectors are approximately a match.
        """
        hits = 0
        iterations = 0
        filter_idx = 0
        number_of_filters = len(self.template.bloom_filters)

        for segment in iter_ratio_slices(eeg_data, self.template.segment_ratio):
            new_hits = self._check_segment_against_filter(segment, self.template.bloom_filters[filter_idx])
            hits += new_hits
            filter_idx = min(filter_idx + 1, number_of_filters)
            iterations += 1

        hit_ratio = hits / iterations
        deviation_ratio = 1 - hit_ratio

        return deviation_ratio <= self.tolerance

    @classmethod
    def _check_segment_against_filter(cls, data_segment: typing.List[np.ndarray], bloom_filter: rbloom.Bloom) -> int:
        """
        Accumulates the number of matching elements are found in the vectors passed from the given data segment, using
        the given Bloom Filter.

        :param data_segment: The segment of EEG feature data vectors to check.
        :param bloom_filter: The Bloom Filter to use to check the vectors.
        :returns: The number of matching elements.
        """
        hits = 0
        for vector in data_segment:
            new_hits = cls._check_vector_against_filter(vector, bloom_filter)
            hits += new_hits
        return hits

    @staticmethod
    def _check_vector_against_filter(vector: np.ndarray, bloom_filter: rbloom.Bloom) -> int:
        """
        Accumulates the number of matching elements are found in the given feature data vector, using the given
        Bloom Filter.

        :param vector: The feature data vector to check.
        :param bloom_filter: The Bloom Filter to use to check the vector.
        :returns: The number of matching elements from the vector.
        """
        hits = 0
        for element in vector:
            if element in bloom_filter:
                hits += 1
        return hits
