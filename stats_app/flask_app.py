from collections import defaultdict

import pandas as pd
from flask import Flask, redirect, render_template, request, url_for

from stats_app.utils import clear_old_files, process_random_sample


app = Flask(__name__)


data = defaultdict(list)
data['distributions'] = pd.read_csv("data/distributions.csv",
                                    index_col="distribution")
data['chosen_dist'] = None


@app.route("/")
def index():
    """Homepage."""
    return render_template("index.html", data=data['distributions'])


@app.route("/summary", methods=["POST", "GET"])
def summary():
    """
    Display a brief summary of the selected distribution, and set its
    parameters.
    """
    if request.method == "POST":
        data['chosen_dist'] = request.form["chosen_dist"]
        data['dist_info'] = data['distributions'].loc[data['chosen_dist']]

        return render_template("summary.html", data=data, set_params=True)

    return redirect(url_for("index"))


@app.route("/sample_results", methods=["POST", "GET"])
def sample_results():
    """
    Show graphs, descriptive statistics, and a preview of the generated sample.
    """
    if request.method == "POST":
        if not data['chosen_dist']:  # If no distribution is currently selected
            redirect(url_for('index'))

        data['sample_size'] = int(request.form["sample_size"])
        data['parameters'] = [
            float(request.form[f"parameter {param + 1}"])
            for param in range(data['dist_info']["no_of_parameters"])
        ]
        random_sample, data['graphs'], data['summary_stats'] = \
            process_random_sample(distribution=data['chosen_dist'],
                                  size=data['sample_size'],
                                  parameters=data['parameters'])

        sample_data = pd.Series(random_sample,
                                name=f"{data['chosen_dist']}_distribution")
        clear_old_files("csv")
        sample_filename = f"{data['chosen_dist']}_sample_data.csv"
        sample_data.to_csv(f"stats_app/static/{sample_filename}",
                           index=False)
        data['preview'] = sample_data.head(20).round(4)
        data['sample_name'] = sample_filename

        return render_template("results.html", data=data)

    return redirect(url_for("index"))
