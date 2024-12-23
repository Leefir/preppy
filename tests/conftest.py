import pytest
import numpy as np

@pytest.fixture
def sample_machine_data():
    return {
        'S': 2,
        'c': [1.0, 2.0],
        'T_up': [100, 200],
        'T_down': [10, 20],
        'mode': 'parallel'
    }

@pytest.fixture
def sample_bernoulli_data():
    return {
        'p1': 0.8,
        'p2': 0.7,
        'N': 5
    } 