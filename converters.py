import numpy as np


def hex_to_dec_primaries(color, arithmetic=False):
    '''Splits hex color code into three decimal values of the primary colors.

    Args:
    - color - color code string (hex), can include '#' prefix
    - arithmetic - if True returns float values between 0 and 1, default: False

    Returns:
    List of three ints (0-255) or floats (0-1)
    '''
    def to_dec(h):
        dec = int('0x' + h, 16)
        if arithmetic:
            dec /= 255
        return dec

    color = color.lstrip('#')
    return [to_dec(color[i:i+2]) for i in range(0, len(color), 2)]


def hex_to_xyz(color):
    '''Converts standard RGB color code to XYZ coordinates using standard
    illuminant D65.

    Args:
    - color - color code string (hex), can include '#' prefix

    Returns:
    1x3 numpy array of float XYZ coordinates
    '''
    rgb = hex_to_dec_primaries(color, arithmetic=True)

    def to_lin(c):
        if c > 0.04045:
            A = 0.055
            return ((c + A) / (1 + A))**2.4
        else:
            return c / 12.92

    rgb_lin = np.array([[to_lin(c)] for c in rgb])

    MATRIX = np.array([[0.4124, 0.3576, 0.1805],
                       [0.2126, 0.7152, 0.0722],
                       [0.0193, 0.1192, 0.9505]])
    xyz = np.matmul(MATRIX, rgb_lin).flatten()

    return xyz


def xyz_to_lab(xyz):
    XYZ_N = [95.0489, 100, 108.8840]
    EPSILON = 0.008856
    KAPPA = 903.3
    
    def f(t):
        if t > EPSILON:
            return np.cbrt(t)
        else:
            return (KAPPA * t + 16) / 116
        
    x_r, y_r, z_r = xyz / XYZ_N
    
    L = 116 * f(y_r) - 16
    a = 500 * (f(x_r) - f(y_r))
    b = 200 * (f(y_r) - f(z_r))
    
    return [L, a, b]
