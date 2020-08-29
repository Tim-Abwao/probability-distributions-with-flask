import matplotlib.pyplot as plt
from seaborn import boxplot, distplot, violinplot
import os
import glob
from datetime import datetime
from statistics import median, mode
from scipy.stats import (
    norm,
    poisson,
    bernoulli,
    uniform,
    geom,
    alpha,
    t,
    beta,
    chi2,
    expon,
    f,
    gamma,
    pareto,
    binom,
    nbinom,
)

distributions = {
    "Normal": norm,
    "Poisson": poisson,
    "Bernoulli": bernoulli,
    "Uniform": uniform,
    "Geometric": geom,
    "Alpha": alpha,
    "Beta": beta,
    "Chi-squared": chi2,
    "Exponential": expon,
    "F": f,
    "Gamma": gamma,
    "Pareto": pareto,
    "Student t": t,
    "Binomial": binom,
    "Negative Binomial":  nbinom
}


def validate_probability(p):
    """
    Ensure that probabilities are in the range 0 <= p <= 1, or else assign
    them a default value of 0.5.
    """
    return p if 0 <= p <= 1 else 0.5


def clear_old_files(extension, directory="static/files/"):
    """Remove files of specified format from given directory."""
    filenames = glob.glob(f"{directory}*.{extension}", recursive=True)
    [os.remove(file) for file in filenames]


def get_random_sample(distribution, size, parameters):
    """
    Generate a random sample of the specified distribution of size length with
    supplied parameters.
    """
    if distribution in {"Negative Binomial", "Binomial", "Geometric",
                        "Bernoulli"}:
        parameters[-1] = validate_probability(parameters[-1])  # p is rightmost
    # Get int values for parameters read from form as float
    parameters = [int_if_fraction_is_zero(param) for param in parameters]
    try:
        return distributions[distribution].rvs(*parameters, size=size)
    except KeyError as error:
        return error


def plot_graph(graph_type, data, title):
    """
    Plot the specified graph_type from the data, save it, and return
    its name.
    """
    plt.figure(figsize=(10, 6))
    graph_type(data, color="#3FBFBF")
    plt.xticks(rotation=90)
    plt.title(title, fontsize=25, fontweight=550, pad=20)
    graph_name = f"files/{str(datetime.now())}_{title.split()[0]}.png"
    plt.savefig(f'static/{graph_name}', transparent=True)
    return graph_name


def get_graphs(data):
    """
    Get a distplot, boxplot and violinplot as png files.
    """
    clear_old_files("png")
    graphs = {'distplot': plot_graph(distplot, data, "Distribution Plot"),
              'boxplot': plot_graph(boxplot, data, "Box Plot"),
              'violinplot': plot_graph(violinplot, data, "Violin Plot")
              }
    return graphs


def int_if_fraction_is_zero(x):
    """
    Convert numerical values with zero fractional parts into integers.
    """
    return int(x) if x % 1 == 0 else x


def descriptive_stats(data):
    """Get basic descriptive statistics of the data."""
    stats = {'Mean': data.mean(),
             'Standard Deviation': data.std(),
             'Minimum': data.min(),
             'Maximum': data.max(),
             'Median': median(data),
             'Mode': mode(data)
             }
    return {key: int_if_fraction_is_zero(round(value, 4))
            for key, value in stats.items()}
