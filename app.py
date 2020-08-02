#!/usr/bin/env python3
# coding: utf-8

from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
from handy_functions import (
    get_random_sample,
    get_graphs,
    descriptive_stats,
    validate_probability,
    clear_old_files,
    Int_float
)
from collections import defaultdict

app = Flask(__name__)

# getting distribution information
data = defaultdict(list)
data['distributions'] = pd.read_csv("data/distributions.csv",
                                    index_col="distribution")


@app.route("/")
def index():
    data['chosen_dist'] = data['graphs'] = None
    return render_template("index.html", data=data, show_intro=True)


@app.route("/parameters", methods=["POST", "GET"])
def parameters():
    if request.method == "POST":
        # extracting form data
        data['chosen_dist'] = request.form["chosen_dist"]
        data['dist_info'] = data['distributions'].loc[data['chosen_dist']]
        data['graphs'] = None
        input_form = True
        if data['chosen_dist'] == "Please Select":
            input_form = False

        return render_template("index.html", data=data, _form=input_form)

    return redirect(url_for("index"))


@app.route("/distribution", methods=["POST", "GET"])
def selection():
    if request.method == "POST":
        # redirect to home page if no distribution is selected
        if not data['chosen_dist']:
            return redirect(url_for('index'))

        # extracting form data
        data['sample_size'] = int(request.form["sample_size"])
        data['parameters'] = \
            [Int_float(float(request.form[f"parameter {i + 1}"]))
             for i in range(data['dist_info']["no_of_parameters"])]
        # ensuring 0<=p<=1 for affected distributions
        if data['chosen_dist'] in {"Negative Binomial", "Binomial",
                                   "Geometric", "Bernoulli"}:
            # probability(p) is the rightmost parameter
            data['parameters'][-1] = \
                validate_probability(data['parameters'][-1])

        # creating and processing the sample
        random_sample = get_random_sample(
            data['chosen_dist'], data['sample_size'], *data['parameters'])
        data['graphs'] = get_graphs(random_sample)
        data['summary_stats'] = descriptive_stats(random_sample)
        sample_data = pd.Series(random_sample,
                                name=data['chosen_dist'] + " distribution")

        # generating a preview
        if len(sample_data) > 0:
            preview = sample_data.head(20).round(7)
        else:
            preview = []

        # exporting the sample to csv file available for download
        clear_old_files("csv")  # removes previously saved samples
        sample_name = data['chosen_dist'] + "_sample_data.csv"
        sample_data.to_csv("static/files/" + sample_name, index=False)
        return render_template("index.html", data=data, preview=preview,
                               sample_name=sample_name
                               )
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
