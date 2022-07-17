import pytest
from numpy import sqrt
from pytest import approx

from metrics import rgb_euclidean, rgb_euclidean_gamma_correction, xyz_euclidean


@pytest.mark.parametrize(
    "color_1, color_2, score",
    [
        ("orange", "blue", 256.205),
        ("orange", "red", 103.465),
        ("orange", "orange", 0),
        ("black", "white", 441.673),
    ],
)
def test_rgb_euclidean(
    color_1: str, color_2: str, score: float, request: pytest.FixtureRequest
):
    color_1 = request.getfixturevalue(color_1)
    color_2 = request.getfixturevalue(color_2)

    assert sqrt(rgb_euclidean(color_1, color_2)) == approx(score, abs=1e-3)


@pytest.mark.parametrize(
    "color_1, color_2, score",
    [
        ("orange", "blue", 416.647),
        ("orange", "red", 188.854),
        ("orange", "orange", 0),
        ("black", "white", 765),
    ],
)
def test_rgb_euclidean_gamma_correction(
    color_1: str, color_2: str, score: float, request: pytest.FixtureRequest
):
    color_1 = request.getfixturevalue(color_1)
    color_2 = request.getfixturevalue(color_2)

    assert sqrt(rgb_euclidean_gamma_correction(color_1, color_2)) == approx(
        score, abs=1e-3
    )


@pytest.mark.parametrize(
    "color_1, color_2, score",
    [
        ("orange", "blue", 0.556),
        ("orange", "red", 0.241),
        ("orange", "orange", 0),
        ("black", "white", 1.758),
    ],
)
def test_xyz_euclidean(
    color_1: str, color_2: str, score: float, request: pytest.FixtureRequest
):
    color_1 = request.getfixturevalue(color_1)
    color_2 = request.getfixturevalue(color_2)

    assert sqrt(xyz_euclidean(color_1, color_2)) == approx(score, abs=1e-3)
