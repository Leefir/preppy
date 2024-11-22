from typing import Iterable, Union
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
    pass
    # expected_types = {
    #     'S': int, 
    #     'c': Iterable, 
    #     'T_up': Iterable, 
    #     'T_down': Iterable, 
    # }
    # expected_ranges = {
    #     'mode': ['parallel', 'consecutive dependent'],
    #     'c_unit': ['parts/sec', 'parts/min', 'parts/hour'],
    #     'T_up_unit': ['seconds', 'minutes', 'hours'],
    #     'T_down_unit': ['seconds', 'minutes', 'hours']
    # }
    
    # for param, expected_type in expected_types.items():
    #     value = locals()[param]  # 获取局部变量值
    #     if not isinstance(value, expected_type):
    #         raise TypeError(f"Parameter '{param}' must be of type {expected_type.__name__}, got {type(value).__name__}")
    #     if param != 'S' and len(param) != S:
    #         raise ValueError(f"Parameter '{param} must have length of {S}'")
    # for param, expected_range in expected_ranges.items():
    #     value = locals()[param]  # 获取局部变量值
    #     if value not in expected_range:
    #         raise ValueError(f"Parameter '{param}' must be in f{expected_range}")
        
    # if len(c) != S
        
    # c_agg = sum(c)
    # T_up_agg = 

    



