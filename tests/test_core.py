def test_agg_machines():
    S = 3
    c = [1.5, 2, 1.7]
    T_up = [10, 8, 9]
    T_down = [90, 79, 85]
    mode = 'parallel'
    c_unit='parts/sec'
    T_up_unit='seconds'
    T_down_unit='seconds'
    # c_agg, T_up_agg, T_down_agg = agg_machines(S, c, T_up, T_down, mode, c_unit, T_up_unit, T_down_unit)
    # assert c_agg == 5.2
    # assert T_up_agg == 8.9175
    # assert T_down_agg == 84.4457