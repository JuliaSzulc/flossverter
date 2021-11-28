import pytest
from numpy import sqrt
from pytest import approx

from src.metrics import squared_euclidean
from src.metrics.helpers import Coordinates


@pytest.mark.parametrize(
    "first, second, result",
    [
        ((2.3, 1.5, 6), (0, 1.1, -5), 11.245),
        ([1, 2], [-3, -2], 5.657),
        ([1], [-9], 10),
        ((1, 1, 1), (1, 1, 1), 0),
        ((), (), 0),
    ],
)
def test_euclidean_without_weights(
    first: Coordinates, second: Coordinates, result: float
):
    assert sqrt(squared_euclidean(first, second)) == approx(result, abs=1e-3)
