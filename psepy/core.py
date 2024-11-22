from typing import Iterable, Union
import numpy as np

def agg_machines(
    S: int, 
    c: Iterable[Union[float, int]], 
    T_up: Iterable[Union[float, int]], 
    T_down: Iterable[Union[float, int]], 
    mode='parallel', 
    c_unit='parts/sec',
    T_up_unit='seconds',
    T_down_unit='seconds'
) -> tuple:
    """Aggregating machines for structural modeling

    Args:
        S (int): Number of machines
        c (Iterable[Union[float, int]]): Machine capacity - number of parts produced per unit of time
        T_up (Iterable[Union[float, int]]): Up time
        T_down (Iterable[Union[float, int]]): Down time
        mode (str, optional): parallel or consecutive dependent. Defaults to 'parallel'.
        c_unit (str, optional): Unit of c. Defaults to 'parts/sec'.
        T_up_unit (str, optional): Unit of T_up. Defaults to 'seconds'.
        T_down_unit (str, optional): Unit of T_down. Defaults to 'seconds'.

    Raises:
        TypeError: _description_
        TypeError: _description_

    Returns:
        tuple: _description_
    """
    expected_types = {
        'S': int, 
        'c': Iterable, 
        'T_up': Iterable, 
        'T_down': Iterable, 
    }
    expected_ranges = {
        'mode': ['parallel', 'consecutive dependent'],
        'c_unit': ['parts/sec', 'parts/min', 'parts/hour'],
        'T_up_unit': ['seconds', 'minutes', 'hours'],
        'T_down_unit': ['seconds', 'minutes', 'hours']
    }
    # 检测 positional args 类型和取值
    for param, expected_type in expected_types.items():
        value = locals()[param] 
        if not isinstance(value, expected_type):
            raise TypeError(f"Parameter '{param}' must be of type {expected_type.__name__}, got {type(value).__name__}")
        if param == 'S':
            if value <= 0:
                raise ValueError(f" Parameter S must be positive integer valued")
        else:
            if len(value) != S:
                raise ValueError(f"Parameter '{param}' must have length of {S}")
            if not all(isinstance(item, (float, int)) for item in value):
                raise TypeError(f"Parameter '{param}' contains non-numeric values")
        
    # 检测 default args 是否在指定范围内
    for param, expected_range in expected_ranges.items():
        value = locals()[param]  # 获取局部变量值
        if value not in expected_range:
            raise ValueError(f"Parameter '{param}' must be in f{expected_range}")

    c = np.array(c)
    T_up = np.array(T_up)
    T_down = np.array(T_down)

    if mode == "parallel":
        # 计算 τ_i
        tau = 1 / c

        # 初始化聚合结果
        T_up_agg = 0
        T_down_agg = 0
        T_agg_denominator = 0

        for i in range(S):
            # 当前机器的 T_up, T_down 和 tau
            T_up_i = T_up[i]
            T_down_i = T_down[i]
            tau_i = tau[i]
            
            product_term = np.prod([1 / T_up[j] + 1 / T_down[j] for j in range(S) if j != i])
            
            # 累积 T_up_agg^par
            T_up_agg += (1 / (tau_i * T_down_i)) * product_term

            # 累积 T_down_agg^par
            T_down_agg += (1 / (tau_i * T_up_i)) * product_term
            # 累积分母部分
            T_agg_denominator += (1 / (T_up_i * T_down_i)) * product_term

        # 最终结果
        c_agg = np.sum(c)
        coef = S / c_agg / T_agg_denominator
        T_up_agg *= coef
        T_down_agg *= coef
        return c_agg, T_up_agg, T_down_agg
    else:
        pass


    



