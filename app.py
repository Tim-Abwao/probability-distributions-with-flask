#!/usr/bin/env python
# coding: utf-8
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from handy_functions import *

app=Flask(__name__)

#get the file distribution info
df=pd.read_csv('data/dist.csv')

dist_list=list(df.distribution) # a list of the distribution names
q=len(dist_list)
distr='Please Select'

@app.route('/')
def index():
	return render_template('index.html', distlist=dist_list, q=q, show_intro=True)

@app.route('/params',  methods=['POST', 'GET'])
def statistics():
	if request.method=='POST':
		#extract form data
		distr=request.form['statdist']

		#save selected distribution for future reference
		with open('data/current_selection.txt', 'w') as f:
			print(distr, file=f)

		indx=dist_list.index(distr) #get index of distribution
		#use index to get selected distribution's info
		num_params=df.at[indx,'nparams']	
		par2=df.at[indx,'param_dim'].split(',') 
		info=df.at[indx, 'summary']
		info=info.split('|')

		return render_template('index.html',d=distr ,distlist=dist_list,q=q, par=num_params, par2=par2, info=info)

@app.route('/distribution', methods=['POST', 'GET'])
def selection():
	if request.method=='POST':
		#extract form data
		n=int(request.form['sample_size'])

		with open('data/current_selection.txt', 'r') as fp:
			d=fp.read()
			d=str(d).strip('\n')
		indx=df.at[dist_list.index(d),'nparams']
		parameters=[float(request.form['par '+str(i+1)]) for i in range(indx) ]
		nparams=len(parameters)
		par3=df.at[dist_list.index(d),'param_dim'].split(',')
		
		#ensure 0<=p<=1 for affected distributions
		if d in ['Negative Binomial','Binomial','Geometric','Bernoulli']:
			if parameters[-1]>1:
				parameters[-1]=default_prob(parameters[-1])

		#create and process the sample
		random_sample=get_random_sample(d,n,parameters)
		y=get_graph(random_sample)
		z=descr_stats(random_sample)
		title= d + ' distribution'
		df2=pd.DataFrame({ title: random_sample})
		if len(df2)>0:
			pw=list(df2[title].head(20))
			pw=[round(a,7) for a in pw ]
			pr=enumerate(pw,start=1)
			preview=True
		else: preview=False
		df2.to_csv('static/files/data.csv')

		return render_template('index.html',d=d, distlist=dist_list, q=q, parameters=parameters, par3=par3, nparams=nparams, n=n, y=y,z=z,preview=preview,pr=pr)

if __name__=='__main__':
	app.run()
