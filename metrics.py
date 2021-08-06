from converters import *
from helpers import squared_euclidean


def rgb_euclidean(base, other):
    '''Calculates the sum of squares of primary colors differences.
    
    score = (R1 - R2)^2 + (G1 - G2)^2 + (B1 - B2)^2
    
    Args:
    - base - string with hex code of the base color (e.g. '#ff0000', '124f05')
    - other - string with hex code of the compared color
    
    Returns:
    Calculated score (variance of the color distances)
    '''
    prim_base = hex_to_dec_primaries(base)
    prim_other = hex_to_dec_primaries(other)
    
    score = squared_euclidean(prim_base, prim_other)
        
    return score


def rgb_gamma_correction(base, other):
    '''Calculates the weighted sum of squares of primary colors differences.
    
    The weights are evaluated based on so-called "redmean":
    redmean = (R1 + R2) / 2
    If the value is smaller than 128 the weights W = [wR, wG, wB] are [2, 4, 3]
    and [3, 4, 2] otherwise.
    
    score = wR (R1 - R2)^2 + wG(G1 - G2)^2 +  wB(B1 - B2)^2
    
    Args:
    - base - string with hex code of the base color (e.g. '#ff0000', '124f05')
    - other - string with hex code of the compared color
    
    Returns:
    Calculated score (weighted variance of the color distances)
    '''
    prim_base = hex_to_dec_primaries(base)
    prim_other = hex_to_dec_primaries(other)
    
    redmean = (prim_base[0] + prim_other[0]) / 2
    weights = (2, 4, 3) if redmean < 128 else (3, 4, 2)
    
    score = squared_euclidean(prim_base, prim_other, weights)
        
    return score


def xyz_euclidean(base, other):
    '''Calculates the sum of squares of XYZ color coordinates.
    The results are quite bad and it was expected (but interesting to observe)
    as XYZ is merely a base used to other systems convertions.
    
    score = (X1 - X2)^2 + (Y1 - Y2)^2 + (Z1 - Z2)^2
    
    Args:
    - base - string with hex code of the base color (e.g. '#ff0000', '124f05')
    - other - string with hex code of the compared color
    
    Returns:
    Calculated score (variance of the distances)
    '''
    xyz_base = hex_to_xyz(base)
    xyz_other = hex_to_xyz(other)
    
    score = squared_euclidean(xyz_base, xyz_other)
        
    return score


def cie76(base, other):
    '''Calculates squared delta E according to CIE76 standard.
    
    score = (L1 - L2)^2 + (a1 - a2)^2 + (b1 - b2)^2
    
    Args:
    - base - string with hex code of the base color (e.g. '#ff0000', '124f05')
    - other - string with hex code of the compared color
    
    Returns:
    Calculated score (squared delta E)
    '''
    lab_base = xyz_to_lab(hex_to_xyz(base))
    lab_other = xyz_to_lab(hex_to_xyz(other))
    
    score = squared_euclidean(lab_base, lab_other)
        
    return score


def cie94(base, other):
    '''Calculates squared delta E according to CIE94 standard.

    score = wL(L1 - L2)^2 + wC(C1 - C2)^2 + wH(C1 - C2)^2
    where:
    wL = 1
    wC = 1 / (1 + K1C1)^2
    wH = 1 / (1 + K2C1)^2
    with:
    K1 = 0.045
    K2 = 0.015

    Args:
    - base - string with hex code of the base color (e.g. '#ff0000', '124f05')
    - other - string with hex code of the compared color

    Returns:
    Calculated score (squared delta E)
    '''
    lch_base = lab_to_lch(xyz_to_lab(hex_to_xyz(base)))
    lch_other = lab_to_lch(xyz_to_lab(hex_to_xyz(other)))

    K1 = 0.045
    K2 = 0.015

    C_base = lch_base[1]

    # squared denominators from the original formula
    weights = [1,
               1 / (1 + K1 * C_base)**2,
               1 / (1 + K2 * C_base)**2]

    score = squared_euclidean(lch_base, lch_other, weights)

    return score


def ciede2000(base, other):
    '''Calculates squared delta E according to CIEDE2000 standard.

    Args:
    - base - string with hex code of the base color (e.g. '#ff0000', '124f05')
    - other - string with hex code of the compared color

    Returns:
    Calculated score (squared delta E)
    '''
    # to LCH
    lab_base = xyz_to_lab(hex_to_xyz(base))
    L1, C1, H1 = lab_to_lch(lab_base)
    
    lab_other = xyz_to_lab(hex_to_xyz(other))
    L2, C2, H2 = lab_to_lch(lab_other)

    # L
    dL_p = L2 - L1
    L_b = (L1 + L2) / 2
    
    # C
    dC_p = C2 - C1
    C_b = (C1 + C2) / 2
    
    a_p_const = 1 - np.sqrt(C_b**7 / (C_b**7 + 25**7))
    a1, b1 = lab_base[-2:]
    a2, b2 = lab_other[-2:]
    a1_p, a2_p = a1 + a1 / 2 * a_p_const, a2 + a2 / 2 * a_p_const
    
    C1_p, C2_p = np.sqrt(a1_p**2 + b1**2), np.sqrt(a2_p**2 + b2**2)
    C_bp = (C1_p + C2_p) / 2
    
    # H
    h1_p = np.degrees(np.arctan2(b1, a1_p)) % 360
    h2_p = np.degrees(np.arctan2(b2, a2_p)) % 360
    
    dh_p = h2_p - h1_p
    if (h_p_diff := abs(h1_p - h2_p)) > 180:
        if h2_p > h1_p < 360:
            dh_p += 360
        else:
            dh_p - 360
            
    H_bp = (h1_p + h2_p) / 2
    if h_p_diff > 180:
        if h_p_diff < 360:
            H_bp += 180
        else:
            H_bp -= 180
            
    dH_p = 2 * np.sqrt(C1_p * C2_p) * np.sin(dh_p / 2)
    
    # denominators
    # S_L
    S_L = 1 + (0.015 * (L_b - 50)**2) / np.sqrt(20 + (L_b - 50)**2)
    # S_C
    S_C = 1 + 0.045 * C_bp
    # S_H
    T = 1 - 0.17 * np.cos(H_bp - 30) + 0.24 * np.cos(2 * H_bp + 6) - 0.2 * np.cos(4 * H_bp - 63)
    S_H = 1 + 0.015 * C_bp * T
       
    # compensation
    R_T = -2 * np.sqrt(C_bp**7 / (C_bp**7 + 25**7)) * np.sin(60 * np.exp(-((H_bp - 275) / 25)**2))
    compensation = R_T * (dC_p / S_C) * (dH_p / S_H)

    score = (dL_p / S_L)**2 +(dC_p / S_C)**2 + (dH_p / S_H)**2 + compensation

    return score