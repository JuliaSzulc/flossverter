"""
Metrics using CMC standard.
"""
import numpy as np

from src.converters import hex_to_xyz, lab_to_lch, xyz_to_lab


def _cmc(base: str, other: str, unit_lc_ratio: bool = True) -> float:
    """
    Calculates squared delta E according to CMC l:c standard.

    Accepted inputs are colors in hexadecimal format (e.g. '#ff0000', '124f05').

    Args:
        base (str): string with hex code of the base color.
        other (str): string with hex code of the compared color.
        unit_lc_ratio (bool, optional): If true l:c=1:1 (imperceptibility), otherwise
            l:c=2:1 (acceptability). Defaults to True.

    Returns:
        float: Calculated score (squared delta E).
    """
    # to Lab
    L1, a1, b1 = xyz_to_lab(hex_to_xyz(base))
    L2, a2, b2 = xyz_to_lab(hex_to_xyz(other))

    # to LCH
    _, C1, H1 = lab_to_lch([L1, a1, b1])
    _, C2, _ = lab_to_lch([L2, a2, b2])

    l = 1 if unit_lc_ratio else 2
    c = 1

    # Lf
    S_L = 0.511 if L1 < 16 else (0.040975 * L1) / (1 + 0.01765 * L1)
    fL = (L1 - L2) / (l * S_L)

    # Cf
    S_C = (0.0638 * C1) / (1 + 0.0131 * C1) + 0.638
    fC = (C1 - C2) / (c * S_C)

    # Hf
    F = np.sqrt(C1 ** 4 / (C1 ** 4 + 1900))

    if 164 <= H1 <= 345:
        T = 0.56 + abs(0.2 * np.cos(np.radians(H1 + 168)))
    else:
        T = 0.36 + abs(0.4 * np.cos(np.radians(H1 + 35)))

    S_H = S_C * (F * T + 1 - F)

    dH = np.sqrt(abs((a1 - a2) ** 2 + (b1 - b2) ** 2 - (C1 - C2) ** 2))
    fH = dH / S_H

    # score
    score = fL ** 2 + fC ** 2 + fH ** 2

    return score


def cmc_1_1(base: str, other: str) -> float:
    """
    Wrapper for cmc function with l:c = 1:1.

    Args:
        base (str): string with hex code of the base color.
        other (str): string with hex code of the compared color.

    Returns:
        float: Calculated score (squared delta E).
    """
    return _cmc(base, other, unit_lc_ratio=True)


def cmc_2_1(base: str, other: str) -> float:
    """
    Wrapper for cmc function with l:c = 1:1.

    Args:
        base (str): string with hex code of the base color.
        other (str): string with hex code of the compared color.

    Returns:
        float: Calculated score (squared delta E).
    """
    return _cmc(base, other, unit_lc_ratio=False)
