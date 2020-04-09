import pytest

# pytest -q test_pytest

def f():
    raise SystemExit(404)

def test_mytest():
    with pytest.raises(SystemExit):
        f()
