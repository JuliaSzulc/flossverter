import numpy as np

from helpers import hex_to_dec_primaries, hex_to_xyz


def rgb_euclidean(base, other):
    '''Calculates the sum of squares of primary colors differences.
    
    score = (R1 - R2)^2 + (G1 - G2)^2 + (B1 - B2)^2
    
    Args:
    - base - string with hex code of the base color (e.g. '#ff0000', '124f05')
    - other - string with hex code of the compared color
    
    Returns:
    Calculated score (variance of the color distances)
    '''
    primaries_base = hex_to_dec_primaries(base)
    primaries_other = hex_to_dec_primaries(other)
    
    score = sum([(b - o)**2 for b, o in zip(primaries_base, primaries_other)])
        
    return score


def rgb_gamma_correction(base, other):
    '''Calculates the weighted sum of squares of primary colors differences.
    
    The weights are evaluated based on so-called "redmean":
    redmean = (R1 + R2) / 2
    If the value is smaller than 128 the weights W = [wR, wG, wB] are [2, 4, 3]
    and [3, 4, 2] otherwise.
    
    score = wR * (R1 - R2)^2 + wG * (G1 - G2)^2 +  wB * (B1 - B2)^2
    
    Args:
    - base - string with hex code of the base color (e.g. '#ff0000', '124f05')
    - other - string with hex code of the compared color
    
    Returns:
    Calculated score (weighted variance of the color distances)
    '''
    primaries_base = hex_to_dec_primaries(base)
    primaries_other = hex_to_dec_primaries(other)
    
    redmean = (primaries_base[0] + primaries_other[0]) / 2
    weights = (2, 4, 3) if redmean < 128 else (3, 4, 2)
    
    score = sum([((b - o)**2 * w) for b, o, w in zip(primaries_base, primaries_other, weights)])
        
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
    
    score = np.sum((xyz_base - xyz_other)**2)
        
    return score