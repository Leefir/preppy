import pytest
import numpy as np
from psepy.validators import InputValidator

class TestInputValidator:
    def setup_method(self):
        self.validator = InputValidator()

    def test_validate_numeric_iterable(self):
        # Valid case
        self.validator.validate_numeric_iterable([1.0, 2.0], 2, "test")

        # Invalid cases
        with pytest.raises(TypeError):
            self.validator.validate_numeric_iterable("not_iterable", 2, "test")
        
        with pytest.raises(ValueError):
            self.validator.validate_numeric_iterable([1.0], 2, "test")
        
        with pytest.raises(TypeError):
            self.validator.validate_numeric_iterable([1.0, "string"], 2, "test")

    def test_validate_positive_int(self):
        # Valid case
        self.validator.validate_positive_int(1, "test")

        # Invalid cases
        with pytest.raises(ValueError):
            self.validator.validate_positive_int(0, "test")
        
        with pytest.raises(ValueError):
            self.validator.validate_positive_int(-1, "test")
        
        with pytest.raises(ValueError):
            self.validator.validate_positive_int(1.5, "test")

    def test_validate_probability(self):
        # Valid cases
        self.validator.validate_probability(0.5, "test")
        self.validator.validate_probability(0.0, "test")
        self.validator.validate_probability(1.0, "test")

        # Invalid cases
        with pytest.raises(ValueError):
            self.validator.validate_probability(-0.1, "test")
        
        with pytest.raises(ValueError):
            self.validator.validate_probability(1.1, "test") 