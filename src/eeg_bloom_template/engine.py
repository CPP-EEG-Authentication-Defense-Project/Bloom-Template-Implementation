import rbloom
import typing
import numpy as np

from .backend import BaseBloomFilterHashBackend
from .utils.iteration import iter_ratio_slices


class EEGBloomFilterTemplateEngine:
    """
    Template generation engine, which helps to assemble data used for creating EEG templates based on Bloom Filters.
    """
    _encoding = 'utf-8'

    def __init__(self, backend: BaseBloomFilterHashBackend, segment_ratio: float, false_positive_rate: float):
        self._backend = backend
        self._segment_ratio = segment_ratio
        self._false_positive_rate = false_positive_rate

    def create_template_data(self, data: typing.List[np.ndarray]) -> typing.List[rbloom.Bloom]:
        """
        Creates data to be used for the EEG template, essentially a list of Bloom Filters which contain
        normalized data.

        :param data: The list of EEG data feature vectors to use to generate template data.
        :returns: The list of Bloom Filters to be used for a template.
        """
        filters = []

        for segment in iter_ratio_slices(data, self._segment_ratio):
            filters.append(self._generate_bloom_filter(segment))

        return filters

    def _generate_bloom_filter(self, segment: typing.List[np.ndarray]) -> rbloom.Bloom:
        """
        Helper method used to generate a Bloom Filter from a given data segment (i.e., a subsection of EEG feature
        data from a broader collection). The segment will be averaged column-wise in order to normalize it for
        use with the Bloom Filter.

        :param segment: The segment of data to use to generate the Bloom Filter.
        :returns: The Bloom Filter.
        """
        matrix = np.array(segment)
        if matrix.ndim != 2:
            raise ValueError(f'Expected data segment to be a 2D array, got {matrix.ndim} dimensions.')
        number_of_items = matrix.shape[1]
        bloom_filter = rbloom.Bloom(number_of_items * 2, self._false_positive_rate, self._backend)
        normalized_segment = matrix.mean(axis=0)

        for item in normalized_segment:
            bloom_filter.add(item)

        return bloom_filter
