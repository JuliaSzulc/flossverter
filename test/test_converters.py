from pytest import approx
import json

from src.converters import *


# Reference values obtained using Bruce Justin Lindbloom calculator
# http://www.brucelindbloom.com/index.html?ColorCalculator.html

with open('test/colors.json', 'r') as f:
    COLORS = json.load(f)

BLUE = COLORS['blue']
RED = COLORS['red']

def test_hex_to_dec_primaries():
    assert hex_to_dec_primaries(BLUE['hex']) == BLUE['rgb']
    assert hex_to_dec_primaries(BLUE['hex'], arithmetic=True) ==\
        approx(BLUE['rgb_ari'])
    assert hex_to_dec_primaries(RED['hex'], arithmetic=True) ==\
        approx(RED['rgb_ari'])


def test_hex_to_xyz():
    assert hex_to_xyz(BLUE['hex']) == approx(BLUE['xyz'], abs=1e-3)
    assert hex_to_xyz(RED['hex']) == approx(RED['xyz'], abs=1e-3)


def test_xyz_to_lab():
    assert xyz_to_lab(BLUE['xyz']) == approx(BLUE['lab'], abs=1e-3)
    assert xyz_to_lab(RED['xyz']) == approx(RED['lab'], abs=1e-3)


def test_lab_to_lch():
    assert lab_to_lch(BLUE['lab']) == approx(BLUE['lch'], abs=1e-3)
    assert lab_to_lch(RED['lab']) == approx(RED['lch'], abs=1e-3)
