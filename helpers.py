import seaborn as sns
import numpy as np
from matplotlib import ticker
from matplotlib.pyplot import figure

def swatch(base_col, similar_cols):
    '''Displays evaluated list of similar colors next to the base color.
    
    Args:
    base_col = color code recognized by Seaborn corresponding to the base
    similar_cols = list of color codes recognized by Seaborn
    '''
    sns.set_theme()
    n = len(similar_cols)
    width = 2 * n

    ax = sns.heatmap([[n] * n, np.arange(n)],
                     cmap=similar_cols + [base_col],
                     cbar=False,
                     square=True,
                     figure=figure(figsize=(width, width)))

    for i in range(n):
        ax.axvline(i, color='white', lw=3)
        
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_major_locator(ticker.NullLocator())