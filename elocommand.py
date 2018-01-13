#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 16:20:30 2018

@author: eric.hensleyibm.com
"""

#from elo_pred import stat_pred
from stataverages import ha_rolling_avg_weighted, team_rolling_avg_weighted
from singlegamestats import pull_targets
from pymongo import MongoClient

client = MongoClient()
db = client['ncaa_bb']

targets_data = pull_targets()
statlist = ['rebounding', 'fouling','foulrate','post', 'guarding','stealing','blocking','shooting-efficiency','teamwork','chemistry','true-shooting-percentage']

for stat in statlist:
    target_stat_data = {}
    for stat in statlist:
        pred_stat_data = {}
    #    elo_for, elo_against = stat_pred(stat, 5.03159923, 3.58803079, 69.86241153, 0.13186422)
    #    pred_stat_data['elo_for'] = elo_for
    #    pred_stat_data['elo_against'] = elo_against
    #    elo_for = None
    #    elo_against = None
        for games in [5, 10, 15, 30, 50, 75, 100]:
            team_for, team_against = team_rolling_avg_weighted(stat, games)
            ha_for, ha_against = ha_rolling_avg_weighted(stat, games)
            pred_stat_data['team_for_'+str(games)] = team_for
            pred_stat_data['team_against_'+str(games)] = team_against
            pred_stat_data['ha_for_'+str(games)] = ha_for
            pred_stat_data['ha_against_'+str(games)] = ha_against
            team_for = None
            team_against = None
            ha_for = None
            ha_against = None
        target_stat_data[stat] = pred_stat_data
    
    
target_stat_data