#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 18:13:53 2017

@author: eric.hensleyibm.com
"""

from pca_clust import both_clust
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, roc_auc_score
import numpy as np

scorelist = [(9,4,StandardScaler()), (9,5,RobustScaler()), (9,7,RobustScaler()), (18,7,RobustScaler()), (27, 2, MinMaxScaler()), (27,3,MinMaxScaler())]
allowedlist = [(9,7,RobustScaler()), (9,6,RobustScaler()), (12,6,RobustScaler()), (12,7,RobustScaler()), (12, 5, MinMaxScaler()), (9,5,RobustScaler())]

all_mae_score = []
all_r2_score = []
all_mae_allow = []
all_r2_allow = []
all_acc_score = []
all_roc_score = []
all_acc_allow = []
all_roc_allow = []
all_acc_both = []
all_roc_both = []
progress = 0
for score in scorelist:
    for allowed in allowedlist:
        progress += 1
        print("%s percent complete" % ((float(progress)/ (float(len(scorelist) * len(allowedlist)))) * 100))
        scored_feats, scored_clusts, scored_scale = score
        allowed_feats, allowed_clusts, allowed_scale = allowed
        data = both_clust(scored_feats, scored_clusts, scored_scale, allowed_feats, allowed_clusts, allowed_scale)
        reg = LinearRegression()
        score_mae_list = []
        score_r2_list = []
        allow_mae_list = []
        allow_r2_list = []
        score_acc_list = []
        allow_acc_list = []
        both_acc_list = []
        score_roc_list = []
        allow_roc_list = []
        both_roc_list = []
        for rand in [1, 10, 35, 46, 71, 86, 1108, 151, 2726, 100]:
            testindex = None
            trainindex = None
            score_train_y = None
            allowed_train_y = None
            score_test_y = None
            allowed_test_y = None
            score_test_x = None
            allowed_test_x = None
            score_test_y = None
            allowed_test_y = None
            score_train_x = None
            allowed_train_x = None
            allowed_test_x = None
            score_test_x = None
            scored_pred = None
            allowed_pred = None
            scored_mae = None
            allowed_mae = None
            scored_r2 = None
            allowed_r2 = None
            fav_allowed = None
            dog_allowed = None
            dog_scored = None
            fav_scored = None
            fav_points = None
            dog_points = None
            pred_score_fav = None
            pred_score_dog = None
            pred_allowed_fav = None
            pred_allowed_dog = None
            testmargin = None
            pred_margin_score = None
            pred_margin_allowed = None
            pred_margin_both = None
            score_acc = None
            allow_acc = None
            both_acc = None
            score_roc = None
            allow_roc = None
            both_roc = None
            
            scored_reg = LinearRegression()
            allowed_reg = LinearRegression()
            testindex = data['fav-pts'].sample(int(len(data['fav-pts'])/10), random_state = rand).index
            trainindex = data['fav-pts'].index[~data['fav-pts'].index.isin(testindex)]            
            score_train_y = data['fav-pts'][trainindex].append(data['dog-pts'][trainindex])
            allowed_train_y = data['dog-pts'][trainindex].append(data['fav-pts'][trainindex])
            score_test_x = pd.DataFrame()
            allowed_test_x = pd.DataFrame()
            score_test_y = data['fav-pts'][testindex].append(data['dog-pts'][testindex])
            allowed_test_y = data['dog-pts'][testindex].append(data['fav-pts'][testindex])
            
            score_train_x = pd.DataFrame()
            allowed_train_x = pd.DataFrame()
            allowed_test_x = pd.DataFrame()
            score_test_x = pd.DataFrame()
            for i in range(1, scored_clusts+1):
                score_train_x['x'+str(i)] = data['fav-scored'+str(i)].loc[trainindex].append(data['dog-scored'+str(i)].loc[trainindex])
                score_test_x['x'+str(i)] = data['fav-scored'+str(i)].loc[testindex].append(data['dog-scored'+str(i)].loc[testindex])
            for i in range(1, allowed_clusts+1):
                allowed_train_x['x'+str(i)] = data['fav-allowed'+str(i)].loc[trainindex].append(data['dog-allowed'+str(i)].loc[trainindex])
                allowed_test_x['x'+str(i)] = data['fav-allowed'+str(i)].loc[testindex].append(data['dog-allowed'+str(i)].loc[testindex])
            scored_reg.fit(score_train_x, score_train_y.values)
            allowed_reg.fit(allowed_train_x, allowed_train_y)                 
            
            scored_pred = scored_reg.predict(score_test_x)
            allowed_pred = allowed_reg.predict(allowed_test_x)
            
            scored_mae = mean_absolute_error(score_test_y, scored_pred)
            allowed_mae = mean_absolute_error(allowed_test_y, allowed_pred)
            scored_r2 = r2_score(score_test_y, scored_pred)
            allowed_r2 = r2_score(allowed_test_y, allowed_pred)
            
            fav_allowed = pd.DataFrame()
            dog_allowed = pd.DataFrame()
            for i in range(1, allowed_clusts+1):
                fav_allowed['x'+str(i)] = data['fav-allowed'+str(i)].loc[testindex]
                dog_allowed['x'+str(i)] = data['dog-allowed'+str(i)].loc[testindex]
            fav_scored = pd.DataFrame()
            dog_scored = pd.DataFrame()
            for i in range(1, scored_clusts+1):
                fav_scored['x'+str(i)] = data['fav-scored'+str(i)].loc[testindex]
                dog_scored['x'+str(i)] = data['dog-scored'+str(i)].loc[testindex]            
            fav_points = data['fav-pts'][testindex]
            dog_points = data['dog-pts'][testindex]

            pred_score_fav = scored_reg.predict(fav_scored)
            pred_score_dog = scored_reg.predict(dog_scored)
            pred_allowed_fav = allowed_reg.predict(fav_allowed)
            pred_allowed_dog = allowed_reg.predict(dog_allowed)

            testmargin = fav_points - dog_points
            pred_margin_score = pred_score_fav - pred_score_dog
            pred_margin_allowed = pred_allowed_dog - pred_allowed_fav
            pred_margin_both = ((pred_allowed_dog + pred_score_fav)/2) - ((pred_allowed_fav + pred_score_dog)/2)

            testmargin = testmargin.apply(lambda x: 1 if x > 0 else -1)
            pred_margin_score = [1 if x > 0 else -1 for x in pred_margin_score]
            pred_margin_allowed = [1 if x > 0 else -1 for x in pred_margin_allowed]
            pred_margin_both = [1 if x > 0 else -1 for x in pred_margin_both]

            score_acc = accuracy_score(testmargin, pred_margin_score)        
            allow_acc = accuracy_score(testmargin, pred_margin_allowed)        
            both_acc = accuracy_score(testmargin, pred_margin_both)        

            score_roc = roc_auc_score(testmargin, pred_margin_score)    
            allow_roc = roc_auc_score(testmargin, pred_margin_allowed) 
            both_roc = roc_auc_score(testmargin, pred_margin_both)   
            
            score_mae_list.append(scored_mae)
            score_r2_list.append(scored_r2)
            allow_mae_list.append(allowed_mae)
            allow_r2_list.append(allowed_r2)
            score_acc_list.append(score_acc)
            allow_acc_list.append(allow_acc)
            both_acc_list.append(both_acc)
            score_roc_list.append(score_roc)
            allow_roc_list.append(allow_roc)
            both_roc_list.append(both_roc)
        all_mae_score.append(np.mean(score_mae_list))
        all_r2_score.append(np.mean(score_r2_list))
        all_mae_allow.append(np.mean(allow_mae_list))
        all_r2_allow.append(np.mean(allow_r2_list))
        all_acc_score.append(np.mean(score_acc_list))
        all_roc_score.append(np.mean(score_roc_list))
        all_acc_allow.append(np.mean(allow_acc_list))
        all_roc_allow.append(np.mean(allow_roc_list))
        all_acc_both.append(np.mean(both_acc_list))
        all_roc_both.append(np.mean(both_roc_list))


all_scored_feats = []
all_scored_clusts = []
all_scored_scale = []
all_allowed_feats = []
all_allowed_clusts = []
all_allowed_scale = []

for score in scorelist:
    for allowed in allowedlist:
        scored_feats, scored_clusts, scored_scale = score
        allowed_feats, allowed_clusts, allowed_scale = allowed
        all_scored_feats.append(scored_feats)
        all_scored_clusts.append(scored_clusts)
        all_scored_scale.append(scored_scale)
        all_allowed_feats.append(allowed_feats)
        all_allowed_clusts.append(allowed_clusts)
        all_allowed_scale.append(allowed_scale)
        
        
CVDF = pd.DataFrame()
CVDF['mae_score'] = all_mae_score
CVDF['mae_allowed'] = all_mae_allow
CVDF['r2_score'] = all_r2_score
CVDF['r2_allow'] = all_r2_allow
CVDF['acc_score'] = all_acc_score
CVDF['acc_allow'] = all_acc_allow
CVDF['acc_both'] = all_acc_both
CVDF['roc_score'] = all_roc_score
CVDF['roc_allow'] = all_roc_allow
CVDF['roc_both'] = all_roc_both
CVDF['score_feats'] = all_scored_feats
CVDF['score_clusts'] = all_scored_clusts
CVDF['score_scale'] = all_scored_scale
CVDF['allow_feats'] = all_allowed_feats
CVDF['allow_clusts'] = all_allowed_clusts
CVDF['allow_scale'] = all_allowed_scale
#score
#4,9,standard
#['floor-percentage', 'effective-field-goal-pct', 'shooting-pct']
#['assists-per-possession', 'defensive-rebounds-per-poss']
#['assists-per-game', 'personal-fouls-per-game', 'defensive-rebounds-per-game']
#['true-shooting-percentage']
#4,9,standard
#5,9,robust
#7,9,robust
#7, 18 robust
#2, 27 minmax
#3, 27 minmax
#
#allowed
#7, 9, robust
#6, 9, robust
#6, 12, robust
#7, 12 robust
#5, 12 minmax
#5, 9 robust <-


