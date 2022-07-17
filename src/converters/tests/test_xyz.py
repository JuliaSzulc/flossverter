import pytest
from pytest import approx

from converters import xyz_to_lab


@pytest.mark.parametrize("color", ["red", "blue"])
def test_xyz_to_lab(color: str, request: pytest.FixtureRequest):
    color = request.getfixturevalue(color)

    assert xyz_to_lab(color.xyz) == approx(color.lab, abs=1e-3)
    assert xyz_to_lab(color.xyz) == approx(color.lab, abs=1e-3)
