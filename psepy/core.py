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
        if not isinstance(value, expected_type) or isinstance(value, str):
            raise TypeError(f"Parameter '{param}' must be of type {expected_type.__name__}, got {type(value).__name__}")
        if param == 'S':
            if value <= 0:
                raise ValueError(f" Parameter S must be positive integer valued")
        else:
            if len(value) != S:
                raise ValueError(f"Parameter '{param}' must have length of {S}")
            if not all(isinstance(item, (float, int)) and item > 0 for item in value):
                raise TypeError(f"Parameter '{param}' contains non-numeric values")
        
    # 检测 default args 是否在指定范围内
    for param, expected_range in expected_ranges.items():
        value = locals()[param]  # 获取局部变量值
        if value not in expected_range:
            raise ValueError(f"Parameter '{param}' must be in f{expected_range}")
    unit_mapping = {
        'seconds': 1,
        'minutes': 60,
        'hours': 3600,
        'parts/sec': 1,
        'parts/min': 1/60,
        'parts/hour': 1/3600
    }
    c = np.array(c) * unit_mapping[c_unit]
    T_up = np.array(T_up) * unit_mapping[T_up_unit]
    T_down = np.array(T_down) * unit_mapping[T_down_unit]

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
    else:
        product_term = np.prod(T_up / (T_up + T_down))
        mean_term = np.mean(T_up + T_down)
        # 最终结果
        c_agg = np.min(c)
        T_up_agg = mean_term * product_term
        T_down_agg = mean_term * (1 - product_term)

    return round(c_agg / unit_mapping[c_unit], 4), round(T_up_agg / unit_mapping[T_up_unit], 4), round(T_down_agg / unit_mapping[T_down_unit], 4)

def P_function_two_machine_bernoulli(p1:float,p2:float,N:int)->list:
    """
    This function takes in two machine whose  p1 and p2 are the probability of the machine to be working at any given time. 
    N is the maximum capacity of the buffer between the two machines
    The function then returns a list contains the probability of the buffer being 0-N at any given time.

    When p1 \neq p2:
    P_0 = \frac{1 - p_2}{1 - p_2 + \alpha + \alpha^2 + \ldots + \alpha^N}
    P_i=\frac{\alpha^i}{1 - p_2}P_0, i = 1, 2, \ldots, N
    where \alpha = \frac{p_1(1 - P_2)}{P_1(1 - p_2)}

    When p1 = p2 = p:
    P_0 = \frac{1 - p}{N + 1 - p}
    P_i = \frac{1}{N + 1 - p}, i = 1, 2, \ldots, N
    Parameters:
    p1 (float): The probability of machine 1 working at any given time
    p2 (float): The probability of machine 2 working at any given time
    N (int): The maximum capacity of the buffer between the two machines

    Returns:
    list: The probability of the buffer being 0-N at any given time
    """
    if p1 == p2:
        P_0 = (1 - p1)/(N + 1 - p1)
        P = [P_0] + [1/(N + 1 - p1)]*N
    else:
        alpha = p1*(1 - p2)/(p2*(1 - p1))
        P_0 = (1 - p2)/(1 - p2 + sum([alpha**i for i in range(1, N + 1)]))
        P = [P_0] + [alpha**i/(1 - p2)*P_0 for i in range(1, N + 1)]
    return P


def Q_function(p1:float,p2:float,N:int)->float:

    """
    This function takes in two machine whose  p1 and p2 are the probability of the machine to be working at any given time. 
    N is the maximum capacity of the buffer between the two machines
    This function is used to calculate the probability of the buffer is empty.
    
    When p1 \neq p2:
    Q(p_1, p_2, N)= \frac{(1 - p_1)(1 - \alpha(p_1, p_2))}{1 - \frac{p_1}{p_2}alpha^N(p_1, p_2)}
    where \alpha(p_1, p_2) = \frac{p_1(1 - p_2)}{p_2(1 - p_1)}

    When p1 = p2 = p:
    Q(p, p, N) = \frac{1 - p}{N + 1 - p}

    Parameters:
    p1 (float): The probability of machine 1 working at any given time
    p2 (float): The probability of machine 2 working at any given time
    N (int): The maximum capacity of the buffer between the two machines

    Returns:
    float: The probability of the buffer being empty
    """
    if p1 == p2:
        return (1 - p1)/(N + 1 - p1)
    else:
        alpha = p1*(1 - p2)/(p2*(1 - p1))
        return (1 - p1)*(1 - alpha)/(1 - p1*alpha**N/p2)
    
