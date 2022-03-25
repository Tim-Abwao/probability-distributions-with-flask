from base64 import b64encode
from io import BytesIO

import matplotlib as mpl
from matplotlib.figure import Figure
from seaborn import boxplot, histplot, violinplot

# Matplotlib configuration
mpl.rc("figure", autolayout=True, dpi=250, figsize=(7, 4.5))
mpl.rc("font", family="serif")
mpl.rc("axes.spines", right=False, top=False)
mpl.use("agg")  # Use a non-interactive back-end


def plot_graph(graph_func, data, title, **kwargs):
    """Get a graph for the supplied data using seaborn.

    Parameters
    ----------
    graph_func : func
        A seaborn plotting function.
    data : array-like
        The data values to plot.
    title : str
        A title for the graph to be plotted.
    **kwargs
        Extra keyword arguments to supply to graph_func.

    Returns
    -------
    Base64-encoded string for a graph in PNG format.
    """
    fig = Figure()
    ax = fig.subplots(nrows=1, ncols=1)
    # Plot the graph
    graph_func(x=data, color="#3FBFBF", ax=ax, **kwargs)
    ax.tick_params(axis="x", rotation=45)
    ax.set_title(title, fontsize=20, fontweight=550, pad=20)

    # Get the graph in PNG format as a base64-encoded string
    graph = BytesIO()
    fig.savefig(graph, transparent=True)

    return b64encode(graph.getvalue()).decode("utf-8")


def get_graphs(data):
    """Plot various types of graphs using the `plot_graph` function.

    Parameters
    ----------
    data : sequence, array-like
        The values to plot.

    Returns
    -------
    A dictionary of plotted graphs.
    """
    return {
        "distplot": plot_graph(
            graph_func=histplot,
            data=data,
            title="Distribution Plot",
            bins=25,
            kde=True,
        ),
        "boxplot": plot_graph(
            graph_func=boxplot, data=data, title="Box Plot", width=0.5
        ),
        "violinplot": plot_graph(
            graph_func=violinplot, data=data, title="Violin Plot", width=0.5
        ),
    }
