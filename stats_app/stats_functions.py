from base64 import b64encode
from statistics import median, mode

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


def resolve_integer_or_float(*numbers):
    """Cast float values as integers if their fractional parts are close to
    zero.

    Parameters
    ----------
    numbers : sequence
        Number(s) to process.

    Returns
    -------
    A number or list of numbers, appropriately transformed.
    """
    if len(numbers) == 1:
        number = numbers[0]
        return int(number) if number % 1 < 1e-6 else round(number, 4)
    else:
        return [
            int(number) if number % 1 < 1e-6 else round(number, 4)
            for number in numbers
        ]


def get_descriptive_stats(data):
    """Get basic descriptive statistics for the supplied data.

    Parameters
    ----------
    data : numpy.ndarray, pandas.Series
        An array of the values to summarise.

    Returns
    -------
    A dictionary of summary statistics.
    """
    stats = {
        "Mean": data.mean(),
        "Standard Deviation": data.std(),
        "Minimum": data.min(),
        "Maximum": data.max(),
        "Median": median(data),
        "Mode": mode(data),
    }
    return {
        key: resolve_integer_or_float(value) for key, value in stats.items()
    }


def process_parameters(distribution, param_list):
    """Modify parameters supplied to ensure that they are valid arguments for
    the distribution's sample-generating function.

    Parameters
    ----------
    distribution : str
        The name of the probability distribution.
    param_list : list
        A list of parameter values.

    Returns
    -------
    A list of parameter values.
    """
    param_list = resolve_integer_or_float(*param_list)

    if not isinstance(param_list, list):
        param_list = [param_list]

    if distribution in {"Bernoulli", "Geometric"}:
        probability = param_list[0]
        return [probability] if 0 <= probability <= 1 else [0.5]
    elif distribution in {"Binomial", "Negative Binomial"}:
        n = round(param_list[0])  # number of trials must be an integer
        probability = param_list[1] if 0 <= param_list[1] <= 1 else 0.5
        return [n, probability]
    else:
        return param_list


def process_random_sample(distribution, size, parameters):
    """Generate a random sample of the specified distribution, plot its values
    and calculate summary statistics.

    Parameters
    ----------
    distribution : str
        The type of distribution. One of "Normal", "Poisson", "Bernoulli",
        "Uniform", "Geometric", "Alpha", "Beta", "Chi-squared", "Exponential",
        "F", "Gamma", "Pareto", "Student t", "Binomial" or "Negative Binomial".
    size : int
        The desired sample size.
    parameters : sequence
        A list or tuple of distribution-specific parameters.

    Returns
    -------
    A dictionary with the sample's information and graphs.
    """
    parameters = process_parameters(distribution, parameters)
    parameter_info = distribution_data.loc[distribution][
        "parameter_info"
    ].split(",")

    sample = pd.Series(
        distribution_functions[distribution].rvs(*parameters, size=size),
        name=f"{distribution} distribution sample",
    ).round(7)
    sample_bytes = sample.to_csv(index=False).encode("utf-8")

    return {
        "distribution": distribution,
        "sample": b64encode(sample_bytes).decode("utf-8"),
        "preview": sample.head(20),
        "graphs": get_graphs(sample),
        "summary_statistics": get_descriptive_stats(sample),
        "parameters": zip(parameter_info, parameters),
        "sample_size": size,
    }
