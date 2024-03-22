import typing
import numpy as np

from .base import BaseEEGTemplateData


class EEGTemplateDataChecker:
    def __init__(self, template: BaseEEGTemplateData, tolerance: float):
        if not 0 < tolerance <= 1:
            raise ValueError(f'Tolerance must be between 0 and 1 (got {tolerance}).')
        self.template = template
        self.tolerance = tolerance

    def check(self, eeg_data: typing.List[np.ndarray]) -> bool:
        pass
