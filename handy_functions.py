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
    Ensures that probabilities are in the range 0 <= p <= 1, or else assigns
    a default value of 0.5 to p.
    """
    return p if 0 <= p <= 1 else 0.5


def clear_old_files(extension, directory="static/files/"):
    [os.remove(file) for file in glob.glob(f"{directory}*.{extension}",
                                           recursive=True)]


def get_random_sample(distribution, size, parameters):
    """
    Returns a random sample of size {size} with the given {parameters},
    for the specified {distribution}.
    """
    if distribution in {"Negative Binomial", "Binomial", "Geometric",
                        "Bernoulli"}:
        # probability(p) is the last parameter
        parameters[-1] = validate_probability(parameters[-1])

    try:
        return distributions[distribution].rvs(*parameters, size=size)
    except KeyError:
        return 1


def plot_graph(graph_type, data, title):
    """
    Plots the required {graph_type} using the {data}, saves it, and returns
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
    Plots various graphs using the data, saves them as png files, and returns
    a dict of their names.
    """
    # remove previously saved graphs
    clear_old_files("png")

    # plot and save the graphs of the current data
    graphs = {'distplot': plot_graph(distplot, data, "Distribution Plot"),
              'boxplot': plot_graph(boxplot, data, "Box Plot"),
              'violinplot': plot_graph(violinplot, data, "Violin Plot")
              }
    return graphs


def int_if_fraction_is_zero(x):
    """
    Converts numerical values with zero fractional parts into integers
    """
    return int(x) if x % 1 == 0 else x


def descriptive_stats(data):
    """
    Returns basic descriptive statistics for the data
    """
    stats = {'Mean': data.mean(),
             'Median': median(data),
             'Standard Deviation': data.std(),
             'Minimum': data.min(),
             'Maximum': data.max()
             }
    try:
        stats['Mode'] = mode(data)
    except ValueError:
        stats['Mode'] = "No unique mode."

    return {key: int_if_fraction_is_zero(round(value, 4))
            for key, value in stats.items()}
