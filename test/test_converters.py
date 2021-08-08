from numpy.testing import assert_allclose
import json

from converters import *


# Reference values obtained using Bruce Justin Lindbloom calculator
# http://www.brucelindbloom.com/index.html?ColorCalculator.html

with open('test/colors.json', 'r') as f:
    COLORS = json.load(f)

BLUE = COLORS['blue']
RED = COLORS['red']

def test_hex_to_dec_primaries():
    '''Test for hex_to_dec_primaries'''
    assert hex_to_dec_primaries(BLUE['hex']) == BLUE['rgb']
    assert_allclose(
        hex_to_dec_primaries(BLUE['hex'], arithmetic=True),
        BLUE['rgb_ari']
    )

    assert hex_to_dec_primaries(RED['hex']) == RED['rgb']
    assert_allclose(
        hex_to_dec_primaries(RED['hex'], arithmetic=True),
        RED['rgb_ari']
    )


def test_hex_to_xyz():
    '''Test for hex_to_xyz'''
    assert_allclose(
        hex_to_xyz(BLUE['hex']),
        BLUE['xyz'],
        atol=1e-3
    )

    assert_allclose(
        hex_to_xyz(RED['hex']),
        RED['xyz'],
        atol=1e-3
    )


def test_xyz_to_lab():
    '''Test for xyz_to_lab'''
    # BLUE
    assert_allclose(
        xyz_to_lab(BLUE['xyz']),
        BLUE['lab'],
        atol=1e-3
    )

    # RED
    assert_allclose(
        xyz_to_lab(RED['xyz']),
        RED['lab'],
        atol=1e-3
    )


def test_lab_to_lch():
    '''Test for lab_to_lch'''
    # BLUE
    assert_allclose(
        lab_to_lch(BLUE['lab']),
        BLUE['lch'],
        atol=1e-3
    )

    # RED
    assert_allclose(
        lab_to_lch(RED['lab']),
        RED['lch'],
        atol=1e-3
    )
