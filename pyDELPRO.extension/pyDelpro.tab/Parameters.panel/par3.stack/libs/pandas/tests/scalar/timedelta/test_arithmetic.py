"""
Tests for scalar Timedelta arithmetic ops
"""
from datetime import datetime, timedelta
import operator

import numpy as np
import pytest

from pandas.compat.numpy import is_numpy_dev

import pandas as pd
from pandas import NaT, Timedelta, Timestamp, compat, offsets
import pandas._testing as tm
from pandas.core import ops


class TestTimedeltaAdditionSubtraction:
    """
    Tests for Timedelta methods:

        __add__, __radd__,
        __sub__, __rsub__
    """

    @pytest.mark.parametrize(
        "ten_seconds",
        [
            Timedelta(10, unit="s"),
            timedelta(seconds=10),
            np.timedelta64(10, "s"),
            np.timedelta64(10000000000, "ns"),
            offsets.Second(10),
        ],
    )
    def test_td_add_sub_ten_seconds(self, ten_seconds):
        # GH#6808
        base = Timestamp("20130101 09:01:12.123456")
        expected_add = Timestamp("20130101 09:01:22.123456")
        expected_sub = Timestamp("20130101 09:01:02.123456")

        result = base + ten_seconds
        assert result == expected_add

        result = base - ten_seconds
        assert result == expected_sub

    @pytest.mark.parametrize(
        "one_day_ten_secs",
        [
            Timedelta("1 day, 00:00:10"),
            Timedelta("1 days, 00:00:10"),
            timedelta(days=1, seconds=10),
            np.timedelta64(1, "D") + np.timedelta64(10, "s"),
            offsets.Day() + offsets.Second(10),
        ],
    )
    def test_td_add_sub_one_day_ten_seconds(self, one_day_ten_secs):
        # GH#6808
        base = Timestamp("20130102 09:01:12.123456")
        expected_add = Timestamp("20130103 09:01:22.123456")
        expected_sub = Timestamp("20130101 09:01:02.123456")

        result = base + one_day_ten_secs
        assert result == expected_add

        result = base - one_day_ten_secs
        assert result == expected_sub

    @pytest.mark.parametrize("op", [operator.add, ops.radd])
    def test_td_add_datetimelike_scalar(self, op):
        # GH#19738
        td = Timedelta(10, unit="d")

        result = op(td, datetime(2016, 1, 1))
        if op is operator.add:
            # datetime + Timedelta does _not_ call Timedelta.__radd__,
            # so we get a datetime back instead of a Timestamp
            assert isinstance(result, Timestamp)
        assert result == Timestamp(2016, 1, 11)

        result = op(td, Timestamp("2018-01-12 18:09"))
        assert isinstance(result, Timestamp)
        assert result == Timestamp("2018-01-22 18:09")

        result = op(td, np.datetime64("2018-01-12"))
        assert isinstance(result, Timestamp)
        assert result == Timestamp("2018-01-22")

        result = op(td, NaT)
        assert result is NaT

    def test_td_add_timestamp_overflow(self):
        msg = "int too (large|big) to convert"
        with pytest.raises(OverflowError, match=msg):
            Timestamp("1700-01-01") + Timedelta(13 * 19999, unit="D")

        with pytest.raises(OverflowError, match=msg):
            Timestamp("1700-01-01") + timedelta(days=13 * 19999)

    @pytest.mark.parametrize("op", [operator.add, ops.radd])
    def test_td_add_td(self, op):
        td = Timedelta(10, unit="d")

        result = op(td, Timedelta(days=10))
        assert isinstance(result, Timedelta)
        assert result == Timedelta(days=20)

    @pytest.mark.parametrize("op", [operator.add, ops.radd])
    def test_td_add_pytimedelta(self, op):
        td = Timedelta(10, unit="d")
        result = op(td, timedelta(days=9))
        assert isinstance(result, Timedelta)
        assert result == Timedelta(days=19)

    @pytest.mark.parametrize("op", [operator.add, ops.radd])
    def test_td_add_timedelta64(self, op):
        td = Timedelta(10, unit="d")
        result = op(td, np.timedelta64(-4, "D"))
        assert isinstance(result, Timedelta)
        assert result == Timedelta(days=6)

    @pytest.mark.parametrize("op", [operator.add, ops.radd])
    def test_td_add_offset(self, op):
        td = Timedelta(10, unit="d")

        result = op(td, offsets.Hour(6))
        assert isinstance(result, Timedelta)
        assert result == Timedelta(days=10, hours=6)

    def test_td_sub_td(self):
        td = Timedelta(10, unit="d")
        expected = Timedelta(0, unit="ns")
        result = td - td
        assert isinstance(result, Timedelta)
        assert result == expected

    def test_td_sub_pytimedelta(self):
        td = Timedelta(10, unit="d")
        expected = Timedelta(0, unit="ns")

        result = td - td.to_pytimedelta()
        assert isinstance(result, Timedelta)
        assert result == expected

        result = td.to_pytimedelta() - td
        assert isinstance(result, Timedelta)
        assert result == expected

    def test_td_sub_timedelta64(self):
        td = Timedelta(10, unit="d")
        expected = Timedelta(0, unit="ns")

        result = td - td.to_timedelta64()
        assert isinstance(result, Timedelta)
        assert result == expected

        result = td.to_timedelta64() - td
        assert isinstance(result, Timedelta)
        assert result == expected

    def test_td_sub_nat(self):
        # In this context pd.NaT is treated as timedelta-like
        td = Timedelta(10, unit="d")
        result = td - NaT
        assert result is NaT

    def test_td_sub_td64_nat(self):
        td = Timedelta(10, unit="d")
        td_nat = np.timedelta64("NaT")

        result = td - td_nat
        assert result is NaT

        result = td_nat - td
        assert result is NaT

    def test_td_sub_offset(self):
        td = Timedelta(10, unit="d")
        result = td - offsets.Hour(1)
        assert isinstance(result, Timedelta)
        assert result == Timedelta(239, unit="h")

    def test_td_add_sub_numeric_raises(self):
        td = Timedelta(10, unit="d")
        msg = "unsupported operand type"
        for other in [2, 2.0, np.int64(2), np.float64(2)]:
            with pytest.raises(TypeError, match=msg):
                td + other
            with pytest.raises(TypeError, match=msg):
                other + td
            with pytest.raises(TypeError, match=msg):
                td - other
            with pytest.raises(TypeError, match=msg):
                other - td

    def test_td_rsub_nat(self):
        td = Timedelta(10, unit="d")
        result = NaT - td
        assert result is NaT

        result = np.datetime64("NaT") - td
        assert result is NaT

    def test_td_rsub_offset(self):
        result = offsets.Hour(1) - Timedelta(10, unit="d")
        assert isinstance(result, Timedelta)
        assert result == Timedelta(-239, unit="h")

    def test_td_sub_timedeltalike_object_dtype_array(self):
        # GH#21980
        arr = np.array([Timestamp("20130101 9:01"), Timestamp("20121230 9:02")])
        exp = np.array([Timestamp("20121231 9:01"), Timestamp("20121229 9:02")])
        res = arr - Timedelta("1D")
        tm.assert_numpy_array_equal(res, exp)

    def test_td_sub_mixed_most_timedeltalike_object_dtype_array(self):
        # GH#21980
        now = Timestamp.now()
        arr = np.array([now, Timedelta("1D"), np.timedelta64(2, "h")])
        exp = np.array(
            [
                now - Timedelta("1D"),
                Timedelta("0D"),
                np.timedelta64(2, "h") - Timedelta("1D"),
            ]
        )
        res = arr - Timedelta("1D")
        tm.assert_numpy_array_equal(res, exp)

    def test_td_rsub_mixed_most_timedeltalike_object_dtype_array(self):
        # GH#21980
        now = Timestamp.now()
        arr = np.array([now, Timedelta("1D"), np.timedelta64(2, "h")])
        msg = r"unsupported operand type\(s\) for \-: 'Timedelta' and 'Timestamp'"
        with pytest.raises(TypeError, match=msg):
            Timedelta("1D") - arr

    @pytest.mark.parametrize("op", [operator.add, ops.radd])
    def test_td_add_timedeltalike_object_dtype_array(self, op):
        # GH#21980
        arr = np.array([Timestamp("20130101 9:01"), Timestamp("20121230 9:02")])
        exp = np.array([Timestamp("20130102 9:01"), Timestamp("20121231 9:02")])
        res = op(arr, Timedelta("1D"))
        tm.assert_numpy_array_equal(res, exp)

    @pytest.mark.parametrize("op", [operator.add, ops.radd])
    def test_td_add_mixed_timedeltalike_object_dtype_array(self, op):
        # GH#21980
        now = Timestamp.now()
        arr = np.array([now, Timedelta("1D")])
        exp = np.array([now + Timedelta("1D"), Timedelta("2D")])
        res = op(arr, Timedelta("1D"))
        tm.assert_numpy_array_equal(res, exp)

    # TODO: moved from index tests following #24365, may need de-duplication
    def test_ops_ndarray(self):
        td = Timedelta("1 day")

        # timedelta, timedelta
        other = pd.to_timedelta(["1 day"]).values
        expected = pd.to_timedelta(["2 days"]).values
        tm.assert_numpy_array_equal(td + other, expected)
        tm.assert_numpy_array_equal(other + td, expected)
        msg = r"unsupported operand type\(s\) for \+: 'Timedelta' and 'int'"
        with pytest.raises(TypeError, match=msg):
            td + np.array([1])
        msg = (
            r"unsupported operand type\(s\) for \+: 'numpy.ndarray' and 'Timedelta'|"
            "Concatenation operation is not implemented for NumPy arrays"
        )
        with pytest.raises(TypeError, match=msg):
            np.array([1]) + td

        expected = pd.to_timedelta(["0 days"]).values
        tm.assert_numpy_array_equal(td - other, expected)
        tm.assert_numpy_array_equal(-other + td, expected)
        msg = r"unsupported operand type\(s\) for -: 'Timedelta' and 'int'"
        with pytest.raises(TypeError, match=msg):
            td - np.array([1])
        msg = r"unsupported operand type\(s\) for -: 'numpy.ndarray' and 'Timedelta'"
        with pytest.raises(TypeError, match=msg):
            np.array([1]) - td

        expected = pd.to_timedelta(["2 days"]).values
        tm.assert_numpy_array_equal(td * np.array([2]), expected)
        tm.assert_numpy_array_equal(np.array([2]) * td, expected)
        msg = (
            "ufunc '?multiply'? cannot use operands with types "
            r"dtype\('<m8\[ns\]'\) and dtype\('<m8\[ns\]'\)"
        )
        with pytest.raises(TypeError, match=msg):
            td * other
        with pytest.raises(TypeError, match=msg):
            other * td

        tm.assert_numpy_array_equal(td / other, np.array([1], dtype=np.float64))
        tm.assert_numpy_array_equal(other / td, np.array([1], dtype=np.float64))

        # timedelta, datetime
        other = pd.to_datetime(["2000-01-01"]).values
        expected = pd.to_datetime(["2000-01-02"]).values
        tm.assert_numpy_array_equal(td + other, expected)
        tm.assert_numpy_array_equal(other + td, expected)

        expected = pd.to_datetime(["1999-12-31"]).values
        tm.assert_numpy_array_equal(-td + other, expected)
        tm.assert_numpy_array_equal(other - td, expected)


