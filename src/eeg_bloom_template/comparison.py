import dataclasses
import typing
import rbloom
import numpy as np

from .base import BaseEEGTemplateData
from .utils.iteration import iter_ratio_slices
from .utils.logging_helpers import get_logger


_logger = get_logger()


@dataclasses.dataclass
class ComparisonResult:
    """
    Simple container for comparison results.
    """
    elements_total: int
    hits: int

    @property
    def hit_ratio(self):
        """
        Calculates the ratio of hits over the total number of iterations used for the comparison.

        :returns: A hit ratio.
        """
        return self.hits / self.elements_total

    @property
    def deviation_ratio(self):
        """
        Calculates a ratio of deviation, based on the inverse of the hit ratio (i.e., the deviation is a miss ratio).

        :returns: A deviation ratio.
        """
        return 1 - self.hit_ratio


class EEGTemplateDataChecker:
    """
    Class which implements comparison operations for EEG templates against EEG feature data vectors. A tolerance
    value is used to indicate at which point the EEG data is to be considered a non-match for the template.
    """
    def __init__(self, template: BaseEEGTemplateData):
        self.template = template

    def check(self, eeg_data: typing.List[np.ndarray]) -> ComparisonResult:
        """
        Checks the given EEG feature data vectors to see if they are approximately a match for the template data.

        :param eeg_data: A list of EEG feature data vectors to check.
        :returns: A flag indicating whether the EEG feature data vectors are approximately a match.
        """
        try:
            elements_total = self._get_number_of_elements(eeg_data)
        except ValueError:
            _logger.warning('EEG data passed to comparison checker was not 2D matrix.')
            return ComparisonResult(hits=0, elements_total=0)
        hits = 0
        iterations = 0
        filter_idx = 0
        max_filter_idx = len(self.template.bloom_filters) - 1

        for segment in iter_ratio_slices(eeg_data, self.template.segment_ratio):
            new_hits = self._check_segment_against_filter(segment, self.template.bloom_filters[filter_idx])
            hits += new_hits
            filter_idx = min(filter_idx + 1, max_filter_idx)
            iterations += 1

        return ComparisonResult(elements_total=elements_total, hits=hits)

    @staticmethod
    def _get_number_of_elements(data: typing.List[np.ndarray]) -> int:
        """
        Calculates the number of elements in the given data matrix to be checked.

        :param data: A data matrix (i.e., a series of rows of EEG feature data to be checked).
        :returns: The total number of elements.
        """
        matrix = np.array(data)
        shape = matrix.shape
        if len(shape) != 2:
            raise ValueError(f'Expected 2D matrix of element data, got {len(shape)} dimensions.')
        return shape[0] * shape[1]

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
