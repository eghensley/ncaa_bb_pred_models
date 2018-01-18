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
    score = cross_val_score(model, data[feat_sigs[:feats]], data['chemistry'], scoring = 'explained_variance' ,cv = KFold(n_splits = 5, random_state = 46), n_jobs = -1)
    print(np.mean(score))
    return np.mean(score)

result_list = []
params_list = []
for ker in [RBF(), RationalQuadratic(), ExpSineSquared(), Matern()]:
    bounds = np.array([[10, 100]])
    start = [[100]]
    results = bayesian_optimisation(n_iters=5,  
                          sample_loss=sample_loss, 
                          bounds=bounds,
                          x0 = start,
                          gp_params = {'kernel': ker, 'alpha': 1e-5, 'n_restarts_optimizer': 10, 'normalize_y': True})
    plt.plot(results[1])
    result_list.append(results[1])
    params_list.append(results[0])