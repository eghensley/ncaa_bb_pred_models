#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 09:35:17 2018

@author: eric.hensleyibm.com
"""

import numpy as np
import math 
from gp import bayesian_optimisation
from matplotlib import pyplot as plt
import singlegamestats 

stat = 'rebounding'
fa = 'allow'
pastdata = singlegamestats.pull_targets_train(stat)
data = singlegamestats.pull_targets_test(stat, fa)
data=data.dropna(how='any')

def sample_loss(parameters):
    print(parameters)
    hf, pwr, shrink, adj = parameters
    all_s1_error = []
    all_s2_error = []
    fordict = {}
    for i in range(0, len(pastdata['name'])):
        if math.isnan(pastdata['for'][i]):
            fordict[pastdata['name'][i]] = np.mean(pastdata['for']) - (np.std(pastdata['for']) * 1.5)
        else:
            fordict[pastdata['name'][i]] = pastdata['for'][i]
    againstdict = {}
    for i in range(0, len(pastdata['name'])):
        if math.isnan(pastdata['against'][i]):
            againstdict[pastdata['name'][i]] = np.mean(pastdata['for']) + (np.std(pastdata['for']) * 1.5)
        else:
            againstdict[pastdata['name'][i]] = pastdata['against'][i]
    season = np.array(data['date'])[0].year
    for date, t1, t2, s1, s2, loc in np.array(data)[:1]:
        if date.month == 11 and date.year > season:
            fordictmean = np.mean(list(fordict.values()))
            againstdictmean = np.mean(list(againstdict.values()))
            for key in fordict.keys():
                fordict[key] = fordict[key] + (fordictmean - fordict[key])*adj
            for key in againstdict.keys():
                againstdict[key] = againstdict[key] + (againstdictmean - againstdict[key])*adj
            season += 1
        if loc == 1:
             loc = -1
        elif loc == 0:
             loc = 1
        s1_exp = (fordict[t1]+againstdict[t2])/2 + (loc * hf)
        s2_exp = (fordict[t2]+againstdict[t1])/2 - (loc * hf)
        s1_error = (s1 - s1_exp)/s1_exp
        s2_error = (s2 - s2_exp)/s2_exp
        all_s1_error.append(math.fabs(s1_error))
        all_s2_error.append(math.fabs(s2_error))
        if math.isnan(fordict[t1] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink):
            break
        else:
            fordict[t1] = fordict[t1] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink
        if math.isnan(againstdict[t2] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink):
            break
        else:
            againstdict[t2] = againstdict[t2] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink
        fordict[t2] = fordict[t2] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink
        againstdict[t1] = againstdict[t1] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink    
    
    errors = (np.array(all_s1_error)+np.array(all_s2_error))/2
    avg_error = np.mean(errors)
    print(avg_error)
    return avg_error

bounds = np.array([[0,.01], [0, 5], [10, 100], [.1, .3]])
start = [[.00501013359, 2.64145612, 20.12802666, 0.17893941]]
results = bayesian_optimisation(n_iters=30,  
                      sample_loss=sample_loss, 
                      bounds=bounds,
                      x0 = start)

plt.plot(results[1])

results[0][list(results[1]).index(min(list(results[1])))]
