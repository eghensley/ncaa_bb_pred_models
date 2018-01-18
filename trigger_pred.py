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
from sklearn.gaussian_process.kernels import RBF, RationalQuadratic, ExpSineSquared, Matern

#from sklearn.model_selection import learning_curve

data = pd.read_csv('chemistry_data.csv')

del data['Unnamed: 0']
x_feats = list(data)
x_feats.remove('chemistry')

model = lgb.LGBMRegressor(random_state = 1108, n_estimators = 74)
model = lgb.LGBMRegressor(random_state = 1108, n_estimators = 50)
model.fit(data[x_feats], data['chemistry'])
sigs = model.feature_importances_
indices = np.argsort(sigs)[::-1]
feat_sigs = [x_feats[i-1] for i in indices]

def sample_loss(parameters):
#    tree_sample = parameters[0]
#    bin_max = int(parameters[1])
#    child_samples = int(parameters[2])
#    leaves = int(parameters[3])
#    sample = parameters[4]
    trees = int(parameters[0])
    feats = int(parameters[1])
    model = lgb.LGBMRegressor(random_state = 1108, n_estimators = trees, colsample_bytree = .97649, min_child_samples = 1, num_leaves = 35, subsample = .8288, max_bin = 1655)
    score = cross_val_score(model, data[feat_sigs[:feats]], data['chemistry'], scoring = 'explained_variance' ,cv = KFold(n_splits = 5, random_state = 46))
    print(np.mean(score))
    return np.mean(score)

#bounds = np.array([[.8, 1], [1000, 2000], [1, 50], [10, 100], [.4, 1]])
#start = [[ .97649, 1655, 1, 35, .8288]]

bounds = np.array([[100, 150], [50, 100]])
start = [[124, 88]]
results = bayesian_optimisation(n_iters=50,  
                      sample_loss=sample_loss, 
                      bounds=bounds,
                      x0 = start)
plt.plot(results[1])


fig, ax1 = plt.subplots()
s0 = []
s1 = []
for i, j in results[0]:
    s0.append(i)
    s1.append(j)
ax1.plot(s1, 'b-')
ax1.plot(s0, 'b:')
ax1.set_xlabel('iteration')
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('trees', color='b')
ax2 = ax1.twinx()
s2 = results[1]
ax2.plot(s2, 'r-')
ax2.set_ylabel('explained variance', color='r')
fig.tight_layout()
plt.show()

#0.767289335287, 0.784977119309, 0.825566840384, 0.828842337602

if list(results[1]).index(max(results[1])) == 0:
    print('no improvement')
else:
    print(  results[0][list(results[1]).index(max(results[1]))] )
    
print(max(results[1]))