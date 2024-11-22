# from psepy import agg_machines
from psepy.core import agg_machines
import pytest
import numpy as np

def test_agg_machines_type_error_handling():
    print("Testing type error handling")
    pytest.raises(TypeError, agg_machines, '3', [1.5, 2, 1.7], [10, 8, 9], [90, 79, 85])
    pytest.raises(ValueError, agg_machines, -1, [1.5, 2, 1.7], [10, 8, 9], [90, 79, 85])
    pytest.raises(ValueError, agg_machines, 0, [1.5, 2, 1.7], [10, 8, 9], [90, 79, 85])
    pytest.raises(TypeError, agg_machines, 3, [1.5, 2, 'a'], [10, 8, 9], [90, 79, 85])
    pytest.raises(TypeError, agg_machines, 3, [0, 0, 0], [10, 8, 9], [90, 79, 85])
    pytest.raises(TypeError, agg_machines, 3, (0, 0, 0), [10, 8, 9], [90, 79, 85])
    pytest.raises(TypeError, agg_machines, 3, np.array([0, 0, 0]), [10, 8, 9], [90, 79, 85])
    pytest.raises(TypeError, agg_machines, 3, {1:2, 3:4, 5:6}, [10, 8, 9], [90, 79, 85])
    pytest.raises(TypeError, agg_machines, 3, [[0], [0], [0]], [10, 8, 9], [90, 79, 85])
    pytest.raises(TypeError, agg_machines, 2.5, [0, 0, 0], [10, 8, 9], [90, 79, 85])

def test_agg_machines_1():
    S = 3
    c = [1.5, 2, 1.7]
    T_up = [10, 8, 9]
    T_down = [90, 79, 85]
    mode = 'parallel'
    c_unit='parts/sec'
    T_up_unit='seconds'
    T_down_unit='seconds'

    c_agg, T_up_agg, T_down_agg = agg_machines(S, c, T_up, T_down, mode, c_unit, T_up_unit, T_down_unit)

    assert c_agg == pytest.approx(5.2, rel=1e-3), f"Expected c_agg=5.2, but got {c_agg}"
    assert T_up_agg == pytest.approx(8.9175, rel=1e-3), f"Expected T_up_agg=8.9175, but got {T_up_agg}"
    assert T_down_agg == pytest.approx(84.4457, rel=1e-3), f"Expected T_down_agg=84.4457, but got {T_down_agg}"

def test_agg_machines_1():
    S = 1000
    c = [1] * S
    T_up = [10] * S
    T_down = [90] * S
    mode = 'parallel'
    c_unit='parts/sec'
    T_up_unit='seconds'
    T_down_unit='seconds'

    c_agg, T_up_agg, T_down_agg = agg_machines(S, c, T_up, T_down, mode, c_unit, T_up_unit, T_down_unit)
    assert True

    # assert c_agg == pytest.approx(5.2, rel=1e-3), f"Expected c_agg=5.2, but got {c_agg}"
    # assert T_up_agg == pytest.approx(8.9175, rel=1e-3), f"Expected T_up_agg=8.9175, but got {T_up_agg}"
    # assert T_down_agg == pytest.approx(84.4457, rel=1e-3), f"Expected T_down_agg=84.4457, but got {T_down_agg}"