from pytest import approx
import json
from numpy import sqrt

from metrics import *

# Reference values obtained using Bruce Justin Lindbloom calculator
# http://www.brucelindbloom.com/index.html?ColorDifferenceCalc.html

with open('test/colors.json', 'r') as f:
    COLORS = json.load(f)

BLUE = COLORS['blue']['hex']
RED = COLORS['red']['hex']
ORANGE = COLORS['orange']['hex']
BLACK = COLORS['black']['hex']
WHITE = COLORS['white']['hex']

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
    assert sqrt(cie76(ORANGE, BLUE)) == approx(142.297131, abs=1e-3)
    assert sqrt(cie76(ORANGE, RED)) == approx(38.606102, abs=1e-3)
    assert sqrt(cie76(ORANGE, ORANGE)) == 0
    assert sqrt(cie76(BLACK, WHITE)) == approx(100, abs=1e-3)


def test_cie94():
    assert sqrt(cie94(ORANGE, BLUE)) == approx(71.407307, abs=1e-3)
    assert sqrt(cie94(ORANGE, RED)) == approx(27.671121, abs=1e-3)
    assert sqrt(cie94(ORANGE, ORANGE)) == 0
    assert sqrt(cie94(BLACK, WHITE)) == approx(100, abs=1e-3)


def test_ciede2000():
    assert sqrt(ciede2000(ORANGE, BLUE)) == approx(55.732417, abs=1e-3)
    assert sqrt(ciede2000(ORANGE, RED)) == approx(25.189495, abs=1e-3)
    assert sqrt(ciede2000(ORANGE, ORANGE)) == 0
    assert sqrt(ciede2000(BLACK, WHITE)) == approx(100, abs=1e-3)


def test_cmc():
    # l:c = 1:1
    assert sqrt(cmc_1_1(ORANGE, BLUE)) == approx(126.335932, abs=1e-3)
    assert sqrt(cmc_1_1(ORANGE, RED)) == approx(28.775007, abs=1e-3)
    assert sqrt(cmc_1_1(ORANGE, ORANGE)) == 0

    # l:c = 2:1
    assert sqrt(cmc_2_1(ORANGE, BLUE)) == approx(125.147427, abs=1e-3)
    assert sqrt(cmc_2_1(ORANGE, RED)) == approx(20.209151, abs=1e-3)
    assert sqrt(cmc_2_1(ORANGE, ORANGE)) == 0
