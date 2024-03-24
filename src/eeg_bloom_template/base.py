import abc
import rbloom
import typing


class BaseEEGTemplateData(abc.ABC):
    """
    Abstract base class defining the general structure of an EEG template data class.
    """
    bloom_filters: typing.List[rbloom.Bloom]
    segment_ratio: float

    def __init__(self, bloom_filters: typing.List[rbloom.Bloom], segment_ratio: float):
        if not 0 < segment_ratio <= 1:
            raise ValueError(f'Segment ratio must be between 0 and 1, but got {segment_ratio}.')
        self.bloom_filters = bloom_filters
        self.segment_ratio = segment_ratio

    def __eq__(self, other: 'BaseEEGTemplateData') -> bool:
        if len(self.bloom_filters) != len(other.bloom_filters):
            return False
        a: rbloom.Bloom
        b: rbloom.Bloom
        for a, b in zip(self.bloom_filters, other.bloom_filters):
            # FIXME: this incorrectly throws an error claiming that the hash functions are not the same,
            #        even when they are.
            if a != b:
                return False
        return self.segment_ratio == other.segment_ratio
