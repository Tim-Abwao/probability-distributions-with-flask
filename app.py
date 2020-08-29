#!/usr/bin/env python3
# coding: utf-8

from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
from handy_functions import (
    get_random_sample,
    get_graphs,
    descriptive_stats,
    clear_old_files
)
from collections import defaultdict

app = Flask(__name__)

data = defaultdict(list)
data['distributions'] = pd.read_csv("data/distributions.csv",
                                    index_col="distribution")


@app.route("/")
def index():
    """Homepage with distribution-selecting menu."""
    data['chosen_dist'] = data['graphs'] = None
    return render_template("index.html", data=data, show_intro=True)


@app.route("/parameters", methods=["POST", "GET"])
def parameters():
    """
    Parameters page with a brief description of selected distribution, a
    distribution-selecting menu, and parameter-collecting forms.
    """
    if request.method == "POST":
        data['chosen_dist'] = request.form["chosen_dist"]
        data['dist_info'] = data['distributions'].loc[data['chosen_dist']]
        data['graphs'] = None

        # Hide parameter input form if no distribution is specified
        input_form = False if data['chosen_dist'] == "Please Select" else True

        return render_template("index.html", data=data, _form=input_form)

    return redirect(url_for("index"))


@app.route("/distribution", methods=["POST", "GET"])
def selection():
    """
    Results page with graphs, descriptive statistics, and a preview of the
    generated sample.
    """
    if request.method == "POST":
        # Redirect to homepage if no distribution is selected
        if not data['chosen_dist']:
            return redirect(url_for('index'))

        data['sample_size'] = int(request.form["sample_size"])
        params = [float(request.form[f"parameter {param + 1}"])
                  for param in range(data['dist_info']["no_of_parameters"])]
        data['parameters'] = params
        random_sample = get_random_sample(distribution=data['chosen_dist'],
                                          size=data['sample_size'],
                                          parameters=data['parameters'])
        data['graphs'] = get_graphs(random_sample)
        data['summary_stats'] = descriptive_stats(random_sample)
        sample_data = pd.Series(random_sample,
                                name=f"{data['chosen_dist']}_distribution")
        preview = sample_data.head(20).round(4)

        clear_old_files("csv")
        sample_name = f"static/files/{data['chosen_dist']}_sample_data.csv"
        sample_data.to_csv(sample_name, index=False)

        return render_template("index.html", data=data, preview=preview,
                               sample_name=sample_name)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
