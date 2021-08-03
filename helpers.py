import seaborn as sns
import numpy as np
import matplotlib.pyplot as  plt


def swatch(base_color, compared_colors, base_label=False, compared_labels=False,
           vertical=False, size=2, whitespace=3):
    '''Displays evaluated list of similar colors next to the base color.
    
    Args:
    base_col - color code recognized by Seaborn corresponding to the base
    compared_colors - list of color codes recognized by Seaborn
    base_label - label of the base color to be displayed in the plot
    compared_labels - labels of the compared colors to be displayed in the plot
    vertical - if True the swatches are plotted in a column, default: False
    size - figure size multiplier, default: 2
    whitespace - width of white lines separating swatches, default: 3
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
