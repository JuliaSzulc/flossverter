import pytest
from numpy import sqrt
from pytest import approx

from src.metrics import cie76, cie94, ciede2000


@pytest.mark.parametrize(
    "color_1, color_2, score",
    [
        ("orange", "blue", 142.297131),
        ("orange", "red", 38.606102),
        ("orange", "orange", 0),
        ("black", "white", 100),
    ],
)
def test_cie76(
    color_1: str, color_2: str, score: float, request: pytest.FixtureRequest
):
    color_1 = request.getfixturevalue(color_1)
    color_2 = request.getfixturevalue(color_2)

    assert sqrt(cie76(color_1, color_2)) == approx(score, abs=1e-3)


@pytest.mark.parametrize(
    "color_1, color_2, score",
    [
        ("orange", "blue", 71.407307),
        ("orange", "red", 27.671121),
        ("orange", "orange", 0),
        ("black", "white", 100),
    ],
)
def test_cie94(
    color_1: str, color_2: str, score: float, request: pytest.FixtureRequest
):
    color_1 = request.getfixturevalue(color_1)
    color_2 = request.getfixturevalue(color_2)

    assert sqrt(cie94(color_1, color_2)) == approx(score, abs=1e-3)


@pytest.mark.parametrize(
    "color_1, color_2, score",
    [
        ("orange", "blue", 55.732417),
        ("orange", "red", 25.189495),
        ("orange", "orange", 0),
        ("black", "white", 100),
    ],
)
def test_ciede2000(
    color_1: str, color_2: str, score: float, request: pytest.FixtureRequest
):
    color_1 = request.getfixturevalue(color_1)
    color_2 = request.getfixturevalue(color_2)

    assert sqrt(ciede2000(color_1, color_2)) == approx(score, abs=1e-3)
