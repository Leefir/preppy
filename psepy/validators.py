from typing import Any, Iterable

class InputValidator:
    @staticmethod
    def validate_numeric_iterable(value: Any, length: int, param_name: str) -> None:
        if not isinstance(value, Iterable) or isinstance(value, str):
            raise TypeError(f"Parameter '{param_name}' must be an iterable")
        
        if len(value) != length:
            raise ValueError(f"Parameter '{param_name}' must have length of {length}")
            
        if not all(isinstance(item, (float, int)) and item > 0 for item in value):
            raise TypeError(f"Parameter '{param_name}' must contain positive numeric values")

    @staticmethod
    def validate_positive_int(value: int, param_name: str) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"Parameter '{param_name}' must be a positive integer")

    @staticmethod
    def validate_probability(value: float, param_name: str) -> None:
        if not isinstance(value, (float, int)) or not 0 <= value <= 1:
            raise ValueError(f"Parameter '{param_name}' must be a probability between 0 and 1") 