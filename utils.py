import matplotlib
import matplotlib.pyplot as plt
from seaborn import boxplot, histplot, violinplot
import os
from glob import glob
from statistics import median, mode
from scipy import stats
from io import StringIO


matplotlib.use('svg')

distributions = {
    "Normal": stats.norm,
    "Poisson": stats.poisson,
    "Bernoulli": stats.bernoulli,
    "Uniform": stats.uniform,
    "Geometric": stats.geom,
    "Alpha": stats.alpha,
    "Beta": stats.beta,
    "Chi-squared": stats.chi2,
    "Exponential": stats.expon,
    "F": stats.f,
    "Gamma": stats.gamma,
    "Pareto": stats.pareto,
    "Student t": stats.t,
    "Binomial": stats.binom,
    "Negative Binomial":  stats.nbinom
}


def validate_probability(p):
    """
    Ensure that probability is in the interval [0, 1], or else assign a
    default value of 0.5.

    parameters
    ----------
    p: int, float
        Probability value.
    """
    return p if 0 <= p <= 1 else 0.5


def clear_old_files(extension='csv', directory="static/files/"):
    """
    Remove files of the specified format from the given directory.

    parameters
    ----------
    extension: str
        A file extension specifying a file format e.g "csv", "png", "html".
    directory: str
        Relative or absolute path to the folder containing the files to remove.
    """
    file_names = glob(f"{directory}*.{extension}", recursive=True)
    [os.remove(file) for file in file_names]


def int_from_0_decimal(number):
    """
    Cast a numeric value as an integer if its fractional part is equal to zero.
    """
    return int(number) if number % 1 == 0 else number


def get_graphs(data):
    """
    Plot graphs using the supplied data, and get them as text objects in svg
    format.

    parameters
    ----------
    data: sequence, array-like
        The values to plot.
    """
    graphs = {'distplot': plot_graph(graph_func=histplot, data=data,
                                     title="Distribution Plot",
                                     kwargs={"kde": True}),
              'boxplot': plot_graph(graph_func=boxplot, data=data,
                                    title="Box Plot"),
              'violinplot': plot_graph(graph_func=violinplot, data=data,
                                       title="Violin Plot")
              }
    return graphs


def plot_graph(graph_func, data, title, kwargs={}):
    """
    Create a graph using matplotlib and seaborn.

    parameters
    ----------
    graph_func: func
        A seaborn plotting function.
    data: array-like
        The values to plot.
    title: str
        A title for the graph to be plotted.
    kwargs: dict
        A dictionary of keyword arguements to supply to the plotting function
        specified in graph_func.
    """
    plt.figure(figsize=(8, 4.5))
    ax = graph_func(data=data, color="#3FBFBF", **kwargs)
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_title(title, fontsize=25, fontweight=550, pad=20)
    graph = StringIO()
    plt.savefig(graph, format='svg', transparent=True)
    plt.close()
    return graph


def descriptive_stats(data):
    """
    Get basic descriptive statistics for the data: mean, standard deviation,
    minimum, maximum and mode.

    parameters
    ----------
    data: numpy ndarray, pandas DataFrame
        The values to summarise.
    """
    stats = {'Mean': data.mean(),
             'Standard Deviation': data.std(),
             'Minimum': data.min(),
             'Maximum': data.max(),
             'Median': median(data),
             'Mode': mode(data)
             }
    return {key: int_from_0_decimal(round(value, 4))
            for key, value in stats.items()}


def get_random_sample(distribution="Normal", size=50, parameters=(0, 1)):
    """
    Generate a random sample of the specified distribution.

    parameters
    ----------
    distribution: str
        The type of distribution. One of "Normal", "Poisson", "Bernoulli",
        "Uniform", "Geometric", "Alpha", "Beta", "Chi-squared", "Exponential",
        "F", "Gamma", "Pareto", "Student t", "Binomial" or "Negative Binomial".
    size: int
        The desired sample size
    parameters: sequence
        A list or tuple distribution-specific parameters passed on to SciPy.
    """
    probabilistic_distributions = {
        "Negative Binomial", "Binomial", "Geometric", "Bernoulli"
    }
    # Ensure probabilities lie in the interval [0, 1]
    if distribution in probabilistic_distributions:
        parameters[-1] = validate_probability(parameters[-1])

    parameters = [int_from_0_decimal(param) for param in parameters]
    try:
        data = distributions[distribution].rvs(*parameters, size=size)
        return data, get_graphs(data), descriptive_stats(data)
    except KeyError as error:
        return error
