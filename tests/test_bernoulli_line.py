import pytest
import numpy as np
from psepy.bernoulli_line import BernoulliLine

class TestBernoulliLine:
    def setup_method(self):
        self.line = BernoulliLine()

    def test_calculate_buffer_probabilities(self, sample_bernoulli_data):
        result = self.line.calculate_buffer_probabilities(
            p1=sample_bernoulli_data['p1'],
            p2=sample_bernoulli_data['p2'],
            N=sample_bernoulli_data['N']
        )
        
        assert isinstance(result, list)
        assert len(result) == sample_bernoulli_data['N'] + 1
        assert all(isinstance(x, float) for x in result)
        assert abs(sum(result) - 1.0) < 1e-10  # Probabilities should sum to 1

    def test_equal_probability_case(self):
        p = 0.7
        N = 5
        result = self.line._equal_probability_case(p, N)
        
        assert isinstance(result, list)
        assert len(result) == N + 1
        assert abs(sum(result) - 1.0) < 1e-10

    def test_invalid_probabilities(self):
        with pytest.raises(ValueError):
            self.line.calculate_buffer_probabilities(1.5, 0.7, 5)
        
        with pytest.raises(ValueError):
            self.line.calculate_buffer_probabilities(0.7, -0.1, 5)

    def test_invalid_buffer_size(self):
        with pytest.raises(ValueError):
            self.line.calculate_buffer_probabilities(0.7, 0.7, 0) 