def performance_measure_two_machine(p1:float,p2:float,N:int)->dict:
    """
    This function takes in two machine whose  p1 and p2 are the probability of the machine to be working at any given time. 
    N is the maximum capacity of the buffer between the two machines
    The function then returns a dictionary containing the performance measures of the system, 
    which contains the production rate(PR), work-in-process(WIP), blockages of machine 1(BL_1) and starvations of machine 2(ST_2).

    PR = p_2(1 - Q(p_1, p_2, N))

    WIP = \sum_{i=0}^{N}iP_i
    when p_1 \neq p_2:
    WIP=\frac{p_i}{p_2 - p_1\alpha^N(p_1, p_2)}*(\frac{1-\alpha^N(p_1, p_2)}{1-\alpha(p_1, p_2)} - N\alpha^N(p_1, p_2))
    when p_1 = p_2 = p:
    WIP=\frac{N(N + 1)}{2(N + 1 - p)}

    BL_1 = p_1Q(p_2, p_1, N)

    ST_2 = p_2Q(p_1, p_2, N)

    Parameters:
    p1 (float): The probability of machine 1 working at any given time
    p2 (float): The probability of machine 2 working at any given time
    N (int): The maximum capacity of the buffer between the two machines

    Returns:
    dict: The performance measures of the system, 
    which contains the production rate(PR), work-in-process(WIP), blockages of machine 1(BL_1) and starvations of machine 2(ST_2). 
    And PR, BL, and ST are round to four significant digits, WIP is round to two decimal places.
    """
    PR = round(p2*(1 - Q_function(p1, p2, N)), 4)
    if p1 == p2:
        WIP = round(N*(N + 1)/(2*(N + 1 - p1)), 2)
    else:
        alpha = p1*(1 - p2)/(p2*(1 - p1))
        WIP = round(p1/(p2 - p1*alpha**N)*((1 - alpha**N)/(1 - alpha) - N*alpha**N) , 2)
    BL_1 = round(p1*Q_function(p2, p1, N), 4)
    ST_2 = round(p2*Q_function(p1, p2, N), 4)
    return {"PR": PR, "WIP": WIP, "BL_1": BL_1, "ST_2": ST_2}

def aggregation_of_bernoulli_lines(p: list[float],M: int,N: list[int])->tuple[list[float], list[float]]:
    """
    This function takes in a list of the probability of each machine working at any time from a Bernoulli line
    and a list of the maximum capacity of the buffer between each machine.
    The function then returns a tuple containing the list of the probability of forward aggregation p^f and the list of the probability of backward aggregation p^b.

    The recursive aggregation procedure is as follows:
    
    defination: 
        s is the number of iterations, s = 0, 1, 2, ...
        p_i is the probability of machine i working at any given time
        
        initial condition:
            p_i^f(0) = p_i, i = 1, 2, ..., M
        
        boundary condition:
            p_1^f(s) = p_1, s = 0, 1, 2, ...
            p_M^b(s) = p_M, s = 0, 1, 2, ...
        
        forward aggregation:
            p_i^b(s+1) = p_i[1 - Q(p_{i + 1}^b(s + 1), p_i^f(s), N_i)], i = M - 1, M - 2, ..., 1
        
        backward aggregation:
            p_i^f(s+1) = p_i[1 - Q(p_{i - 1}^f(s + 1), p_i^b(s + 1), N_{i - 1})], i = 2, 3, ..., M

        Termination condition:
            The iteration continues until the difference between p_i^f(s) and p_i^f(s - 1) is less than 1e-6 for all i = 2, 3, ..., M;
            The iteration continues until the difference between p_i^b(s) and p_i^b(s - 1) is less than 1e-6 for all i = 2, 3, ..., M; 

    Parameters:
        p (list[float]): The probability of each machine working at any time from a Bernoulli line
        M (int): The number of machines
        N (list[int]): The maximum capacity of the buffer between each machine

    Returns:
        tuple[list[float], list[float]]: The tuple containing the list of the probability of forward aggregation p^f and the list of the probability of backward aggregation p^b
    """

    p_f = p.copy()
    p_b = p.copy()
    while True:
        p_f_new = p_f.copy()
        p_b_new = p_b.copy()
 
        for i in range(M - 2, -1, -1):
            p_b_new[i] = p[i]*(1 - Q_function(p_b_new[i+1], p_f_new[i], N[i]))
        
        for i in range(1, M):
            p_f_new[i] = p[i]*(1 - Q_function(p_f_new[i - 1], p_b_new[i], N[i - 1]))
        if all(abs(p_f_new[i] - p_f[i]) < 1e-6 for i in range(0, M)) and all(abs(p_b_new[i] - p_b[i]) < 1e-6 for i in range(0, M)):
            break
        p_f = p_f_new
        p_b = p_b_new
    return [round(pf,4) for pf in p_f], [round(pb,4) for pb in p_b]

