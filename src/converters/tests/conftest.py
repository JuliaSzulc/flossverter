from dataclasses import dataclass

import pytest


@dataclass
class Color:
    """Data class keeping different representations of a color."""

    hexadec: str
    rgb: list[int]
    rgb_ari: list[float]
    xyz: list[float]
    lab: list[float]
    lch: list[float]


# Reference values obtained using Bruce Justin Lindbloom calculator
# http://www.brucelindbloom.com/index.html?ColorCalculator.html


@pytest.fixture
def blue() -> Color:
    c = Color(
        hexadec="2025c7",
        rgb=[32, 37, 199],
        rgb_ari=[0.1254902, 0.14509804, 0.78039216],
        xyz=[0.115625, 0.057523, 0.545227],
        lab=[28.7788, 54.7346, -81.6141],
        lch=[28.7788, 98.2687, 303.8478],
    )
    return c


@pytest.fixture
def red() -> Color:
    c = Color(
        hexadec="6e1f0f",
        rgb=[110, 31, 15],
        rgb_ari=[0.43137255, 0.12156863, 0.05882353],
        xyz=[0.070074, 0.043305, 0.009187],
        lab=[24.7353, 34.0741, 29.5059],
        lch=[24.7353, 45.0738, 40.8904],
    )
    return c
