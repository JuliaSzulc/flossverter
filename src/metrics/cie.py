"""
Metrics utilizing CIE standards.
"""
import numpy as np

from converters import hex_to_xyz, xyz_to_lab
from metrics import squared_euclidean


def cie76(base: str, other: str) -> float:
    """
    Calculates squared delta E according to CIE76 standard.

    Accepted inputs are colors in hexadecimal format (e.g. '#ff0000', '124f05').

    Args:
        base (str): string with hex code of the base color.
        other (str): string with hex code of the compared color.

    Returns:
        float: Calculated score (squared delta E).
    """
    lab_base = xyz_to_lab(hex_to_xyz(base))
    lab_other = xyz_to_lab(hex_to_xyz(other))

    score = squared_euclidean(lab_base, lab_other)

    return score


def cie94(base: str, other: str) -> float:
    """
    Calculates squared delta E according to CIE94 standard.

    score = (dL)^2 + (dC / (1 + K1C1))^2 + (sqrt(da^2 + db^2 - dC^2) / (1 + K2C1))^2
    with:
    K1 = 0.045
    K2 = 0.015

    Accepted inputs are colors in hexadecimal format (e.g. '#ff0000', '124f05').

    Args:
        base (str): string with hex code of the base color.
        other (str): string with hex code of the compared color.

    Returns:
        float: Calculated score (squared delta E).
    """
    L1, a1, b1 = xyz_to_lab(hex_to_xyz(base))
    L2, a2, b2 = xyz_to_lab(hex_to_xyz(other))

    C1 = np.sqrt(a1 ** 2 + b1 ** 2)
    C2 = np.sqrt(a2 ** 2 + b2 ** 2)

    dC = C1 - C2

    dH = np.sqrt(abs((a1 - a2) ** 2 + (b1 - b2) ** 2 - dC ** 2))

    K1 = 0.045
    K2 = 0.015

    score = (L1 - L2) ** 2 + (dC / (1 + K1 * C1)) ** 2 + (dH / (1 + K2 * C1)) ** 2

    return score


def ciede2000(base: str, other: str) -> float:
    """
    Calculates squared delta E according to CIEDE2000 standard.

    Accepted inputs are colors in hexadecimal format (e.g. '#ff0000', '124f05').

    Args:
        base (str): string with hex code of the base color.
        other (str): string with hex code of the compared color.

    Returns:
        float: Calculated score (squared delta E).
    """
    # to Lab
    L1, a1, b1 = xyz_to_lab(hex_to_xyz(base))
    L2, a2, b2 = xyz_to_lab(hex_to_xyz(other))

    # fL
    dL_p = L2 - L1
    L_b = (L1 + L2) / 2

    S_L = 1 + (0.015 * (L_b - 50) ** 2) / np.sqrt(20 + (L_b - 50) ** 2)
    fL = dL_p / S_L

    # fC
    C1 = np.sqrt(a1 ** 2 + b1 ** 2)
    C2 = np.sqrt(a2 ** 2 + b2 ** 2)

    dC_p = C2 - C1
    C_b = (C1 + C2) / 2

    a_p_const_part = 1 - np.sqrt(C_b ** 7 / (C_b ** 7 + 25 ** 7))
    a1_p = a1 + a1 / 2 * a_p_const_part
    a2_p = a2 + a2 / 2 * a_p_const_part

    C1_p = np.sqrt(a1_p ** 2 + b1 ** 2)
    C2_p = np.sqrt(a2_p ** 2 + b2 ** 2)
    C_bp = (C1_p + C2_p) / 2

    S_C = 1 + 0.045 * C_bp
    fC = dC_p / S_C

    # fH
    h1_p = np.degrees(np.arctan2(b1, a1_p)) % 360
    h2_p = np.degrees(np.arctan2(b2, a2_p)) % 360

    dh_p = h2_p - h1_p
    if (h_p_diff := abs(h1_p - h2_p)) > 180:
        if h2_p > h1_p:
            dh_p -= 360
        else:
            dh_p += 360

    h_p_sum = h1_p + h2_p
    if h_p_diff > 180:
        if h_p_sum < 360:
            h_p_sum += 360
        else:
            h_p_sum -= 360
    H_bp = h_p_sum / 2

    dH_p = 2 * np.sqrt(C1_p * C2_p) * np.sin(np.radians(dh_p / 2))

    T = (
        1
        - 0.17 * np.cos(np.radians(H_bp - 30))
        + 0.24 * np.cos(np.radians(2 * H_bp))
        + 0.32 * np.cos(np.radians(3 * H_bp + 6))
        - 0.2 * np.cos(np.radians(4 * H_bp - 63))
    )

    S_H = 1 + 0.015 * C_bp * T
    fH = dH_p / S_H

    # score
    theta = np.radians(60 * np.exp(-(((H_bp - 275) / 25) ** 2)))
    R_T = -2 * np.sqrt(C_bp ** 7 / (C_bp ** 7 + 25 ** 7)) * np.sin(theta)

    score = fL ** 2 + fC ** 2 + fH ** 2 + (R_T * fC * fH)

    return score
