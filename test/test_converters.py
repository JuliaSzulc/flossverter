import pytest
from numpy.testing import assert_allclose

from converters import *


# Reference values obtained using Bruce Justin Lindbloom calculator
# http://www.brucelindbloom.com/index.html?ColorCalculator.html

BLUE = '#2025c7'
RED = '6e1f0f'


def test_hex_to_dec_primaries():
    '''Test for hex_to_dec_primaries'''
    assert hex_to_dec_primaries(BLUE) == [32, 37, 199]
    assert_allclose(
        hex_to_dec_primaries(BLUE, arithmetic=True),
        [0.125490, 0.145098, 0.780392],
        atol=1e-6
    )

    assert hex_to_dec_primaries(RED) == [110, 31, 15]
    assert_allclose(
        hex_to_dec_primaries(RED, arithmetic=True),
        [0.431373, 0.121569, 0.058824],
        atol=1e-6
    )


def test_hex_to_xyz():
    '''Test for hex_to_xyz'''
    assert_allclose(
        hex_to_xyz(BLUE),
        [0.115625, 0.057523, 0.545227],
        atol=1e-6
    )

    assert_allclose(
        hex_to_xyz(RED),
        [0.070074, 0.043305, 0.009187],
        atol=1e-6
    )


def test_xyz_to_lab():
    '''Test for xyz_to_lab'''
    # BLUE
    assert_allclose(
        xyz_to_lab([0.115625, 0.057523, 0.545227]),
        [28.7787, 54.7349, -81.6143],
        atol=1e-4
    )

    # RED
    assert_allclose(
        xyz_to_lab([0.070074, 0.043305, 0.009187]),
        [24.7353, 34.0740, 29.5064],
        atol=1e-4
    )
