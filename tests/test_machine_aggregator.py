import pytest
import numpy as np
from psepy.machine_aggregator import MachineAggregator

class TestMachineAggregator:
    def setup_method(self):
        self.aggregator = MachineAggregator()

    def test_aggregate_machines_parallel(self, sample_machine_data):
        result = self.aggregator.aggregate_machines(
            S=sample_machine_data['S'],
            c=sample_machine_data['c'],
            T_up=sample_machine_data['T_up'],
            T_down=sample_machine_data['T_down'],
            mode='parallel'
        )
        
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert all(isinstance(x, float) for x in result)

    def test_aggregate_machines_consecutive(self, sample_machine_data):
        result = self.aggregator.aggregate_machines(
            S=sample_machine_data['S'],
            c=sample_machine_data['c'],
            T_up=sample_machine_data['T_up'],
            T_down=sample_machine_data['T_down'],
            mode='consecutive dependent'
        )
        
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert all(isinstance(x, float) for x in result)

    def test_invalid_mode(self, sample_machine_data):
        with pytest.raises(ValueError):
            self.aggregator.aggregate_machines(
                S=sample_machine_data['S'],
                c=sample_machine_data['c'],
                T_up=sample_machine_data['T_up'],
                T_down=sample_machine_data['T_down'],
                mode='invalid'
            ) 