class TestTimedeltaMultiplicationDivision:
    """
    Tests for Timedelta methods:

        __mul__, __rmul__,
        __div__, __rdiv__,
        __truediv__, __rtruediv__,
        __floordiv__, __rfloordiv__,
        __mod__, __rmod__,
        __divmod__, __rdivmod__
    """

    # ---------------------------------------------------------------
    # Timedelta.__mul__, __rmul__

    @pytest.mark.parametrize(
        "td_nat", [NaT, np.timedelta64("NaT", "ns"), np.timedelta64("NaT")]
    )
    @pytest.mark.parametrize("op", [operator.mul, ops.rmul])
    def test_td_mul_nat(self, op, td_nat):
        # GH#19819
        td = Timedelta(10, unit="d")
        typs = "|".join(["numpy.timedelta64", "NaTType", "Timedelta"])
        msg = "|".join(
            [
                rf"unsupported operand type\(s\) for \*: '{typs}' and '{typs}'",
                r"ufunc '?multiply'? cannot use operands with types",
            ]
        )
        with pytest.raises(TypeError, match=msg):
            op(td, td_nat)

    @pytest.mark.parametrize("nan", [np.nan, np.float64("NaN"), float("nan")])
    @pytest.mark.parametrize("op", [operator.mul, ops.rmul])
    def test_td_mul_nan(self, op, nan):
        # np.float64('NaN') has a 'dtype' attr, avoid treating as array
        td = Timedelta(10, unit="d")
        result = op(td, nan)
        assert result is NaT

    @pytest.mark.parametrize("op", [operator.mul, ops.rmul])
    def test_td_mul_scalar(self, op):
        # GH#19738
        td = Timedelta(minutes=3)

        result = op(td, 2)
        assert result == Timedelta(minutes=6)

        result = op(td, 1.5)
        assert result == Timedelta(minutes=4, seconds=30)

        assert op(td, np.nan) is NaT

        assert op(-1, td).value == -1 * td.value
        assert op(-1.0, td).value == -1.0 * td.value

        msg = "unsupported operand type"
        with pytest.raises(TypeError, match=msg):
            # timedelta * datetime is gibberish
            op(td, Timestamp(2016, 1, 2))

        with pytest.raises(TypeError, match=msg):
            # invalid multiply with another timedelta
            op(td, td)

    # ---------------------------------------------------------------
    # Timedelta.__div__, __truediv__

    def test_td_div_timedeltalike_scalar(self):
        # GH#19738
        td = Timedelta(10, unit="d")

        result = td / offsets.Hour(1)
        assert result == 240

        assert td / td == 1
        assert td / np.timedelta64(60, "h") == 4

        assert np.isnan(td / NaT)

    def test_td_div_td64_non_nano(self):

        # truediv
        td = Timedelta("1 days 2 hours 3 ns")
        result = td / np.timedelta64(1, "D")
        assert result == td.value / float(86400 * 1e9)
        result = td / np.timedelta64(1, "s")
        assert result == td.value / float(1e9)
        result = td / np.timedelta64(1, "ns")
        assert result == td.value

        # floordiv
        td = Timedelta("1 days 2 hours 3 ns")
        result = td // np.timedelta64(1, "D")
        assert result == 1
        result = td // np.timedelta64(1, "s")
        assert result == 93600
        result = td // np.timedelta64(1, "ns")
        assert result == td.value

    def test_td_div_numeric_scalar(self):
        # GH#19738
        td = Timedelta(10, unit="d")

        result = td / 2
        assert isinstance(result, Timedelta)
        assert result == Timedelta(days=5)

        result = td / 5.0
        assert isinstance(result, Timedelta)
        assert result == Timedelta(days=2)

    @pytest.mark.parametrize(
        "nan",
        [
            np.nan,
            pytest.param(
                np.float64("NaN"),
                marks=pytest.mark.xfail(
                    # Works on numpy dev only in python 3.9
                    is_numpy_dev and not compat.PY39,
                    raises=RuntimeWarning,
                    reason="https://github.com/pandas-dev/pandas/issues/31992",
                ),
            ),
            float("nan"),
        ],
    )
    def test_td_div_nan(self, nan):
        # np.float64('NaN') has a 'dtype' attr, avoid treating as array
        td = Timedelta(10, unit="d")
        result = td / nan
        assert result is NaT

        result = td // nan
        assert result is NaT

    # ---------------------------------------------------------------
    # Timedelta.__rdiv__

    def test_td_rdiv_timedeltalike_scalar(self):
        # GH#19738
        td = Timedelta(10, unit="d")
        result = offsets.Hour(1) / td
        assert result == 1 / 240.0

        assert np.timedelta64(60, "h") / td == 0.25

    def test_td_rdiv_na_scalar(self):
        # GH#31869 None gets cast to NaT
        td = Timedelta(10, unit="d")

        result = NaT / td
        assert np.isnan(result)

        result = None / td
        assert np.isnan(result)

        result = np.timedelta64("NaT") / td
        assert np.isnan(result)

        msg = r"unsupported operand type\(s\) for /: 'numpy.datetime64' and 'Timedelta'"
        with pytest.raises(TypeError, match=msg):
            np.datetime64("NaT") / td

        msg = r"unsupported operand type\(s\) for /: 'float' and 'Timedelta'"
        with pytest.raises(TypeError, match=msg):
            np.nan / td

    def test_td_rdiv_ndarray(self):
        td = Timedelta(10, unit="d")

        arr = np.array([td], dtype=object)
        result = arr / td
        expected = np.array([1], dtype=np.float64)
        tm.assert_numpy_array_equal(result, expected)

        arr = np.array([None])
        result = arr / td
        expected = np.array([np.nan])
        tm.assert_numpy_array_equal(result, expected)

        arr = np.array([np.nan], dtype=object)
        msg = r"unsupported operand type\(s\) for /: 'float' and 'Timedelta'"
        with pytest.raises(TypeError, match=msg):
            arr / td

        arr = np.array([np.nan], dtype=np.float64)
        msg = "cannot use operands with types dtype"
        with pytest.raises(TypeError, match=msg):
            arr / td

    # ---------------------------------------------------------------
    # Timedelta.__floordiv__

    def test_td_floordiv_timedeltalike_scalar(self):
        # GH#18846
        td = Timedelta(hours=3, minutes=4)
        scalar = Timedelta(hours=3, minutes=3)

        assert td // scalar == 1
        assert -td // scalar.to_pytimedelta() == -2
        assert (2 * td) // scalar.to_timedelta64() == 2

    def test_td_floordiv_null_scalar(self):
        # GH#18846
        td = Timedelta(hours=3, minutes=4)

        assert td // np.nan is NaT
        assert np.isnan(td // NaT)
        assert np.isnan(td // np.timedelta64("NaT"))

    def test_td_floordiv_offsets(self):
        # GH#19738
        td = Timedelta(hours=3, minutes=4)
        assert td // offsets.Hour(1) == 3
        assert td // offsets.Minute(2) == 92

    def test_td_floordiv_invalid_scalar(self):
        # GH#18846
        td = Timedelta(hours=3, minutes=4)

        msg = "|".join(
            [
                r"Invalid dtype datetime64\[D\] for __floordiv__",
                "'dtype' is an invalid keyword argument for this function",
                r"ufunc '?floor_divide'? cannot use operands with types",
            ]
        )
        with pytest.raises(TypeError, match=msg):
            td // np.datetime64("2016-01-01", dtype="datetime64[us]")

    def test_td_floordiv_numeric_scalar(self):
        # GH#18846
        td = Timedelta(hours=3, minutes=4)

        expected = Timedelta(hours=1, minutes=32)
        assert td // 2 == expected
        assert td // 2.0 == expected
        assert td // np.float64(2.0) == expected
        assert td // np.int32(2.0) == expected
        assert td // np.uint8(2.0) == expected

    def test_td_floordiv_timedeltalike_array(self):
        # GH#18846
        td = Timedelta(hours=3, minutes=4)
        scalar = Timedelta(hours=3, minutes=3)

        # Array-like others
        assert td // np.array(scalar.to_timedelta64()) == 1

        res = (3 * td) // np.array([scalar.to_timedelta64()])
        expected = np.array([3], dtype=np.int64)
        tm.assert_numpy_array_equal(res, expected)

        res = (10 * td) // np.array([scalar.to_timedelta64(), np.timedelta64("NaT")])
        expected = np.array([10, np.nan])
        tm.assert_numpy_array_equal(res, expected)

    def test_td_floordiv_numeric_series(self):
        # GH#18846
        td = Timedelta(hours=3, minutes=4)
        ser = pd.Series([1], dtype=np.int64)
        res = td // ser
        assert res.dtype.kind == "m"

    # ---------------------------------------------------------------
    # Timedelta.__rfloordiv__

    def test_td_rfloordiv_timedeltalike_scalar(self):
        # GH#18846
        td = Timedelta(hours=3, minutes=3)
        scalar = Timedelta(hours=3, minutes=4)

        # scalar others
        # x // Timedelta is defined only for timedelta-like x. int-like,
        # float-like, and date-like, in particular, should all either
        # a) raise TypeError directly or
        # b) return NotImplemented, following which the reversed
        #    operation will raise TypeError.
        assert td.__rfloordiv__(scalar) == 1
        assert (-td).__rfloordiv__(scalar.to_pytimedelta()) == -2
        assert (2 * td).__rfloordiv__(scalar.to_timedelta64()) == 0

    def test_td_rfloordiv_null_scalar(self):
        # GH#18846
        td = Timedelta(hours=3, minutes=3)

        assert np.isnan(td.__rfloordiv__(NaT))
        assert np.isnan(td.__rfloordiv__(np.timedelta64("NaT")))

    def test_td_rfloordiv_offsets(self):
        # GH#19738
        assert offsets.Hour(1) // Timedelta(minutes=25) == 2

    def test_td_rfloordiv_invalid_scalar(self):
        # GH#18846
        td = Timedelta(hours=3, minutes=3)

        dt64 = np.datetime64("2016-01-01", "us")

        assert td.__rfloordiv__(dt64) is NotImplemented

        msg = (
            r"unsupported operand type\(s\) for //: 'numpy.datetime64' and 'Timedelta'"
        )
        with pytest.raises(TypeError, match=msg):
            dt64 // td

    def test_td_rfloordiv_numeric_scalar(self):
        # GH#18846
        td = Timedelta(hours=3, minutes=3)

        assert td.__rfloordiv__(np.nan) is NotImplemented
        assert td.__rfloordiv__(3.5) is NotImplemented
        assert td.__rfloordiv__(2) is NotImplemented
        assert td.__rfloordiv__(np.float64(2.0)) is NotImplemented
        assert td.__rfloordiv__(np.uint8(9)) is NotImplemented
        assert td.__rfloordiv__(np.int32(2.0)) is NotImplemented

        msg = r"unsupported operand type\(s\) for //: '.*' and 'Timedelta"
        with pytest.raises(TypeError, match=msg):
            np.float64(2.0) // td
        with pytest.raises(TypeError, match=msg):
            np.uint8(9) // td
        with pytest.raises(TypeError, match=msg):
            # deprecated GH#19761, enforced GH#29797
            np.int32(2.0) // td

    def test_td_rfloordiv_timedeltalike_array(self):
        # GH#18846
        td = Timedelta(hours=3, minutes=3)
        scalar = Timedelta(hours=3, minutes=4)

        # Array-like others
        assert td.__rfloordiv__(np.array(scalar.to_timedelta64())) == 1

        res = td.__rfloordiv__(np.array([(3 * scalar).to_timedelta64()]))
        expected = np.array([3], dtype=np.int64)
        tm.assert_numpy_array_equal(res, expected)

        arr = np.array([(10 * scalar).to_timedelta64(), np.timedelta64("NaT")])
        res = td.__rfloordiv__(arr)
        expected = np.array([10, np.nan])
        tm.assert_numpy_array_equal(res, expected)

    def test_td_rfloordiv_intarray(self):
        # deprecated GH#19761, enforced GH#29797
        ints = np.array([1349654400, 1349740800, 1349827200, 1349913600]) * 10 ** 9

        msg = "Invalid dtype"
        with pytest.raises(TypeError, match=msg):
            ints // Timedelta(1, unit="s")

    def test_td_rfloordiv_numeric_series(self):
        # GH#18846
        td = Timedelta(hours=3, minutes=3)
        ser = pd.Series([1], dtype=np.int64)
        res = td.__rfloordiv__(ser)
        assert res is NotImplemented

        msg = "Invalid dtype"
        with pytest.raises(TypeError, match=msg):
            # Deprecated GH#19761, enforced GH#29797
            ser // td

    # ----------------------------------------------------------------
    # Timedelta.__mod__, __rmod__

    def test_mod_timedeltalike(self):
        # GH#19365
        td = Timedelta(hours=37)

        # Timedelta-like others
        result = td % Timedelta(hours=6)
        assert isinstance(result, Timedelta)
        assert result == Timedelta(hours=1)

        result = td % timedelta(minutes=60)
        assert isinstance(result, Timedelta)
        assert result == Timedelta(0)

        result = td % NaT
        assert result is NaT

    def test_mod_timedelta64_nat(self):
        # GH#19365
        td = Timedelta(hours=37)

        result = td % np.timedelta64("NaT", "ns")
        assert result is NaT

    def test_mod_timedelta64(self):
        # GH#19365
        td = Timedelta(hours=37)

        result = td % np.timedelta64(2, "h")
        assert isinstance(result, Timedelta)
        assert result == Timedelta(hours=1)

    def test_mod_offset(self):
        # GH#19365
        td = Timedelta(hours=37)

        result = td % offsets.Hour(5)
        assert isinstance(result, Timedelta)
        assert result == Timedelta(hours=2)

    def test_mod_numeric(self):
        # GH#19365
        td = Timedelta(hours=37)

        # Numeric Others
        result = td % 2
        assert isinstance(result, Timedelta)
        assert result == Timedelta(0)

        result = td % 1e12
        assert isinstance(result, Timedelta)
        assert result == Timedelta(minutes=3, seconds=20)

        result = td % int(1e12)
        assert isinstance(result, Timedelta)
        assert result == Timedelta(minutes=3, seconds=20)

    def test_mod_invalid(self):
        # GH#19365
        td = Timedelta(hours=37)
        msg = "unsupported operand type"
        with pytest.raises(TypeError, match=msg):
            td % Timestamp("2018-01-22")

        with pytest.raises(TypeError, match=msg):
            td % []

    def test_rmod_pytimedelta(self):
        # GH#19365
        td = Timedelta(minutes=3)

        result = timedelta(minutes=4) % td
        assert isinstance(result, Timedelta)
        assert result == Timedelta(minutes=1)

    def test_rmod_timedelta64(self):
        # GH#19365
        td = Timedelta(minutes=3)
        result = np.timedelta64(5, "m") % td
        assert isinstance(result, Timedelta)
        assert result == Timedelta(minutes=2)

    def test_rmod_invalid(self):
        # GH#19365
        td = Timedelta(minutes=3)

        msg = "unsupported operand"
        with pytest.raises(TypeError, match=msg):
            Timestamp("2018-01-22") % td

        with pytest.raises(TypeError, match=msg):
            15 % td

        with pytest.raises(TypeError, match=msg):
            16.0 % td

        msg = "Invalid dtype int"
        with pytest.raises(TypeError, match=msg):
            np.array([22, 24]) % td

    # ----------------------------------------------------------------
    # Timedelta.__divmod__, __rdivmod__

    def test_divmod_numeric(self):
        # GH#19365
        td = Timedelta(days=2, hours=6)

        result = divmod(td, 53 * 3600 * 1e9)
        assert result[0] == Timedelta(1, unit="ns")
        assert isinstance(result[1], Timedelta)
        assert result[1] == Timedelta(hours=1)

        assert result
        result = divmod(td, np.nan)
        assert result[0] is NaT
        assert result[1] is NaT

    def test_divmod(self):
        # GH#19365
        td = Timedelta(days=2, hours=6)

        result = divmod(td, timedelta(days=1))
        assert result[0] == 2
        assert isinstance(result[1], Timedelta)
        assert result[1] == Timedelta(hours=6)

        result = divmod(td, 54)
        assert result[0] == Timedelta(hours=1)
        assert isinstance(result[1], Timedelta)
        assert result[1] == Timedelta(0)

        result = divmod(td, NaT)
        assert np.isnan(result[0])
        assert result[1] is NaT

    def test_divmod_offset(self):
        # GH#19365
        td = Timedelta(days=2, hours=6)

        result = divmod(td, offsets.Hour(-4))
        assert result[0] == -14
        assert isinstance(result[1], Timedelta)
        assert result[1] == Timedelta(hours=-2)

    def test_divmod_invalid(self):
        # GH#19365
        td = Timedelta(days=2, hours=6)

        msg = r"unsupported operand type\(s\) for //: 'Timedelta' and 'Timestamp'"
        with pytest.raises(TypeError, match=msg):
            divmod(td, Timestamp("2018-01-22"))

    def test_rdivmod_pytimedelta(self):
        # GH#19365
        result = divmod(timedelta(days=2, hours=6), Timedelta(days=1))
        assert result[0] == 2
        assert isinstance(result[1], Timedelta)
        assert result[1] == Timedelta(hours=6)

    def test_rdivmod_offset(self):
        result = divmod(offsets.Hour(54), Timedelta(hours=-4))
        assert result[0] == -14
        assert isinstance(result[1], Timedelta)
        assert result[1] == Timedelta(hours=-2)

    def test_rdivmod_invalid(self):
        # GH#19365
        td = Timedelta(minutes=3)
        msg = "unsupported operand type"

        with pytest.raises(TypeError, match=msg):
            divmod(Timestamp("2018-01-22"), td)

        with pytest.raises(TypeError, match=msg):
            divmod(15, td)

        with pytest.raises(TypeError, match=msg):
            divmod(16.0, td)

        msg = "Invalid dtype int"
        with pytest.raises(TypeError, match=msg):
            divmod(np.array([22, 24]), td)

    # ----------------------------------------------------------------

    @pytest.mark.parametrize(
        "op", [operator.mul, ops.rmul, operator.truediv, ops.rdiv, ops.rsub]
    )
    @pytest.mark.parametrize(
        "arr",
        [
            np.array([Timestamp("20130101 9:01"), Timestamp("20121230 9:02")]),
            np.array([Timestamp.now(), Timedelta("1D")]),
        ],
    )
    def test_td_op_timedelta_timedeltalike_array(self, op, arr):
        msg = "unsupported operand type|cannot use operands with types"
        with pytest.raises(TypeError, match=msg):
            op(arr, Timedelta("1D"))


class TestTimedeltaComparison:
    def test_compare_tick(self, tick_classes):
        cls = tick_classes

        off = cls(4)
        td = off.delta
        assert isinstance(td, Timedelta)

        assert td == off
        assert not td != off
        assert td <= off
        assert td >= off
        assert not td < off
        assert not td > off

        assert not td == 2 * off
        assert td != 2 * off
        assert td <= 2 * off
        assert td < 2 * off
        assert not td >= 2 * off
        assert not td > 2 * off

    def test_comparison_object_array(self):
        # analogous to GH#15183
        td = Timedelta("2 days")
        other = Timedelta("3 hours")

        arr = np.array([other, td], dtype=object)
        res = arr == td
        expected = np.array([False, True], dtype=bool)
        assert (res == expected).all()

        # 2D case
        arr = np.array([[other, td], [td, other]], dtype=object)
        res = arr != td
        expected = np.array([[True, False], [False, True]], dtype=bool)
        assert res.shape == expected.shape
        assert (res == expected).all()

    def test_compare_timedelta_ndarray(self):
        # GH#11835
        periods = [Timedelta("0 days 01:00:00"), Timedelta("0 days 01:00:00")]
        arr = np.array(periods)
        result = arr[0] > arr
        expected = np.array([False, False])
        tm.assert_numpy_array_equal(result, expected)

    def test_compare_td64_ndarray(self):
        # GG#33441
        arr = np.arange(5).astype("timedelta64[ns]")
        td = Timedelta(arr[1])

        expected = np.array([False, True, False, False, False], dtype=bool)

        result = td == arr
        tm.assert_numpy_array_equal(result, expected)

        result = arr == td
        tm.assert_numpy_array_equal(result, expected)

        result = td != arr
        tm.assert_numpy_array_equal(result, ~expected)

        result = arr != td
        tm.assert_numpy_array_equal(result, ~expected)

    @pytest.mark.skip(reason="GH#20829 is reverted until after 0.24.0")
    def test_compare_custom_object(self):
        """
        Make sure non supported operations on Timedelta returns NonImplemented
        and yields to other operand (GH#20829).
        """

        class CustomClass:
            def __init__(self, cmp_result=None):
                self.cmp_result = cmp_result

            def generic_result(self):
                if self.cmp_result is None:
                    return NotImplemented
                else:
                    return self.cmp_result

            def __eq__(self, other):
                return self.generic_result()

            def __gt__(self, other):
                return self.generic_result()

        t = Timedelta("1s")

        assert not (t == "string")
        assert not (t == 1)
        assert not (t == CustomClass())
        assert not (t == CustomClass(cmp_result=False))

        assert t < CustomClass(cmp_result=True)
        assert not (t < CustomClass(cmp_result=False))

        assert t == CustomClass(cmp_result=True)

    @pytest.mark.parametrize("val", ["string", 1])
    def test_compare_unknown_type(self, val):
        # GH#20829
        t = Timedelta("1s")
        msg = "not supported between instances of 'Timedelta' and '(int|str)'"
        with pytest.raises(TypeError, match=msg):
            t >= val
        with pytest.raises(TypeError, match=msg):
            t > val
        with pytest.raises(TypeError, match=msg):
            t <= val
        with pytest.raises(TypeError, match=msg):
            t < val


def test_ops_notimplemented():
    class Other:
        pass

    other = Other()

    td = Timedelta("1 day")
    assert td.__add__(other) is NotImplemented
    assert td.__sub__(other) is NotImplemented
    assert td.__truediv__(other) is NotImplemented
    assert td.__mul__(other) is NotImplemented
    assert td.__floordiv__(other) is NotImplemented


def test_ops_error_str():
    # GH#13624
    td = Timedelta("1 day")

    for left, right in [(td, "a"), ("a", td)]:

        msg = "|".join(
            [
                "unsupported operand type",
                r'can only concatenate str \(not "Timedelta"\) to str',
                "must be str, not Timedelta",
            ]
        )
        with pytest.raises(TypeError, match=msg):
            left + right

        msg = "not supported between instances of"
        with pytest.raises(TypeError, match=msg):
            left > right

        assert not left == right
        assert left != right