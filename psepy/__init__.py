# psepy/__init__.py

"""
PSEPY: Production System Engineering with Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PSEPY is a Python library for production system engineering calculations,
focusing on machine aggregation and Bernoulli line analysis.

Basic usage:
    >>> from psepy import MachineAggregator
    >>> aggregator = MachineAggregator()
    >>> result = aggregator.aggregate_machines(...)

For more information, please see: https://github.com/yourusername/psepy
"""

from .machine_aggregator import MachineAggregator
from .bernoulli_line import BernoulliLine
from .validators import InputValidator

__version__ = "0.1.0"
__author__ = "Your Name"
__license__ = "MIT"

__all__ = [
    "MachineAggregator",
    "BernoulliLine",
    "InputValidator",
]
