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
    Ensures probabilities stick to the range 0<=p<=1 by assigning a default
    value of p=0.5 for entries greater than 1
    """
    return p if 0 <= p <= 1 else 0.5


def clear_old_files(extension):
    old_files = glob.glob("static/files/*." + extension, recursive=True)
    for file in old_files:
        os.remove(file)


def get_random_sample(distribution, size, *parameters):
    """
    Returns a random sample of size {size} with the given {parameters},
    for the specified {distribution}.
    """
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
    Plots  distribution graph of the random sample and saves it to a png file
    """
    # clear old graphs
    clear_old_files("png")
    # create time-stamped names for the graph image
    graphs = {'distplot': plot_graph(distplot, data, "Distribution Plot"),
              'boxplot': plot_graph(boxplot, data, "Box Plot"),
              'violinplot': plot_graph(violinplot, data, "Violin Plot")
              }
    return graphs


def Int_float(x):
    """
    Converts float values with zero fractional parts into integers
    """
    return int(x) if x % 1 == 0 else x


def descriptive_stats(data):
    """
    Returns basic descriptive statistics for the random sample
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

    return {key: Int_float(round(value, 4)) for key, value in stats.items()}
