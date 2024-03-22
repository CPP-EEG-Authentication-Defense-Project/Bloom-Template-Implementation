import abc
import rbloom
import typing


class BaseEEGTemplateData(abc.ABC):
    """
    Abstract base class defining the general structure of an EEG template data class.
    """
    bloom_filters: typing.List[rbloom.Bloom]
    segment_ratio: float

    def __init__(self, bloom_filters: typing.List[rbloom], segment_ratio: float):
        if not 0 < segment_ratio <= 1:
            raise ValueError(f'Segment ratio must be between 0 and 1, but got {segment_ratio}.')
        self.bloom_filters = bloom_filters
        self.segment_ratio = segment_ratio
