import matplotlib.colors as colors
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

def blue_variance_graph(df, report):
    cmap = cm.get_cmap('Blues')
    new_cmap = truncate_colormap(cmap, 0.2, 0.8)
    df.plot.line(x="day", title=report, figsize=(8,6), cmap=new_cmap)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.grid()
    plt.tight_layout()
    plt.show(block=True)

def comparison_graph(df, report):
    # cmap = cm.get_cmap('Blues')
    # new_cmap = truncate_colormap(cmap, 0.2, 0.8)
    df.plot.line(x="day", title=report, figsize=(8,6))
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.grid()
    plt.tight_layout()
    plt.show(block=True)