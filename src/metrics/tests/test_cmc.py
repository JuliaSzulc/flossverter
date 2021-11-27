import pytest
from numpy import sqrt
from pytest import approx

from src.metrics import _cmc, cmc_1_1, cmc_2_1


@pytest.mark.parametrize(
    "color_1, color_2, score",
    [
        ("orange", "blue", 126.335932),
        ("orange", "red", 28.775007),
        ("orange", "orange", 0),
    ],
)
def test_cmc_1_1(
    color_1: str, color_2: str, score: float, request: pytest.FixtureRequest
):
    color_1 = request.getfixturevalue(color_1)
    color_2 = request.getfixturevalue(color_2)

    result = sqrt(cmc_1_1(color_1, color_2))

    assert result == approx(score, abs=1e-3)
    assert result == sqrt(_cmc(color_1, color_2, unit_lc_ratio=True))


@pytest.mark.parametrize(
    "color_1, color_2, score",
    [
        ("orange", "blue", 125.147427),
        ("orange", "red", 20.209151),
        ("orange", "orange", 0),
    ],
)
def test_cmc_2_1(
    color_1: str, color_2: str, score: float, request: pytest.FixtureRequest
):
    color_1 = request.getfixturevalue(color_1)
    color_2 = request.getfixturevalue(color_2)

    result = sqrt(cmc_2_1(color_1, color_2))

    assert result == approx(score, abs=1e-3)
    assert result == sqrt(_cmc(color_1, color_2, unit_lc_ratio=False))
