import abc
import rbloom
import typing


class BaseEEGTemplateData(abc.ABC):
    """
    Abstract base class defining the general structure of an EEG template data class.
    """
    bloom_filters: typing.List[rbloom.Bloom]

    def __init__(self, bloom_filters: typing.List[rbloom]):
        self.bloom_filters = bloom_filters
