"""
Converters for RGB colors in hexadecimal format.
"""
from typing import Union

import numpy as np


def hex_to_dec_primaries(
    color: str, arithmetic: bool = False
) -> Union[list[int], list[float]]:
    """
    Splits hex color code into three decimal values of the primary colors.

    Args:
        color (str): Color code string (hex), can include '#' prefix
        arithmetic (bool, optional): If True returns float values between 0 and 1.
            Defaults to False.

    Returns:
        Union[list[int], list[float]]: List of three integers (0-255) or floats (0-1)
    """

    def to_dec(h):
        dec = int("0x" + h, 16)
        if arithmetic:
            dec /= 255
        return dec

    color = color.lstrip("#")
    return [to_dec(color[i : i + 2]) for i in range(0, len(color), 2)]


def hex_to_xyz(color: str) -> np.ndarray:
    """
    Converts standard RGB color code to XYZ coordinates.

    Uses the standard illuminant D65 with 2° observer.

    Args:
        color (str): Color code string (hex), can include '#' prefix

    Returns:
        np.ndarray[float]: 1x3 numpy array of float XYZ coordinates (0-1)
    """

    rgb = hex_to_dec_primaries(color, arithmetic=True)

    def to_lin(c):
        if c > 0.04045:
            A = 0.055
            return ((c + A) / (1 + A)) ** 2.4
        else:
            return c / 12.92

    rgb_lin = np.array([[to_lin(c)] for c in rgb])

    SRGB_MATRIX = np.array(
        [
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041],
        ]
    )
    xyz = np.matmul(SRGB_MATRIX, rgb_lin).flatten()

    return xyz
