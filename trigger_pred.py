#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 20:52:56 2018

@author: eric.hensleyibm.com
"""

import pandas as pd
import lightgbm as lgb
from gp import bayesian_optimisation
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from matplotlib import pyplot as plt

#from sklearn.model_selection import learning_curve

data = pd.read_csv('chemistry_data.csv')

del data['Unnamed: 0']
x_feats = list(data)
x_feats.remove('chemistry')


#train_sizes, train_scores, valid_scores = learning_curve(model, data[x_feats], data['chemistry'], train_sizes=[10000, 25000, 45000], cv=5)


def sample_loss(parameters):
    trees = int(round(parameters[0],0))
#    trees = 10
    model = lgb.LGBMRegressor(random_state = 1108, n_estimators = trees)
    score = cross_val_score(model, data[x_feats], data['chemistry'], scoring = 'explained_variance' ,cv = KFold(random_state = 46))
    return np.mean(score)

bounds = np.array([[5, 200]])
#start = [[.1, 2.5, 50, 0.25]]
start = [[ 50.64148649]]
results = bayesian_optimisation(n_iters=25,  
                      sample_loss=sample_loss, 
                      bounds=bounds,
                      x0 = start)

plt.plot(results[1])
if list(results[1]).index(max(results[1])) == 0:
    print('no improvement')
else:
    print(  results[0][list(results[1]).index(max(results[1]))] )