from converters import *
from helpers import squared_euclidean


def rgb_euclidean(base, other):
    '''Calculates the sum of squares of primary colors differences.
    
    score = (R2 - R1)^2 + (G2 - G1)^2 + (B2 - B1)^2
    
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
    
    score = wR (R2 - R1)^2 + wG(G2 - G1)^2 +  wB(B2 - B1)^2
    
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
    
    score = (X2 - X1)^2 + (Y2 - Y1)^2 + (Z2 - Z1)^2
    
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
    
    score = (L2 - L1)^2 + (a2 - a1)^2 + (b2 - b1)^2
    
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

    score = wL(L2 - L1)^2 + wC(C2 - C1)^2 + wH(C2 - C1)^2
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
