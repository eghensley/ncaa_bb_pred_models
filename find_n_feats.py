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

model = lgb.LGBMRegressor(random_state = 1108, n_estimators = 100)
model.fit(data[x_feats], data['chemistry'])
sigs = model.feature_importances_
indices = np.argsort(sigs)[::-1]
feat_sigs = [x_feats[i-1] for i in indices]

def sample_loss(parameters):
    feats = int(parameters[0])
    model = lgb.LGBMRegressor(random_state = 1108, n_estimators = 100)
    score = cross_val_score(model, data[feat_sigs[:feats]], data['chemistry'], scoring = 'explained_variance' ,cv = KFold(n_splits = 5, random_state = 46))
    print(np.mean(score))
    return np.mean(score)

result_list = []
params_list = []
right = .2
for ker in [RBF(), RationalQuadratic(), ExpSineSquared(), Matern()]:
    bounds = np.array([[10, 100]])
    start = [[100]]
    results = bayesian_optimisation(n_iters=2,  
                          sample_loss=sample_loss, 
                          bounds=bounds,
                          x0 = start,
                          gp_params = {'kernel': ker, 'alpha': 1e-5, 'n_restarts_optimizer': 10, 'normalize_y': True})
    plt.plot(results[1], label = ker)
    plt.legend(bbox_to_anchor = (2, right))
    right += .2
    print('kernel: %s, score: %s' % (ker, max(results[1]))) 
    result_list.append(results[1])
    params_list.append(results[0])