import pytest


# Reference values obtained using Bruce Justin Lindbloom calculator
# http://www.brucelindbloom.com/index.html?ColorCalculator.html


@pytest.fixture
def blue() -> str:
    return "#2025c7"


@pytest.fixture
def red() -> str:
    return "#6e1f0f"


@pytest.fixture
def orange() -> str:
    return "#c25b08"


@pytest.fixture
def black() -> str:
    return "#000000"


@pytest.fixture
def white() -> str:
    return "#ffffff"
