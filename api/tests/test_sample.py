import pytest

def test_sum():
    assert sum([1, 2, 3]) == 6

def f():
    raise SystemExit(1)

def test_system_exit():
    with pytest.raises(SystemExit):
        f()

class TestClass:
    def test_in_str(self):
        assert 'h' in 'this'

    def test_hasattr(self):
        x = 'hello'
        assert isinstance(x, str)

def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        10 / 1
