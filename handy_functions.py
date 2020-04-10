#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import datetime
from statistics import mean,median,stdev,mode

def validate_probability(p):
    """
    Ensures probabilities stick to the range 0<=p<=1 by assigning a default value of p=0.5 for entries greater than 1
    """
    if 0 <= p <= 1:
        return p
    else:
        return 0.5

def get_random_sample(distribution,size,parameters):
    """
    Returns a random sample of size {size} with the given {parameters}, for the specified {distribution}.
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

def clear_old_files(extension):
    old_files=glob.glob('static/files/*.'+extension, recursive=True)
    for file in old_files:
        os.remove(file)

def get_graph(data):
    """
    Plots a distribution graph of the random sample and saves it to a png file
    """
    #clear old graphs
    clear_old_files('png')
    #create time-stamped name for the graph image
    new_name=str(datetime.datetime.now())+'.png'
    plt.figure(figsize=(10,6))
    sns.set()
    sns.distplot(data, color='teal')
    plt.xticks(rotation=90)
    plt.savefig('static/files/'+ new_name, transparent=True)
    return new_name

def descriptive_stats(random_sample):
    """
    Returns basic descriptive statistics for the random sample
    """
    try:
        _mean=round(mean(random_sample),4)
        _median=round(median(random_sample),4)
    except ValueError:
        _median=_mean='No data to process.'
     
    try:
        std=round(stdev(random_sample),4)
        _min=round(min(random_sample),4)
        _max=round(max(random_sample),4)
    except ValueError:
        std=_min=_max= 'Not available. At least 2 data points required.'
    
    try: 
        _mode=round(mode(random_sample),4)
    except ValueError:
        _mode='No unique mode.'
    return [('Mean: ',_mean),('Median: ',_median),('Mode: ',_mode),('Min: ',_min),('Max: ',_max),('Standard Deviation: ',std)]