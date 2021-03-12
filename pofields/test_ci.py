import pytest

@pytest.fixture
def random_string():
  return "wololoooooo"


def test_random_string(random_string):
  assert random_string == "wololoooooo"
