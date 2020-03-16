#!/usr/bin/env python3
# coding: utf-8
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from handy_functions import default_prob, get_random_sample, get_graph, descr_stats

app=Flask(__name__)

#get the distribution-info file
df=pd.read_csv('data/distributions.csv', index_col='distribution')

distributions=list(df.index) # a list of the distribution names
q=len(distributions)
distr='Please Select'  #initial choice of distribution before overwriting by form-data

@app.route('/')
def index():
	return render_template('index.html', distributions=distributions, q=q, show_intro=True)

@app.route('/parameters', methods=['POST', 'GET'])
def parameters():
	if request.method=='POST':
		#extract form-data
		distr=request.form['statdist']

		#save selected distribution for future reference
		with open('data/current_selection.txt', 'w') as f:
			f.write(distr)

		num_params=df.at[distr,'nparams']	
		param_def=df.at[distr,'param_def'].split(',') 
		info=df.at[distr, 'summary'].split('|')

		return render_template('index.html', d=distr, distributions=distributions,q=q, num_params=num_params, param_def=param_def, info=info)

@app.route('/distribution', methods=['POST', 'GET'])
def selection():
	if request.method=='POST':
		#extract form data
		n=int(request.form['sample_size'])

		with open('data/current_selection.txt', 'r') as fp:
			distr=fp.read()
			
		nparams=df.at[distr,'nparams']
		parameters=[float(request.form['par '+str(i+1)]) for i in range(nparams)]
		param_def=df.at[distr,'param_def'].split(',')
		
		#ensure 0<=p<=1 for affected distributions
		if distr in ['Negative Binomial','Binomial','Geometric','Bernoulli']:
			if parameters[-1]>1:
				parameters[-1]=default_prob(parameters[-1])

		#create and process the sample
		random_sample=get_random_sample(distr, n, parameters)
		graph=get_graph(random_sample)
		summary_stats=descr_stats(random_sample)
		title= distr + ' distribution'
		df2=pd.DataFrame({ title: random_sample})
		
		#create preview
		if len(df2)>0:
			preview=list(df2[title].round(7).head(20))
			preview=enumerate(preview, start=1)
		else: preview=False
		
		#create csv file for download
		df2.to_csv('static/files/data.csv')

		return render_template('index.html',d=distr, distributions=distributions, q=q, parameters=parameters, param_def=param_def, nparams=nparams, n=n, graph=graph, summary_stats=summary_stats, preview=preview)

if __name__=='__main__':
	app.run(debug=True)
