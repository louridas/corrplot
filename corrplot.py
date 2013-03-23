import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Ellipse
import string

def corrplot(data, pvalues, labels):
    """Creates a correlation plot of the passed data.

    The function returns the plot which can then be shown with
    plot.show(), saved to a file with plot.savefig(), or manipulated
    in any other standard matplotlib way.

    data is the correlation matrix, a 2-D numpy array containing
    the pairwise correlations between variables;

    pvalues is a matrix containing the pvalue for each corresponding
    correlation value; if none it is assumed to be the zero matrix

    labels is an array containing the variable names
    """

    plt.figure(1)

    column_labels = labels
    row_labels = labels
    
    ax = plt.subplot(1, 1, 1, aspect='equal')

    width, height = data.shape
    num_cols, num_rows = width, height

    if pvalues is None:
        pvalues = np.zeros([num_rows, num_cols])
        
    shrink = 0.9

    poscm = cm.get_cmap('Blues')
    negcm = cm.get_cmap('Oranges')

    for x in xrange(width):
        for y in xrange(height):
            d = data[x, y]
            c = pvalues[x, y]
            rotate = -45 if d > 0 else +45
            clrmap = poscm if d >= 0 else negcm
            d_abs = np.abs(d)
            ellipse = Ellipse((x, y),
                              width=1 * shrink,
                              height=(shrink - d_abs*shrink),
                              angle=rotate)
            ellipse.set_edgecolor('black')
            ellipse.set_facecolor(clrmap(d_abs))
            if c > 0.05:
                ellipse.set_linestyle('dotted')
            ax.add_artist(ellipse)

    ax.set_xlim(-1, num_cols)
    ax.set_ylim(-1, num_rows)
        
    ax.xaxis.tick_top()
    xtickslocs = np.arange(len(row_labels))
    ax.set_xticks(xtickslocs)
    ax.set_xticklabels(row_labels, rotation=30, fontsize='small', ha='left')

    ax.invert_yaxis()
    ytickslocs = np.arange(len(row_labels))
    ax.set_yticks(ytickslocs)
    ax.set_yticklabels(column_labels, fontsize='small')

    return plt

if __name__ == "__main__":
    
    num_rows = 20
    num_cols = num_rows

    min_length = 10
    max_length = 20

    alnums = list(string.ascii_uppercase + string.digits)
    labels = [''.join(np.random.choice(alnums,
                                       np.random.randint(min_length,
                                                         max_length)))
              for y in np.arange(num_rows)]
    
   
    data = np.random.random([num_rows, num_cols])

    data[np.random.choice(num_rows, num_rows / 2), :] *= -1

    np.fill_diagonal(data, 1)

    data_symm = (data + data.T) / 2

    plot = corrplot(data_symm, None, labels)
    plot.show()
