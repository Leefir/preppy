from typing import Dict

# Unit conversion mappings
UNIT_MAPPING: Dict[str, float] = {
    'seconds': 1,
    'minutes': 60,
    'hours': 3600,
    'parts/sec': 1,
    'parts/min': 1/60,
    'parts/hour': 1/3600
}

# Valid parameter ranges
VALID_MODES = ['parallel', 'consecutive dependent']
VALID_TIME_UNITS = ['seconds', 'minutes', 'hours']
VALID_PRODUCTION_UNITS = ['parts/sec', 'parts/min', 'parts/hour']

# Convergence threshold for iterative calculations
CONVERGENCE_THRESHOLD = 1e-6 