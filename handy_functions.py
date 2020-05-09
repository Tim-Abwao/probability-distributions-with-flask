#!/usr/bin/env python3
# coding: utf-8

import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
from datetime import datetime
from statistics import mean, median, stdev, mode
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


def validate_probability(p):
    """
    Ensures probabilities stick to the range 0<=p<=1 by assigning a default
    value of p=0.5 for entries greater than 1
    """
    if 0 <= p <= 1:
        return p
    else:
        return 0.5


def get_random_sample(distribution, size, parameters):
    """
    Returns a random sample of size {size} with the given {parameters},
    for the specified {distribution}.
    """
    params = list(parameters)

    if distribution == "Normal":
        return norm.rvs(params[0], params[1], size=size)

    if distribution == "Poisson":
        return poisson.rvs(params[0], size=size)

    if distribution == "Bernoulli":
        return bernoulli.rvs(params[0], size=size)

    if distribution == "Uniform":
        return uniform.rvs(params[0], params[1], size=size)

    if distribution == "Geometric":
        return geom.rvs(params[0], size=size)

    if distribution == "Alpha":
        return alpha.rvs(params[0], size=size)

    if distribution == "Beta":
        return beta.rvs(params[0], params[1], size=size)

    if distribution == "Chi-squared":
        return chi2.rvs(params[0], size=size)

    if distribution == "Exponential":
        return expon.rvs(params[0], size=size)

    if distribution == "F":
        return f.rvs(params[0], params[1], size=size)

    if distribution == "Gamma":
        return gamma.rvs(params[0], size=size)

    if distribution == "Pareto":
        return pareto.rvs(params[0], size=size)

    if distribution == "Student t":
        return t.rvs(params[0], size=size)

    if distribution == "Binomial":
        return binom.rvs(round(params[0]), params[1], size=size)

    if distribution == "Negative Binomial":
        return nbinom.rvs(round(params[0]), params[1], size=size)

    return 1


def clear_old_files(extension):
    old_files = glob.glob("static/files/*." + extension, recursive=True)
    for file in old_files:
        os.remove(file)


def get_graphs(data):
    """
    Plots  distribution graph of the random sample and saves it to a png file
    """
    # clear old graphs
    clear_old_files("png")
    # create time-stamped names for the graph image
    graph_names = [
        "files/" + str(datetime.now()) + f"_{i}.png"
        for i in ["distplot", "violinplot", "boxplot"]
    ]
    graph_loc = ["static/" + i for i in graph_names]
    sns.set()
    # Distribution plot
    plt.figure(figsize=(10, 6))
    sns.distplot(data, color="teal")
    plt.xticks(rotation=90)
    plt.title("Distribution plot", fontsize=25, fontweight=550, pad=20)
    plt.savefig(graph_loc[0], transparent=True)
    # Violin plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(data, color="#3FBFBF")
    plt.xticks(rotation=90)
    plt.title("Violin plot", fontsize=25, fontweight=550, pad=20)
    plt.savefig(graph_loc[1], transparent=True)
    # Box plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(data, color="#3FBFBF")
    plt.xticks(rotation=90)
    plt.title("Box plot", fontsize=25, fontweight=550, pad=20)
    plt.savefig(graph_loc[2], transparent=True)
    return graph_names


def descriptive_stats(random_sample):
    """
    Returns basic descriptive statistics for the random sample
    """
    try:
        _mean = round(mean(random_sample), 4)
        _median = round(median(random_sample), 4)
    except ValueError:
        _median = _mean = "No data to process."

    try:
        std = round(stdev(random_sample), 4)
        _min = round(min(random_sample), 4)
        _max = round(max(random_sample), 4)
    except ValueError:
        std = _min = _max = "Not available. At least 2 data points required."

    try:
        _mode = round(mode(random_sample), 4)
    except ValueError:
        _mode = "No unique mode."

    return [
        ("Mean: ", _mean),
        ("Median: ", _median),
        ("Mode: ", _mode),
        ("Standard Deviation: ", std),
        ("Minimum: ", _min),
        ("Maximum: ", _max),
    ]