def performance_measure_multiply_machine_bernoulli(p: list[float],M: int,N: list[int],t: float)->dict:
    """
    This function takes in a list of the probability of each machine working at any time from a Bernoulli line
    and a list of the maximum capacity of the buffer between each machine, t is the time period of the system.
    The function then returns a dictionary containing the performance measures of the system, 
    which contains the list p, p_f, p_b,N, the production rate(PR), work-in-process(WIP), blockages of each machine(BL), starvations of each machine(ST) ,throughput(TP) and the total WIP.

    where p_f and p_b are the probability of forward and backward aggregation respectively, which are calculated from the aggregation_of_bernoulli_lines function.

    The performance measures of the system are calculated as follows:
    
        PR = p^b[0] = p_f[M-1]

        when p_f[i] != p_b[i+1]:
            WIP[i] = \frac{p_f[i]}{p_{b}[i+1] - p_f[i]\alpha^{N[i]}(p_f[i],p_b[i+1])}*(\frac{1-\alpha^{N[i]}(p_f[i],p_b[i+1])}{1-\alpha(p_f[i],p_b[i+1])} - N[i]\alpha^{N[i]}(p_f[i],p_b[i+1]))
        when p_f[i] = p_b[i+1]:
            WIP[i]=\frac{N[i](N[i] + 1)}{2(N[i] + 1 - p_f[i])}
        where i = 1,2,...,M-1
            
        TotalWIP = \sum_{i=1}^{M-1}WIP[i]


        BL[i] = p[i] * Q(p_b[i+1], p_f[i], N[i]), i = 1, 2, ..., M - 1 

        ST[i] = p[i] * Q(p_f[i-1], p_b[i], N[i-1]), i = 2, 3, ..., M

        TP = PR/t
    
    Parameters:
        p (list[float]): The probability of each machine working at any time from a Bernoulli line
        M (int): The number of machines
        N (list[int]): The maximum capacity of the buffer between each machine
        t (float): The time period of the system

    Returns:
        dict: The performance measures of the system, 
        which contains list p, p_f, p_b,N, the production rate(PR), work-in-process(WIP), blockages of each machine(BL), starvations of each machine(ST), TP and the total WIP.
        And PR, BL, ST, TP are round to four significant digits, WIP is round to two decimal places, they are all list.
        The total WIP is the sum of the WIP of each machine, which is round to two decimal places.
    """

    p_f, p_b = aggregation_of_bernoulli_lines(p, M, N)
    PR = round(p_b[0], 4)
    WIP = []
    BL = []
    ST = []
    for i in range(0, M-1):
        if p_f[i] != p_b[i+1]:
            alpha = p_f[i]*(1 - p_b[i+1])/(p_b[i+1]*(1 - p_f[i]))
            WIP.append(p_f[i]/(p_b[i+1] - p_f[i]*alpha**N[i])*((1 - alpha**N[i])/(1 - alpha) - N[i]*alpha**N[i]))
        else:
            WIP.append(N[i]*(N[i] + 1)/(2*(N[i] + 1 - p_f[i])))
    for i in range(0, M-1):
        BL.append(round(p[i]*Q_function(p_b[i+1], p_f[i], N[i]), 4))
    BL.append(0)
    ST.append(0)
    for i in range(1, M):
        ST.append(round(p[i]*Q_function(p_f[i - 1], p_b[i], N[i - 1]), 4))
    
    TotalWIP = round(sum(WIP), 2)
    WIP = [round(w, 2) for w in WIP]
    TP = round(PR/t, 4)
    return {"p":p, 'pf':p_f, 'pb':p_b, "ST": ST, "BL": BL, 'N':N,"WIP": WIP, "PR": PR, "TotalWIP": TotalWIP, "TP":TP}