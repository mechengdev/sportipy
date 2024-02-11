import pytest

from sportipy import utils


class TestMsToMinPerKm:
    @pytest.mark.parametrize("input_, output", [
        (0, 0),
        (60, 0.2777777777777778),
        (5.5, 3.0303030303030303)
    ])
    def test_positive_value(self, input_, output):
        assert utils.ms_to_min_per_km(input_) == output

    def test_negative_value(self):
        with pytest.raises(ValueError):
            utils.ms_to_min_per_km(-12.1)
