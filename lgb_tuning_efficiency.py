import pandas as pd
import lightgbm as lgb
from gp import bayesian_optimisation
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from matplotlib import pyplot as plt
from sklearn.gaussian_process.kernels import RBF, RationalQuadratic, ExpSineSquared, Matern
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.pipeline import Pipeline
data = pd.read_csv('shooting_efficiency.csv')

del data['Unnamed: 0']
x_feats = list(data)
x_feats.remove('shooting-efficiency')

def test_scaler(x, y):
    scores = []
    for scale in [StandardScaler(), MinMaxScaler(), RobustScaler()]:
        pipe = Pipeline([('scale',scale), ('clf',lgb.LGBMRegressor(random_state = 1108))])
        score = cross_val_score(pipe, x, y, scoring = 'explained_variance' ,cv = KFold(n_splits = 5, random_state = 46))
        scores.append(np.mean(score))
    if scores.index(max(scores)) == 0:
        print('Using Standard Scaler')
        return StandardScaler()
    elif scores.index(max(scores)) == 1:
        print('Using Min Max Scaler')
        return MinMaxScaler()
    elif scores.index(max(scores)) == 2:
        print('Using Robust Scaler')
        return RobustScaler()

def check_lr(lr, x, y, scale):
    scores = []
    for tree in [50, 100, 150]:
        test = Pipeline([('scale',scale), ('clf',lgb.LGBMRegressor(random_state = 1108, n_estimators = tree, subsample = .8, learning_rate = lr))])
        score = cross_val_score(test, x, y, scoring = 'explained_variance' ,cv = KFold(n_splits = 5, random_state = 46))
        scores.append(np.mean(score))
    return scores.index(max(scores))

def find_lr(start_lr, x_, y, scale):
    last = None
    while start_lr:
        x = check_lr(start_lr, x_, y, scale)
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

def sample_loss_n_feats(parameters):
    feats = int(parameters[0])
    model = Pipeline([('scale',scale), ('clf',lgb.LGBMRegressor(random_state = 1108, n_estimators = 100, subsample = .8, learning_rate = learn_rate))])
    score = cross_val_score(model, data[feat_sigs[:feats]], data['shooting-efficiency'], scoring = 'explained_variance' ,cv = KFold(n_splits = 5, random_state = 46))
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

def sample_loss_hyperparameters(parameters):
    tree_sample = parameters[0]
    bin_max = int(parameters[1])
    child_samples = int(parameters[2])
    leaves = int(parameters[3])
    sample = parameters[4]
    model = Pipeline([('scale',scale), ('clf',lgb.LGBMRegressor(random_state = 1108, n_estimators = 100, colsample_bytree = tree_sample, min_child_samples = child_samples, num_leaves = leaves, subsample = sample, max_bin = bin_max, learning_rate = new_learn_rate))])
    score = cross_val_score(model, data[feat_sigs[:features]], data['shooting-efficiency'], scoring = 'explained_variance' ,cv = KFold(n_splits = 5, random_state = 46))
    print(np.mean(score))
    return np.mean(score)
 
def hyper_parameter_tuning():
    result_list = []
    params_list = []
    right = .2
    for ker in [RBF(), RationalQuadratic(), ExpSineSquared(), Matern()]:
        bounds = np.array([[.6, 1], [1000, 2000], [1, 100], [10, 200], [.4, 1]])
        start = [[ .8, 1655, 1, 35, .8]]
        results = bayesian_optimisation(n_iters=100,  
                              sample_loss=sample_loss_hyperparameters, 
                              bounds=bounds,
                              x0 = start,
                              gp_params = {'kernel': ker, 'alpha': 1e-5, 'n_restarts_optimizer': 10, 'normalize_y': True})
        plt.plot(results[1], label = ker)
        plt.legend(bbox_to_anchor = (2, right))
        right += .2
        print('kernel: %s, score: %s' % (ker, max(results[1]))) 
        result_list.append(results[1])
        params_list.append(results[0])
    return result_list, params_list
    
scale = test_scaler(data[x_feats], data['shooting-efficiency'])
learn_rate = find_lr(.01, data[x_feats], data['shooting-efficiency'], scale)
model = lgb.LGBMRegressor(random_state = 1108, n_estimators = 100, subsample = .8, learning_rate = learn_rate)
model.fit(scale.fit_transform(data[x_feats]), data['shooting-efficiency'])
sigs = model.feature_importances_
indices = np.argsort(sigs)[::-1]
feat_sigs = [x_feats[i-1] for i in indices]
features = find_feats()
new_learn_rate = find_lr(.01, data[feat_sigs[:features]], data['shooting-efficiency'], scale)
results, params = hyper_parameter_tuning()

