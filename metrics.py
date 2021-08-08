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

    score = (dL)^2 + (dC / (1 + K1C1))^2 + (sqrt(da^2 + db^2 - dC^2) / (1 + K2C1))^2
    with:
    K1 = 0.045
    K2 = 0.015

    Args:
    - base - string with hex code of the base color (e.g. '#ff0000', '124f05')
    - other - string with hex code of the compared color

    Returns:
    Calculated score (squared delta E)
    '''
    L1, a1, b1 = xyz_to_lab(hex_to_xyz(base))
    L2, a2, b2 = xyz_to_lab(hex_to_xyz(other))

    C1 = np.sqrt(a1**2 + b1**2)
    C2 = np.sqrt(a2**2 + b2**2)

    dC = C1 - C2
    
    dH = np.sqrt(abs((a1 - a2)**2 + (b1 - b2)**2 - dC**2))
    
    K1 = 0.045
    K2 = 0.015

    score = (L1 - L2)**2 + (dC / (1 + K1 * C1))**2 + (dH / (1 + K2 * C1))**2

    return score


def ciede2000(base, other):
    '''Calculates squared delta E according to CIEDE2000 standard.

    Args:
    - base - string with hex code of the base color (e.g. '#ff0000', '124f05')
    - other - string with hex code of the compared color

    Returns:
    Calculated score (squared delta E)
    '''
    # to Lab
    L1, a1, b1 = xyz_to_lab(hex_to_xyz(base))
    L2, a2, b2 = xyz_to_lab(hex_to_xyz(other))

    # fL
    dL_p = L2 - L1
    L_b = (L1 + L2) / 2
    
    S_L = 1 + (0.015 * (L_b - 50)**2) / np.sqrt(20 + (L_b - 50)**2)
    fL = dL_p / S_L
    
    # fC
    C1 = np.sqrt(a1**2 + b1**2)
    C2 = np.sqrt(a2**2 + b2**2)
    
    dC_p = C2 - C1
    C_b = (C1 + C2) / 2
    
    a_p_const_part = 1 - np.sqrt(C_b**7 / (C_b**7 + 25**7))
    a1_p = a1 + a1 / 2 * a_p_const_part
    a2_p = a2 + a2 / 2 * a_p_const_part
    
    C1_p = np.sqrt(a1_p**2 + b1**2)
    C2_p = np.sqrt(a2_p**2 + b2**2)
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

    T = 1 - 0.17 * np.cos(np.radians(H_bp - 30)) +\
        0.24 * np.cos(np.radians(2 * H_bp)) +\
        0.32 * np.cos(np.radians(3 * H_bp + 6)) -\
        0.2 * np.cos(np.radians(4 * H_bp - 63))
    
    S_H = 1 + 0.015 * C_bp * T
    fH = dH_p / S_H
       
    # score
    theta = np.radians(60 * np.exp(-((H_bp - 275) / 25)**2))
    R_T = -2 * np.sqrt(C_bp**7 / (C_bp**7 + 25**7)) * np.sin(theta)

    score = fL**2 + fC**2 + fH**2 + (R_T * fC * fH)

    return score


def cmc(base, other, unit_lc_ratio=True):
    '''Calculates squared delta E according to CMC l:c standard.

    Args:
    - base - string with hex code of the base color (e.g. '#ff0000', '124f05')
    - other - string with hex code of the compared color
    - unit_lc_ratio - if true l:c=1:1 (imperceptibility),
        otherwise l:c=2:1 (acceptability) default: True

    Returns:
    Calculated score (squared delta E)
    '''    # to Lab
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
    F = np.sqrt(C1**4 / (C1**4 + 1900))
    
    if (164 <= H1 <= 345):
        T = 0.56 + abs(0.2 * np.cos(np.radians(H1 + 168)))
    else:
        T = 0.36 + abs(0.4 * np.cos(np.radians(H1 + 35)))
    
    S_H = S_C * (F * T + 1 - F)
    
    dH = np.sqrt(abs((a1 - a2)**2 + (b1 - b2)**2 - (C1 - C2)**2))
    fH = dH / S_H
    
    # score
    score = fL**2 + fC**2 + fH**2
    
    return score


def cmc_1_1(base, other):
    '''Wrapper for cmc function with l:c = 1:1'''
    return cmc(base, other, unit_lc_ratio=True)
    
    
def cmc_2_1(base, other):
    '''Wrapper for cmc function with l:c = 1:1'''
    return cmc(base, other, unit_lc_ratio=False)
