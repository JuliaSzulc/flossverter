"""
Converters colors in XYZ format.
"""
from typing import Sequence

import numpy as np


def xyz_to_lab(xyz: Sequence[float]) -> list[float]:
    """
    Converts XYZ coordinates to Lab using the standard illuminant D65 with 2° observer.

    Args:
        xyz (Sequence[float]): List or numpy array with XYZ coordinates (0-1).

    Returns:
        list[float]: List containing Lab coordinates.
    """
    XYZ_N = [0.95047, 1, 1.08883]
    EPSILON = 0.008856  # 216 / 24389
    KAPPA = 903.3  # 24389 / 27

    x_r, y_r, z_r = np.array(xyz) / XYZ_N

    def f(t: float) -> float:
        if t > EPSILON:
            return np.cbrt(t)
        else:
            return (KAPPA * t + 16) / 116

    L = 116 * f(y_r) - 16
    a = 500 * (f(x_r) - f(y_r))
    b = 200 * (f(y_r) - f(z_r))

    return [L, a, b]
