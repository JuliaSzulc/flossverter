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
    '''Converts standard RGB color code to XYZ coordinates using the standard
    illuminant D65 with 2° observer.

    Args:
    - color - color code string (hex), can include '#' prefix

    Returns:
    1x3 numpy array of float XYZ coordinates (0-1)
    '''
    rgb = hex_to_dec_primaries(color, arithmetic=True)

    def to_lin(c):
        if c > 0.04045:
            A = 0.055
            return ((c + A) / (1 + A))**2.4
        else:
            return c / 12.92

    rgb_lin = np.array([[to_lin(c)] for c in rgb])

    sRGB_MATRIX = np.array([[0.4124564, 0.3575761, 0.1804375],
                            [0.2126729, 0.7151522, 0.0721750],
                            [0.0193339, 0.1191920, 0.9503041]])
    xyz = np.matmul(sRGB_MATRIX, rgb_lin).flatten()

    return xyz


def xyz_to_lab(xyz):
    '''Converts XYZ coordinates (0-1) to Lab using the standard illuminant D65
    with 2° observer.

    Args:
    - xyz - list or numpy array with XYZ coordinates (0-1)

    Returns:
    List containing Lab coordinates
    '''
    XYZ_N = [0.95047, 1, 1.08883]
    EPSILON = 0.008856 # 216 / 24389
    KAPPA = 903.3 # 24389 / 27

    x_r, y_r, z_r = np.array(xyz) / XYZ_N
    
    def f(t):
        if t > EPSILON:
            return np.cbrt(t)
        else:
            return (KAPPA * t + 16) / 116
        
    L = 116 * f(y_r) - 16
    a = 500 * (f(x_r) - f(y_r))
    b = 200 * (f(y_r) - f(z_r))
    
    return [L, a, b]


def lab_to_lch(lab):
    '''Converts Lab coordinates to LCHab.

    Args:
    - lab - list or numpy array with Lab coordinates

    Returns:
    List containing LCH coordinates with H expressed in degrees.
    '''
    L, a, b = lab
    
    C = np.sqrt(a**2 + b**2)
    H = np.degrees(np.arctan2(b, a))
    if H < 0:
        H += 360
    
    return [L, C, H]
