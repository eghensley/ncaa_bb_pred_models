import pandas as pd
import lightgbm as lgb
from gp import bayesian_optimisation
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from matplotlib import pyplot as plt
from sklearn.gaussian_process.kernels import RBF, RationalQuadratic, ExpSineSquared, Matern
data = pd.read_csv('chemistry_data.csv')

del data['Unnamed: 0']
x_feats = list(data)
x_feats.remove('chemistry')
def check_lr(lr, x, y):
    scores = []
    for tree in [50, 100, 150]:
        test = lgb.LGBMRegressor(random_state = 1108, n_estimators = tree, subsample = .8, learning_rate = lr)
        score = cross_val_score(test, x, y, scoring = 'explained_variance' ,cv = KFold(n_splits = 5, random_state = 46))
        scores.append(np.mean(score))
    return scores.index(max(scores))

def find_lr(start_lr, x, y):
    last = None
    while start_lr:
        x = check_lr(start_lr, x, y)
        if x == 0:
            if last == 2:
                learn_rate = np.mean([start_lr, start_lr /2])
                print('Learning Rate: %s' % (learn_rate))
                start_lr = False
            else:
                start_lr /= 2
        elif x==1:
            learn_rate = start_lr
            print('Learning Rate: %s' % (learn_rate))
            start_lr = False
        elif x==2:
            if last == 0:
                learn_rate = np.mean([start_lr, start_lr/2])
                print('Learning Rate: %s' % (learn_rate))
                start_lr = False
            else:
                start_lr *= 2
        last = x
    return learn_rate


learn_rate = find_lr(.01, data[x_feats], data['chemistry'])
model = lgb.LGBMRegressor(random_state = 1108, n_estimators = 100, subsample = .8, learning_rate = learn_rate)
model.fit(data[x_feats], data['chemistry'])
sigs = model.feature_importances_
indices = np.argsort(sigs)[::-1]
feat_sigs = [x_feats[i-1] for i in indices]

def sample_loss_n_feats(parameters):
    feats = int(parameters[0])
    model = lgb.LGBMRegressor(random_state = 1108, n_estimators = 100, subsample = .8, learning_rate = learn_rate)
    score = cross_val_score(model, data[feat_sigs[:feats]], data['chemistry'], scoring = 'explained_variance' ,cv = KFold(n_splits = 5, random_state = 46))
    print(np.mean(score))
    return np.mean(score)

def find_feats():
    bounds = np.array([[10, 100]])
    start = [[70]]
    results = bayesian_optimisation(n_iters=20,  
                          sample_loss=sample_loss_n_feats, 
                          bounds=bounds,
                          x0 = start,
                          gp_params = {'kernel': Matern(), 'alpha': 1e-5, 'n_restarts_optimizer': 10, 'normalize_y': True})
    return int(results[0][list(results[1]).index(max(results[1]))])
feats = find_feats()
new_learn_rate = find_lr(.01, data[feat_sigs[:feats]], data['chemistry'])




result_list = []
params_list = []
right = .2
for ker in [RBF(), RationalQuadratic(), ExpSineSquared(), Matern()]:
    bounds = np.array([[10, 100]])
    start = [[100]]
    results = bayesian_optimisation(n_iters=10,  
                          sample_loss=sample_loss, 
                          bounds=bounds,
                          x0 = start,
                          gp_params = {'kernel': Matern(), 'alpha': 1e-5, 'n_restarts_optimizer': 10, 'normalize_y': True})
    plt.plot(results[1], label = ker)
    plt.legend(bbox_to_anchor = (2, right))
    right += .2
    print('kernel: %s, score: %s' % (ker, max(results[1]))) 
    result_list.append(results[1])
    params_list.append(results[0])
# exsine x