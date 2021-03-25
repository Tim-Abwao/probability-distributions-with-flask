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
    data['chosen_dist'] = data['graphs'] = None
    return render_template("index.html", data=data, show_intro=True)


@app.route("/description", methods=["POST", "GET"])
def description():
    """
    Display a brief description of the selected distribution, and set its
    parameters.
    """
    if request.method == "POST":
        data['chosen_dist'] = request.form["chosen_dist"]
        data['dist_info'] = data['distributions'].loc[data['chosen_dist']]
        data['graphs'] = None

        # Hide parameter input form if no distribution is specified
        input_form = False if data['chosen_dist'] == "Please Select" else True

        return render_template("index.html", data=data, _form=input_form)

    return redirect(url_for("index"))


@app.route("/results", methods=["POST", "GET"])
def results():
    """
    Show graphs, descriptive statistics, and a preview of the generated sample.
    """
    if request.method == "POST":
        # Redirect to description page if no distribution is selected
        if not data['chosen_dist']:
            return redirect(url_for('description'))

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
        preview = sample_data.head(20).round(4)

        clear_old_files("csv")
        sample_filename = f"{data['chosen_dist']}_sample_data.csv"
        sample_data.to_csv(f"stats_app/static/{sample_filename}",
                           index=False)

        return render_template("index.html", data=data, preview=preview,
                               sample_name=sample_filename)

    return redirect(url_for("index"))
