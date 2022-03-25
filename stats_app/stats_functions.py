from base64 import b64encode
from statistics import median, mode
from typing import Sequence, Union

import pandas as pd
from scipy import stats

from stats_app.plotting import get_graphs

distribution_data = pd.read_csv(
    "data/distributions.csv", index_col="distribution"
)

distribution_functions = {
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
    "Negative Binomial": stats.nbinom,
}


def resolve_integer_or_float(
    numbers: list, *, threshold: float = 1e-6
) -> list:
    """Cast float values to integers if their fractional parts are close to
    zero. Round float values to 4 decimal places.

    Args:
        numbers (list): A list of float values.
        threshold (float, optional): Maximum size of the fractional part to
            consider 'similar to zero'. Defaults to 1e-6.

    Returns:
       list: A list of numbers, appropriately transformed.
    """
    return [
        int(number) if number % 1 < 1e-6 else round(number, 4)
        for number in numbers
    ]


def get_descriptive_stats(data: pd.Series) -> dict:
    """Calculate descriptive statistics for the supplied `data`.

    Args:
        data (pd.Series): An array of the values to summarise.

    Returns:
        dict: A dictionary of summary statistics.
    """
    stats = [
        "Mean",
        "Standard Deviation",
        "Minimum",
        "Maximum",
        "Median",
        "Mode",
    ]
    values = resolve_integer_or_float(
        [
            data.mean(),
            data.std(),
            data.min(),
            data.max(),
            median(data),
            mode(data),
        ]
    )
    return dict(zip(stats, values))


def process_parameters(distribution: str, param_list: list) -> list:
    """Modify supplied parameters to ensure that they are valid arguments for
    the `distribution`.

    Args:
        distribution (str): The type of probability distribution.
        param_list (list): A list of parameter values.

    Returns:
        list: A list of parameter values.
    """
    param_list = resolve_integer_or_float(param_list)

    if distribution in {"Bernoulli", "Geometric"}:
        # Probability must be in interval [0, 1]
        return param_list if 0 <= param_list[0] <= 1 else [0.5]
    elif distribution in {"Binomial", "Negative Binomial"}:
        n = round(param_list[0])  # number of trials must be an integer
        probability = param_list[1] if 0 <= param_list[1] <= 1 else 0.5
        return [n, probability]
    else:
        return param_list


def process_random_sample(
    distribution: str, size: int, parameters: Sequence
) -> dict:
    """Generate a random sample of the specified distribution, plot its values
    and calculate summary statistics.

    Args:
        distribution (str): The type of probability distribution.
        size (int): The desired sample size.
        parameters (Sequence): Distribution-specific parameters.

    Returns:
        dict: A dictionary with the sample's properties and graphs.
    """
    parameters = process_parameters(distribution, parameters)
    parameter_info = distribution_data.at[distribution, "parameter_info"]

    sample = pd.Series(
        distribution_functions[distribution].rvs(*parameters, size=size),
        name=f"{distribution} distribution sample",
    ).round(7)
    sample_as_bytes = sample.to_csv(index=False).encode("utf-8")

    return {
        "distribution": distribution,
        "sample": b64encode(sample_as_bytes),
        "preview": sample.head(10),
        "graphs": get_graphs(sample),
        "summary_statistics": get_descriptive_stats(sample),
        "parameters": zip(parameter_info.split(","), parameters),
        "sample_size": size,
    }
