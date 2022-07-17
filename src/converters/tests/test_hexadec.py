import pytest
from pytest import approx

from converters import hex_to_dec_primaries, hex_to_xyz


@pytest.mark.parametrize("color", ["red", "blue"])
def test_hex_to_dec_primaries(color: str, request: pytest.FixtureRequest):
    color = request.getfixturevalue(color)

    assert hex_to_dec_primaries(color.hexadec) == color.rgb
    assert hex_to_dec_primaries(color.hexadec, arithmetic=True) == approx(color.rgb_ari)


@pytest.mark.parametrize("color", ["red", "blue"])
def test_hex_to_xyz(color: str, request: pytest.FixtureRequest):
    color = request.getfixturevalue(color)

    assert hex_to_xyz(color.hexadec) == approx(color.xyz, abs=1e-3)
