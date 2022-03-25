from base64 import b64encode
from collections.abc import Callable
from io import BytesIO

import matplotlib as mpl
from matplotlib.figure import Figure
from numpy import ndarray
from seaborn import boxplot, histplot, violinplot

# Matplotlib configuration
mpl.rc("figure", autolayout=True, dpi=250, figsize=(7, 4.5))
mpl.rc("font", family="serif")
mpl.rc("axes.spines", right=False, top=False)
mpl.use("agg")  # Use a non-interactive back-end


def plot_graph(
    graph_func: Callable, data: ndarray, title: str, **kwargs
) -> bytes:
    """Get a graph of the supplied `data`.

    Args:
        graph_func (function): A seaborn plotting function.
        data (ndarray): The values to plot.
        title (str): A title for the graph to be plotted.

    Returns:
        bytes: Base64-encoded graph in PNG format.
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


def get_graphs(data: ndarray) -> dict:
    """Create a dist-plot, box-plot and violin-plot using the supplied `data`.

    Args:
        data (ndarray): The values to plot.

    Returns:
        dict: A dictionary of plotted graphs.
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
