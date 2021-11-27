"""
Converters for colors in LAB format.
"""
import numpy as np


def lab_to_lch(lab):
    """Converts Lab coordinates to LCHab.

    Args:
    - lab - list or numpy array with Lab coordinates

    Returns:
    List containing LCH coordinates with H expressed in degrees.
    """
    L, a, b = lab

    C = np.sqrt(a ** 2 + b ** 2)
    H = np.degrees(np.arctan2(b, a)) % 360

    return [L, C, H]
