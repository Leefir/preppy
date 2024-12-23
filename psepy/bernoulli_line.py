from typing import List, Dict, Union
from .validators import InputValidator

class BernoulliLine:
    def __init__(self):
        self.validator = InputValidator()

    def calculate_buffer_probabilities(self, p1: float, p2: float, N: int) -> List[float]:
        """Calculate probability of buffer states for two-machine Bernoulli line"""
        # Validate inputs
        if not 0 <= p1 <= 1:
            raise ValueError(f"Parameter 'p1' must be between 0 and 1, got {p1}")
        if not 0 <= p2 <= 1:
            raise ValueError(f"Parameter 'p2' must be between 0 and 1, got {p2}")
        if N <= 0:
            raise ValueError(f"Parameter 'N' must be positive, got {N}")

        if p1 == p2:
            return self._equal_probability_case(p1, N)
        return self._different_probability_case(p1, p2, N)

    def _equal_probability_case(self, p: float, N: int) -> List[float]:
        """Calculate buffer probabilities when p1 equals p2"""
        P_0 = (1 - p)/(N + 1 - p)
        return [P_0] + [1/(N + 1 - p)]*N

    def _different_probability_case(self, p1: float, p2: float, N: int) -> List[float]:
        """Calculate buffer probabilities when p1 is not equal to p2"""
        alpha = p1*(1 - p2)/(p2*(1 - p1))
        P_0 = (1 - p2)/(1 - p2 + sum([alpha**i for i in range(1, N + 1)]))
        return [P_0] + [alpha**i/(1 - p2)*P_0 for i in range(1, N + 1)] 