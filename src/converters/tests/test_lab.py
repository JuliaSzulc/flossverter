import pytest
from pytest import approx

from converters import lab_to_lch


@pytest.mark.parametrize("color", ["red", "blue"])
def test_xyz_to_lab(color: str, request: pytest.FixtureRequest):
    color = request.getfixturevalue(color)

    assert lab_to_lch(color.lab) == approx(color.lch, abs=1e-3)
    assert lab_to_lch(color.lab) == approx(color.lch, abs=1e-3)
