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
    floatInt_to_int
)

app = Flask(__name__)

# getting distribution information
distribution_data = pd.read_csv("data/distributions.csv",
                                index_col="distribution")


@app.route("/")
def index():
    return render_template(
        "index.html", distributions=distribution_data, show_intro=True)


@app.route("/parameters", methods=["POST", "GET"])
def parameters():
    if request.method == "POST":
        # extracting form data
        chosen_distr = request.form["chosen_dist"]
        # persist current selection
        with open("data/current_selection.txt", "w") as file:
            file.write(chosen_distr)

        dist_info = distribution_data.loc[chosen_distr]
        input_form = "A variable to toggle the sample creation form"
        if chosen_distr == "Please Select":
            input_form = False

        return render_template(
            "index.html",
            chosen_distr=chosen_distr,
            dist_info=dist_info,
            distributions=distribution_data,
            input_form=input_form,
        )

    return redirect(url_for("index"))


@app.route("/distribution", methods=["POST", "GET"])
def selection():
    if request.method == "POST":
        # extracting form data
        sample_size = int(request.form["sample_size"])

        # retrieving distribution selected to know no. of parameters
        with open("data/current_selection.txt", "r") as file:
            chosen_distr = file.read()

        dist_info = distribution_data.loc[chosen_distr]
        # obtaining parameters
        parameters = [
            floatInt_to_int(float(request.form["parameter " + str(i + 1)]))
            for i in range(dist_info["no_of_parameters"])
        ]
        # ensuring 0<=p<=1 for affected distributions
        if chosen_distr in {"Negative Binomial", "Binomial",
                            "Geometric", "Bernoulli"}:
            # probability(p) is the rightmost parameter
            parameters[-1] = validate_probability(parameters[-1])

        # creating and processing the sample
        random_sample = get_random_sample(chosen_distr, sample_size,
                                          parameters)
        graphs = get_graphs(random_sample)
        summary_stats = descriptive_stats(random_sample)
        sample_data = pd.Series(random_sample,
                                name=chosen_distr + " distribution")

        # generating a preview
        if len(sample_data) > 0:
            preview = enumerate(sample_data.head(20).round(7).to_numpy())
        else:
            preview = False

        # clear old samples
        clear_old_files("csv")

        # creating a csv file of the sample, for download
        sample_name = chosen_distr + "_sample_data.csv"
        sample_data.to_csv("static/files/" + sample_name, index=False)

        return render_template(
            "index.html",
            chosen_distr=chosen_distr,
            dist_info=dist_info,
            distributions=distribution_data,
            sample_size=sample_size,
            preview=preview,
            summary_stats=summary_stats,
            graphs=graphs,
            sample_name=sample_name,
            parameters=parameters,
        )
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
