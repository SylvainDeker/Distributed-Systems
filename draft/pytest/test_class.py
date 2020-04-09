class TestClass:
    """docstring for TestClass."""

    def test_one(self):
        x = "this"
        assert "w" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")
