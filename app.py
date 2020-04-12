#!/usr/bin/env python3
# coding: utf-8

from flask import (Flask, render_template, request, url_for, redirect)
import pandas as pd
from handy_functions import (get_random_sample, get_graph, descriptive_stats,
                             validate_probability, clear_old_files)

app = Flask(__name__)

# getting the distribution summaries
distribution_data = pd.read_csv('data/distributions.csv',
                                index_col='distribution')
distribution_names = list(distribution_data.index)
tally = len(distribution_names)
default_dist = 'Please Select'  # initial choice of distribution


@app.route('/')
def index():
    return render_template('index.html', distributions=distribution_names,
                           tally=tally, show_intro=True)


@app.route('/parameters', methods=['POST', 'GET'])
def parameters():
    if request.method == 'POST':
        # extracting form data
        chosen_distr = request.form['chosen_dist']

        # save selected distribution for future reference
        with open('data/current_selection.txt', 'w') as file:
            file.write(chosen_distr)

        num_params = distribution_data.at[chosen_distr, 'no_of_parameters']
        param_info = distribution_data.at[chosen_distr, 'parameter_info']
        param_info = param_info.split(',')
        dist_summary = distribution_data.at[chosen_distr, 'summary'].split('|')

        return render_template('index.html', chosen_distr=chosen_distr,
                               tally=tally, num_params=num_params,
                               param_info=param_info, input_form=True,
                               distributions=distribution_names,
                               dist_summary=dist_summary)
    return redirect(url_for('index'))


@app.route('/distribution', methods=['POST', 'GET'])
def selection():
    if request.method == 'POST':
        # extracting form data
        sample_size = int(request.form['sample_size'])

        with open('data/current_selection.txt', 'r') as file:
            chosen_distr = file.read()

        num_params = distribution_data.at[chosen_distr, 'no_of_parameters']
        parameters = [float(request.form['parameter ' + str(i+1)])
                      for i in range(num_params)]
        param_info = distribution_data.at[chosen_distr, 'parameter_info']
        param_info = param_info.split(',')

        # ensuring 0<=p<=1 for affected distributions
        if chosen_distr in ['Negative Binomial', 'Binomial', 'Geometric',
                            'Bernoulli']:
            # p is the rightmost parameter
            parameters[-1] = validate_probability(parameters[-1])

        # creating and processing the sample
        random_sample = get_random_sample(chosen_distr, sample_size,
                                          parameters)
        graph = get_graph(random_sample)
        summary_stats = descriptive_stats(random_sample)
        title = chosen_distr + ' distribution'
        sample_data = pd.DataFrame({title: random_sample})

        # generating a preview
        if len(sample_data) > 0:
            # the preview as a dataframe
            preview = list(sample_data[title].head(20).round(7))
            # the preview as a list of tuples
            preview = enumerate(preview, start=1)
        else:
            preview = False

        # clear old samples
        clear_old_files('csv')

        # creating a csv file for download
        sample_name = chosen_distr + '_sample_data.csv'
        sample_data.to_csv('static/files/' + sample_name)

        return render_template('index.html', chosen_distr=chosen_distr,
                               tally=tally, distributions=distribution_names,
                               param_info=param_info, num_params=num_params,
                               sample_size=sample_size, preview=preview,
                               summary_stats=summary_stats, graph=graph,
                               sample_name=sample_name, parameters=parameters)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
