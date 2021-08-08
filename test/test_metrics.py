from numpy.testing import assert_allclose
import json
from numpy import sqrt

from metrics import *

# Reference values obtained using Bruce Justin Lindbloom calculator
# http://www.brucelindbloom.com/index.html?ColorDifferenceCalc.html

with open('test/colors.json', 'r') as f:
    COLORS = json.load(f)

BLUE = COLORS['blue']
RED = COLORS['red']
ORANGE = COLORS['orange']

# def test_rgb_euclidean():
#     '''Test for rgb_euclidean'''
#     pass


# def test_rgb_gamma_correction():
#     '''Test for rgb_gamma_correction'''
#     pass


# def test_xyz_euclidean():
#     '''Test for xyz_euclidean'''
#     pass


def test_cie76():
    assert_allclose(
        sqrt(cie76(ORANGE['hex'], BLUE['hex'])),
        142.297131,
        atol=1e-3
    )
    
    assert_allclose(
        sqrt(cie76(ORANGE['hex'], RED['hex'])),
        38.606102,
        atol=1e-3
    )


def test_cie94():
    assert_allclose(
        sqrt(cie94(ORANGE['hex'], BLUE['hex'])),
        71.407307,
        atol=1e-3
    )
    
    assert_allclose(
        sqrt(cie94(ORANGE['hex'], RED['hex'])),
        27.671121,
        atol=1e-3
    )


def test_ciede2000():
    assert_allclose(
        sqrt(ciede2000(ORANGE['hex'], BLUE['hex'])),
        55.732417,
        atol=1e-3
    )
    
    assert_allclose(
        sqrt(ciede2000(ORANGE['hex'], RED['hex'])),
        25.189495,
        atol=1e-3
    )
