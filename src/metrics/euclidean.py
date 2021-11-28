"""
Metrics based on euclidean distances.
"""
from src.converters import hex_to_dec_primaries, hex_to_xyz
from src.metrics import squared_euclidean


def rgb_euclidean(base: str, other: str) -> float:
    """
    Calculates the sum of squares of primary colors differences.

    score = (R1 - R2)^2 + (G1 - G2)^2 + (B1 - B2)^2

    Accepted inputs are colors in hexadecimal format (e.g. '#ff0000', '124f05').

    Args:
        base (str): string with hex code of the base color.
        other (str): string with hex code of the compared color.

    Returns:
        float: Calculated score (variance of the color distances).
    """
    prim_base = hex_to_dec_primaries(base)
    prim_other = hex_to_dec_primaries(other)

    score = squared_euclidean(prim_base, prim_other)

    return score


def rgb_euclidean_gamma_correction(base: str, other: str) -> float:
    """
    Calculates the weighted sum of squares of primary colors differences.

    The weights are evaluated based on so-called "redmean":
    redmean = (R1 + R2) / 2
    If the value is smaller than 128 the weights W = [wR, wG, wB] are [2, 4, 3] and
    [3, 4, 2] otherwise.

    score = wR (R1 - R2)^2 + wG(G1 - G2)^2 +  wB(B1 - B2)^2

    Accepted inputs are colors in hexadecimal format (e.g. '#ff0000', '124f05').

    Args:
        base (str): string with hex code of the base color.
        other (str): string with hex code of the compared color.

    Returns:
        float: Calculated score (weighted variance of the color distances).
    """
    prim_base = hex_to_dec_primaries(base)
    prim_other = hex_to_dec_primaries(other)

    redmean = (prim_base[0] + prim_other[0]) / 2
    weights = (2, 4, 3) if redmean < 128 else (3, 4, 2)

    score = squared_euclidean(prim_base, prim_other, weights)

    return score


def xyz_euclidean(base: str, other: str) -> float:
    """
    Calculates the sum of squares of XYZ color coordinates.

    The results are quite bad and it was expected (but interesting to observe) as XYZ is
    merely a base used to other systems convertions.

    score = (X1 - X2)^2 + (Y1 - Y2)^2 + (Z1 - Z2)^2

    Accepted inputs are colors in hexadecimal format (e.g. '#ff0000', '124f05').

    Args:
        base (str): string with hex code of the base color.
        other (str): string with hex code of the compared color.

    Returns:
        float: Calculated score (variance of the distances).
    """
    xyz_base = hex_to_xyz(base)
    xyz_other = hex_to_xyz(other)

    score = squared_euclidean(xyz_base, xyz_other)

    return score
