import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


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
    3x1 numpy array of float XYZ coordinates
    '''
    rgb = hex_to_dec_primaries(color, arithmetic=True)

    def to_lin(c):
        if c > 0.04045:
            a = 0.055
            return ((c + a) / (1 + a))**2.4
        else:
            return c / 12.92

    rgb_lin = np.array([[to_lin(c)] for c in rgb])

    matrix = np.array([[0.4124, 0.3576, 0.1805],
                       [0.2126, 0.7152, 0.0722],
                       [0.0193, 0.1192, 0.9505]])
    xyz = np.matmul(matrix, rgb_lin)

    return xyz


def swatch(base_color, compared_colors, base_label=False, compared_labels=False,
           vertical=False, size=2, whitespace=3):
    '''Displays evaluated list of similar colors next to the base color.

    Args:
    - base_col - color code recognized by Seaborn corresponding to the base
    - compared_colors - list of color codes recognized by Seaborn
    - base_label - label of the base color to be displayed in the plot
    - compared_labels - labels of the compared colors to be displayed in the plot
    - vertical - if True the swatches are plotted in a column, default: False
    - size - figure size multiplier, default: 2
    - whitespace - width of white lines separating swatches, default: 3
    '''
    # setting right orientation of data and labels
    if vertical:
        axis = 1
        xlabels = [base_label, ''] if base_label else False
        ylabels = compared_labels if compared_labels else False
    else:
        axis = 0
        xlabels = compared_labels if compared_labels else False
        ylabels = [base_label, ''] if base_label else False

    n = len(compared_colors)
    # plot heatmap
    ax = sns.heatmap(np.stack(([n] * n, np.arange(n)), axis),
                     cmap=compared_colors + [base_color],
                     cbar=False,
                     square=True,
                     figure=plt.figure(figsize=((size * n), (size * n))),
                     xticklabels=xlabels,
                     yticklabels=ylabels)

    if vertical:
        # ylabels on the right side (next to the colors)
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position('right')
        # xlabels on the top (above the base)
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')

    # remove ticks
    ax.tick_params(length=0)

    # rotate ylabels
    plt.setp(plt.yticks()[1], rotation=0)

    # drawing whitespaces
    line_func = ax.axhline if vertical else ax.axvline
    for i in range(n):
        line_func(i, color='white', lw=whitespace)