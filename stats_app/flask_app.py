from typing import Union

from flask import Flask, Response, redirect, render_template, request, url_for

from stats_app.stats_functions import distribution_data, process_random_sample

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """The home page.

    Returns:
        str: HTML text.
    """
    return render_template("index.html", data=distribution_data)


@app.route("/summary", methods=["POST", "GET"])
def summary() -> Union[str, Response]:
    """Display a brief summary of the selected distribution, and collect
    parameter input values.

    Returns:
        Union[str, Response]: HTML text if the method is POST, or a response
            redirecting to the home-page otherwise.
    """
    if request.method == "POST":
        # Get selected distribution
        current_distribution = request.form["chosen_dist"]
        current_distribution_data = distribution_data.loc[current_distribution]

        return render_template("summary.html", data=current_distribution_data)

    return redirect(url_for("index"))


@app.route("/sample_results", methods=["POST", "GET"])
def sample_results() -> Union[str, Response]:
    """Display graphs, descriptive statistics, and a preview of the generated
    sample.

    Returns:
        Union[str, Response]: HTML text if the method is POST, or a response
            redirecting to the home-page otherwise.
    """
    if request.method == "POST":
        # Collect info & parameters from the submitted form
        param_dict = dict(request.form)
        current_distribution = param_dict.pop("current-distribution")
        sample_size = int(param_dict.pop("sample_size"))
        parameters = map(float, param_dict.values())

        # Create and process the sample using specified parameters
        sample_results = process_random_sample(
            distribution=current_distribution,
            size=sample_size,
            parameters=parameters,
        )

        return render_template("results.html", data=sample_results)

    return redirect(url_for("index"))
