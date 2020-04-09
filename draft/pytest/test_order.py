import pytest

# fixtures documentation order example
order = []


@pytest.fixture(scope="session")
def s1():
    order.append("s1")


@pytest.fixture(scope="module")
def m1():
    order.append("m1")


@pytest.fixture
def f1(f3): # f3 is also a fixture
    order.append("f1")


@pytest.fixture
def f3():
    order.append("f3")

# Autouse fixtures will be instantiated before explicitly used fixtures.
@pytest.fixture(autouse=True)
def a1():
    order.append("a1")


@pytest.fixture
def f2():
    order.append("f2")


def test_order(f1, m1, f2, s1):
    assert order == ["s1", "m1", "a1", "f3", "f1", "f2"]


# s1: is the highest-scoped fixture (session).
# m1: is the second highest-scoped fixture (module).
# a1: is a function-scoped autouse fixture: it will be instantiated before other fixtures within the same scope.
# f3: is a function-scoped fixture, required by f1: it needs to be instantiated at this point
# f1: is the first function-scoped fixture in test_order parameter list.
# f2: is the last function-scoped fixture in test_order parameter list.
