#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import datetime
from statistics import mean,median,stdev,mode

def default_prob(p):
    """
    Ensuring probabilities stick to range 0<=p<=1 by assigning default p=0.5 for values over 1
    """
    if p > 1:
        p=0.5 
    return p

def get_random_sample(distribution,size,parameters):
    """
    Return a random sample of size {size} with the given parameter(s) for the specified distribution.
    """
    params=list(parameters)
    
    if distribution=='Normal':
        from scipy.stats import norm
        sampl = norm.rvs(params[0],params[1], size=size)
        return sampl

    if distribution=='Poisson':
        from scipy.stats import poisson
        sampl=poisson.rvs(params[0] ,size=size)
        return sampl

    if distribution=='Bernoulli':
        from scipy.stats import bernoulli
        sampl=bernoulli.rvs(params[0], size=size)
        return sampl

    if distribution=='Uniform':
        from scipy.stats import uniform
        sampl=uniform.rvs(params[0],params[1],size=size)
        return sampl

    if distribution=='Geometric':
        from scipy.stats import geom
        sampl=geom.rvs(params[0],size=size)
        return sampl

    if distribution=='Alpha':
        from scipy.stats import alpha
        sampl=alpha.rvs(params[0], size=size)
        return sampl

    if distribution=='Beta':
        from scipy.stats import beta
        sampl=beta.rvs(params[0], params[1],size=size)
        return sampl

    if distribution=='Chi-squared':
        from scipy.stats import chi2
        sampl=chi2.rvs(params[0], size=size)
        return sampl

    if distribution=='Exponential':
        from scipy.stats import expon
        sampl=expon.rvs(params[0],size=size)
        return sampl

    if distribution=='F':
        from scipy.stats import f
        sampl=f.rvs(params[0],params[1], size=size)
        return sampl

    if distribution=='Gamma':
        from scipy.stats import gamma
        sampl=gamma.rvs(params[0],size=size)
        return sampl

    if distribution=='Pareto':
        from scipy.stats import pareto
        sampl=pareto.rvs(params[0], size=size)
        return sampl

    if distribution=='Student t':
        from scipy.stats import t
        sampl=t.rvs(params[0], size=size)
        return sampl

    if distribution=='Binomial':
        from scipy.stats import binom
        sampl=binom.rvs(round(params[0]),params[1], size=size)
        return sampl

    if distribution=='Negative Binomial':
        from scipy.stats import nbinom
        sampl=nbinom.rvs(round(params[0]), params[1],size=size)
        return sampl
    return 1


def get_graph(data):
    """
    Plot a distribution plot of the random sample and save it as a png image file
    """

    #remove old graphs
    old_files=glob.glob('static/files/*.png', recursive=True)
    for fl in old_files:
        os.remove(fl)
    #create new time-defined name for the graph file
    new_path='files/'+str(datetime.datetime.now())+'.png'
    
    plt.figure(figsize=(10,6))
    sns.set()
    sns.distplot(data, color='teal')
    plt.xticks(rotation=90)
    plt.savefig('static/'+ new_path, transparent=True)
    
    return new_path

def descr_stats(random_sample):
    """
    Get descriptive statistics for the random sample
    """
    #handle instances of missing/insufficient data
    try:
        mu=round(mean(random_sample),4)
        med=round(median(random_sample),4)
    except ValueError:
        med=mu='No data to process.'
     
    try:
        std=round(stdev(random_sample),4)
        mi=round(min(random_sample),4)
        ma=round(max(random_sample),4)
    except ValueError:
        std=mi=ma= 'Not available. At least 2 data points required.'
    
    try: 
        mod=round(mode(random_sample),4)
    except ValueError:
        mod='No unique mode.'
    return [('Mean: ',mu),('Median: ',med),('Mode: ',mod),('Min: ',mi),('Max: ',ma),('Standard Deviation: ',std)]





