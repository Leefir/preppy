from typing import Iterable, Union, Tuple
import numpy as np
from .constants import UNIT_MAPPING, VALID_MODES, VALID_TIME_UNITS, VALID_PRODUCTION_UNITS
from .validators import InputValidator

class MachineAggregator:
    def __init__(self):
        self.validator = InputValidator()

    def aggregate_machines(
        self,
        S: int, 
        c: Iterable[Union[float, int]], 
        T_up: Iterable[Union[float, int]], 
        T_down: Iterable[Union[float, int]], 
        mode: str = 'parallel',
        c_unit: str = 'parts/sec',
        T_up_unit: str = 'seconds',
        T_down_unit: str = 'seconds'
    ) -> Tuple[float, float, float]:
        """Aggregating machines for structural modeling"""
        from .core import agg_machines  # Import here to avoid circular imports
        return agg_machines(S, c, T_up, T_down, mode, c_unit, T_up_unit, T_down_unit) 