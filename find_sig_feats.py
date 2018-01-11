#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 16:34:06 2017

@author: eric.hensleyibm.com
"""

import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor
from matplotlib import pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import linkage, cophenet
from scipy.spatial.distance import pdist
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate
from sklearn.model_selection import KFold

names = ['teamname','scoredate','shooting-efficiency','teamwork','chemistry','true-shooting-percentage','points-per-game','offensive-efficiency',
'floor-percentage','points-from-2-pointers','points-from-3-pointers','percent-of-points-from-2-pointers','percent-of-points-from-3-pointers',
'percent-of-points-from-free-throws','defensive-efficiency','shooting-pct','fta-per-fga','ftm-per-100-possessions','free-throw-rate',
'three-point-rate','two-point-rate','three-pointers-made-per-game','effective-field-goal-pct','true-shooting-percentage','offensive-rebounds-per-game',
'offensive-rebounding-pct','defensive-rebounds-per-game','defensive-rebounding-pct','blocks-per-game','steals-per-game','block-pct','steals-perpossession',
'steal-pct','assists-per-game','turnovers-per-game','turnovers-per-possession','assist--per--turnover-ratio','assists-per-fgm','assists-per-possession',
'turnover-pct','personal-fouls-per-game','personal-fouls-per-possession','personal-foul-pct','possessions-per-game','extra-chances-per-game','effective-possession-ratio']

avg = pd.read_csv('average_stats.csv')
targets = avg[['teamname','date', 'shooting-efficiency','teamwork','chemistry','true-shooting-percentage']]
del avg['Unnamed: 0']
del avg['shooting-efficiency']
del avg['teamwork']
del avg['chemistry']
del avg['true-shooting-percentage']
avg.columns = ['avg' + i for i in avg.columns]
twoweek = pd.read_csv('2_wk_average_stats.csv')
del twoweek['Unnamed: 0']
del twoweek['shooting-efficiency']
del twoweek['teamwork']
del twoweek['chemistry']
del twoweek['true-shooting-percentage']
twoweek.columns = ['2wk' + i for i in twoweek.columns]
onemonth = pd.read_csv('1_month_average_stats.csv')
del onemonth['Unnamed: 0']
del onemonth['shooting-efficiency']
del onemonth['teamwork']
del onemonth['chemistry']
del onemonth['true-shooting-percentage']
onemonth.columns = ['1mth' + i for i in onemonth.columns]
threemonth = pd.read_csv('3_month_average_stats.csv')
del threemonth['Unnamed: 0']
del threemonth['shooting-efficiency']
del threemonth['teamwork']
del threemonth['chemistry']
del threemonth['true-shooting-percentage']
threemonth.columns = ['3mth' + i for i in threemonth.columns]
homeaway = pd.read_csv('home_away.csv')

ha = []
for i in range(0, len(homeaway)):
    if homeaway['teamname'][i] == homeaway['favorite'][i]:
        if homeaway['homeaway'][i] == 1:
            ha.append(1)
        else:
            ha.append(0)
    elif homeaway['teamname'][i] == homeaway['underdog'][i]:
        if homeaway['homeaway'][i] == 1:
            ha.append(0)
        else:
            ha.append(1)            
homeaway['ha'] = ha
del homeaway['favorite']
del homeaway['underdog']
del homeaway['homeaway']
del homeaway['Unnamed: 0']

data = pd.merge(avg, twoweek, left_on = ['avgteamname','avgdate'], right_on = ['2wkteamname', '2wkdate'])
data = pd.merge(data, onemonth, left_on = ['avgteamname', 'avgdate'], right_on = ['1mthteamname', '1mthdate'])
data = pd.merge(data, threemonth, left_on = ['avgteamname', 'avgdate'], right_on = ['3mthteamname', '3mthdate'])
data = pd.merge(data, homeaway, left_on = ['avgteamname', 'avgdate'], right_on = ['teamname', 'date'])
data = pd.merge(data, targets, left_on = ['avgteamname', 'avgdate'], right_on = ['teamname', 'date'])
del data['avgteamname']
del data['avgdate']
del data['2wkteamname']
del data['2wkdate']
del data['1mthteamname']
del data['1mthdate']
del data['3mthteamname']
del data['3mthdate']
del data['teamname_x']
del data['date_x']
del data['teamname_y']
del data['date_y']
data = data.dropna(how='any')

y1 = data['shooting-efficiency']
y2 = data['teamwork']
y3 = data['chemistry']
y4 = data['true-shooting-percentage']

del data['shooting-efficiency']
del data['teamwork']
del data['chemistry']
del data['true-shooting-percentage']

# shooting efficiency
#labels = ['ha',
# '3mthoffensive-efficiency',
# '3mthtrue-shooting-percentage.1',
# '1mthfloor-percentage',
# '3mthfloor-percentage',
# '1mthoffensive-efficiency',
# '3mthshooting-pct',
# 'avgtrue-shooting-percentage.1', #<-----------
# '3mtheffective-field-goal-pct',
# '1mthtrue-shooting-percentage.1',
# 'avgshooting-pct',
# '1mthshooting-pct',
# 'avgeffective-field-goal-pct',
# '2wkdefensive-rebounding-pct',
# '1mtheffective-field-goal-pct',
# '2wkfloor-percentage',
# '2wkdefensive-efficiency',
# '2wkoffensive-efficiency',
# '1mthpoints-per-game',
# '2wkdefensive-rebounds-per-game',
# '3mthpoints-per-game',
# '2wktrue-shooting-percentage.1',
# '2wkshooting-pct',
# '2wkextra-chances-per-game',
# '2wkpoints-per-game',
# '1mthdefensive-rebounding-pct',
# '2wkblock-pct',
# 'avgoffensive-efficiency',
# '2wkeffective-field-goal-pct',
# '2wkassists-per-fgm',
# '2wkoffensive-rebounding-pct',
# '2wkblocks-per-game',
# '2wkassist--per--turnover-ratio',
# '1mthdefensive-efficiency',
# '2wkpoints-from-2-pointers',
# '2wkpossessions-per-game',
# '2wkoffensive-rebounds-per-game',
# '2wkeffective-possession-ratio',
# '2wkassists-per-game',
# '2wkassists-per-possession',
# '1mthdefensive-rebounds-per-game',
# '2wkpersonal-fouls-per-possession',
# '2wkpersonal-fouls-per-game',
# '2wkpersonal-foul-pct',
# '2wkftm-per-100-possessions',
# '2wkpercent-of-points-from-2-pointers',
# '2wksteals-per-game',
# '2wkfta-per-fga',
# '2wksteal-pct',
# '1mthextra-chances-per-game',
# '2wkfree-throw-rate',
# '2wkpercent-of-points-from-free-throws',
# '2wksteals-perpossession',
# '3mthdefensive-rebounding-pct',
# '1mthassists-per-game',
# '1mthassist--per--turnover-ratio',
# '1mthassists-per-possession',
# '2wkturnovers-per-possession',
# '2wkturnover-pct',
# '2wkturnovers-per-game',
# '1mthassists-per-fgm',
# '3mthdefensive-efficiency',
# '1mthoffensive-rebounding-pct',
# 'avgfloor-percentage',
# '3mthdefensive-rebounds-per-game',
# '1mthblock-pct',
# '2wkthree-point-rate',
# '2wktwo-point-rate',
# '2wkpercent-of-points-from-3-pointers',
# '1mthpossessions-per-game',
# '1mtheffective-possession-ratio',
# '1mthpoints-from-2-pointers',
# '1mthoffensive-rebounds-per-game',
# 'avgdefensive-rebounding-pct',
# '1mthblocks-per-game',
# '1mthpersonal-fouls-per-game',
# '3mthassist--per--turnover-ratio',
# '1mthpersonal-fouls-per-possession',
# '1mthpersonal-foul-pct',
# '1mthftm-per-100-possessions',
# '3mthextra-chances-per-game',
# 'avgdefensive-efficiency',
# '2wkpoints-from-3-pointers',
# '1mthfree-throw-rate',
# '2wkthree-pointers-made-per-game',
# '1mthfta-per-fga',
# 'avgdefensive-rebounds-per-game',
# '1mthpercent-of-points-from-free-throws',
# '1mthturnovers-per-possession',
# '1mthturnovers-per-game',
# '1mthturnover-pct',
# '3mthassists-per-possession',
# '3mthassists-per-game',
# '1mthpercent-of-points-from-2-pointers',
# '1mthsteals-per-game',
# 'avgassists-per-game',
# '1mthsteal-pct',
# '1mthsteals-perpossession',
# '3mthblock-pct',
# '3mthoffensive-rebounding-pct',
# 'avgpoints-per-game',
# '3mthpossessions-per-game',
# '3mthassists-per-fgm',
# 'avgassists-per-possession',
# 'avgassists-per-fgm',
# 'avgpersonal-fouls-per-game',
# '3mthpersonal-fouls-per-game',
# '3mthpoints-from-2-pointers',
# 'avgextra-chances-per-game',
# '3mthblocks-per-game',
# '3mthpersonal-fouls-per-possession',
# '3mtheffective-possession-ratio',
# '3mthpersonal-foul-pct',
# 'avgblock-pct',
# 'avgpersonal-foul-pct',
# 'avgpossessions-per-game',
# '3mthoffensive-rebounds-per-game',
# '3mthftm-per-100-possessions',
# '3mthfree-throw-rate',
# '3mthfta-per-fga',
# 'avgftm-per-100-possessions',
# 'avgassist--per--turnover-ratio',
# 'avgpersonal-fouls-per-possession',
# '3mthpercent-of-points-from-free-throws',
# '3mthturnovers-per-game',
# '1mthtwo-point-rate',
# 'avgblocks-per-game',
# '1mththree-point-rate',
# 'avgoffensive-rebounding-pct',
# '1mthpercent-of-points-from-3-pointers',
# 'avgfree-throw-rate',
# 'avgfta-per-fga',
# '3mthturnover-pct',
# '3mthturnovers-per-possession',
# '3mthsteals-per-game',
# 'avgpercent-of-points-from-free-throws',
# 'avgeffective-possession-ratio',
# '3mthsteal-pct',
# '3mthsteals-perpossession',
# 'avgoffensive-rebounds-per-game',
# '3mthpercent-of-points-from-2-pointers',
# '1mththree-pointers-made-per-game',
# '1mthpoints-from-3-pointers',
# 'avgsteals-perpossession',
# 'avgturnovers-per-game',
# 'avgsteal-pct',
# 'avgpoints-from-2-pointers',
# 'avgturnovers-per-possession',
# 'avgpercent-of-points-from-2-pointers',
# 'avgsteals-per-game',
# 'avgturnover-pct',
# '3mththree-point-rate',
# '3mthtwo-point-rate',
# '3mthpercent-of-points-from-3-pointers',
# 'avgthree-pointers-made-per-game',
# 'avgtwo-point-rate',
# 'avgthree-point-rate',
# 'avgpoints-from-3-pointers',
# '3mththree-pointers-made-per-game',
# '3mthpoints-from-3-pointers',
# 'avgpercent-of-points-from-3-pointers']
#
#


# teamwork
#labels = ['ha',
# 'avgassists-per-possession',
# '3mthassists-per-possession',
# '2wkdefensive-rebounds-per-game',
# '2wkfta-per-fga',
# '3mthdefensive-rebounds-per-game',
# '1mthassists-per-possession',
# 'avgassists-per-game',
# '2wkeffective-possession-ratio',
# 'avgdefensive-rebounding-pct',
# '1mthdefensive-rebounds-per-game',
# 'avgpoints-per-game',
# 'avgassists-per-fgm',
# '3mthdefensive-rebounding-pct',
# '2wkassists-per-possession',
# 'avgdefensive-rebounds-per-game',
# '2wkfree-throw-rate',
# '2wksteals-perpossession',
# 'avgoffensive-efficiency',
# '1mthdefensive-rebounding-pct',
# '1mthassists-per-game',
# '2wkturnovers-per-game',
# '2wkassists-per-fgm',
# '2wkdefensive-rebounding-pct',
# '2wkpercent-of-points-from-free-throws',
# '3mthassists-per-game',
# '2wkoffensive-efficiency', # <---------
# '2wkdefensive-efficiency',
# '3mthassists-per-fgm',
# '3mtheffective-possession-ratio',
# '2wkoffensive-rebounds-per-game',
# '1mtheffective-possession-ratio',
# '2wksteals-per-game',
# '2wkassists-per-game',
# '3mthassist--per--turnover-ratio',
# '2wkftm-per-100-possessions',
# '2wkblock-pct',
# 'avgassist--per--turnover-ratio',
# '2wksteal-pct',
# '2wkassist--per--turnover-ratio',
# '2wkextra-chances-per-game',
# '2wkoffensive-rebounding-pct',
# '1mthassist--per--turnover-ratio',
# '2wkpoints-from-3-pointers',
# '1mthassists-per-fgm',
# 'avgftm-per-100-possessions',
# '2wkpersonal-fouls-per-game',
# '2wkblocks-per-game',
# '2wkthree-pointers-made-per-game',
# '2wkturnovers-per-possession',
# '1mthdefensive-efficiency',
# '2wkpersonal-foul-pct',
# '2wkpossessions-per-game',
# '2wkturnover-pct',
# '2wkpersonal-fouls-per-possession',
# 'avgdefensive-efficiency',
# '3mthturnovers-per-possession',
# '3mthdefensive-efficiency',
# '2wktwo-point-rate',
# '1mthsteals-per-game',
# 'avgpoints-from-3-pointers',
# 'avgfta-per-fga',
# 'avgpossessions-per-game',
# '2wkpercent-of-points-from-3-pointers',
# '3mthoffensive-efficiency',
# '3mthextra-chances-per-game',
# '1mthextra-chances-per-game',
# '1mthoffensive-rebounding-pct',
# 'avgtrue-shooting-percentage.1',
# '1mthblocks-per-game',
# '1mthpossessions-per-game',
# '2wkpoints-from-2-pointers',
# 'avgeffective-field-goal-pct',
# 'avgpercent-of-points-from-free-throws',
# '2wkpercent-of-points-from-2-pointers',
# '1mthblock-pct',
# '3mthsteals-per-game',
# '1mthsteal-pct',
# '1mthpersonal-fouls-per-game',
# '3mthpersonal-fouls-per-game',
# '1mthturnover-pct',
# '2wkpoints-per-game',
# '3mthpossessions-per-game',
# 'avgpercent-of-points-from-2-pointers',
# 'avgshooting-pct',
# '3mthsteal-pct',
# 'avgfloor-percentage',
# '3mthturnover-pct',
# '3mthblocks-per-game',
# '1mthoffensive-rebounds-per-game',
# '1mthfree-throw-rate',
# '3mtheffective-field-goal-pct',
# '2wktrue-shooting-percentage.1',
# '1mthpercent-of-points-from-free-throws',
# '2wkshooting-pct',
# '2wkthree-point-rate',
# '1mthfta-per-fga',
# '2wkfloor-percentage',
# '1mthshooting-pct',
# '3mthoffensive-rebounding-pct',
# '1mthpersonal-fouls-per-possession',
# '3mthshooting-pct',
# '3mthfloor-percentage',
# '2wkeffective-field-goal-pct',
# '3mthsteals-perpossession',
# 'avgfree-throw-rate',
# '3mthpercent-of-points-from-free-throws',
# '1mthturnovers-per-game',
# '1mthfloor-percentage',
# '1mthsteals-perpossession',
# '1mthturnovers-per-possession',
# '3mthturnovers-per-game',
# '1mthpersonal-foul-pct',
# '3mthblock-pct',
# '1mthpercent-of-points-from-2-pointers',
# 'avgoffensive-rebounding-pct',
# '1mthpoints-per-game',
# 'avgpersonal-fouls-per-game',
# 'avgthree-pointers-made-per-game',
# '1mthtrue-shooting-percentage.1',
# '1mtheffective-field-goal-pct',
# '3mthpersonal-foul-pct',
# '1mthoffensive-efficiency',
# 'avgsteals-per-game',
# '3mthtrue-shooting-percentage.1',
# '1mthftm-per-100-possessions',
# 'avgthree-point-rate',
# 'avgpersonal-foul-pct',
# '3mthpersonal-fouls-per-possession',
# '3mthfree-throw-rate',
# '3mthftm-per-100-possessions',
# '3mthfta-per-fga',
# '1mthpoints-from-2-pointers',
# '1mthtwo-point-rate',
# '3mthpoints-from-2-pointers',
# '3mthoffensive-rebounds-per-game',
# '1mthpercent-of-points-from-3-pointers',
# 'avgturnovers-per-game',
# '1mthpoints-from-3-pointers',
# '3mthpoints-from-3-pointers',
# '1mththree-pointers-made-per-game',
# '3mthpercent-of-points-from-2-pointers',
# '1mththree-point-rate',
# 'avgtwo-point-rate',
# 'avgsteal-pct',
# 'avgblocks-per-game',
# 'avgextra-chances-per-game',
# '3mthpercent-of-points-from-3-pointers',
# '3mthpoints-per-game',
# 'avgpersonal-fouls-per-possession',
# 'avgturnovers-per-possession',
# 'avgblock-pct',
# 'avgsteals-perpossession',
# 'avgoffensive-rebounds-per-game',
# 'avgpercent-of-points-from-3-pointers',
# 'avgeffective-possession-ratio',
# 'avgpoints-from-2-pointers',
# '3mththree-point-rate',
# '3mthtwo-point-rate',
# 'avgturnover-pct',
# '3mththree-pointers-made-per-game']


## chemistry
#labels = ['ha',
# '3mthdefensive-rebounds-per-game',
# '1mthdefensive-rebounds-per-game',
# '2wkdefensive-rebounds-per-game',
# 'avgassists-per-game',
# '3mthassists-per-game',
# '1mthassists-per-game',
# '2wkassists-per-game',
# 'avgpoints-per-game',
# 'avgdefensive-rebounds-per-game',
# '2wkfta-per-fga',
# '2wkassists-per-possession',
# 'avgassists-per-possession',
# '3mthassists-per-possession', # <-----
# '3mthpoints-per-game',
# '2wkeffective-possession-ratio',
# '3mthpersonal-fouls-per-possession',
# '1mthpoints-per-game',
# '2wkfree-throw-rate',
# '1mthassists-per-possession',
# '2wkpersonal-foul-pct',
# '2wksteal-pct',
# '2wkdefensive-rebounding-pct',
# '2wkthree-pointers-made-per-game',
# '2wkassist--per--turnover-ratio',
# '2wkpoints-per-game',
# '2wkturnover-pct',
# '1mtheffective-possession-ratio',
# '1mthdefensive-rebounding-pct',
# '3mtheffective-possession-ratio',
# '2wkpersonal-fouls-per-possession',
# '2wkpercent-of-points-from-free-throws',
# '2wkoffensive-rebounds-per-game',
# '2wkassists-per-fgm',
# '3mthdefensive-rebounding-pct',
# '2wkpersonal-fouls-per-game',
# '2wktwo-point-rate',
# '3mthpersonal-foul-pct',
# '1mthpersonal-fouls-per-possession',
# '2wkdefensive-efficiency',
# 'avgassists-per-fgm',
# '2wkblock-pct',
# '2wkturnovers-per-possession',
# '2wkpercent-of-points-from-3-pointers',
# '1mthdefensive-efficiency',
# '2wkpoints-from-3-pointers',
# 'avgftm-per-100-possessions',
# 'avgoffensive-efficiency',
# '2wkturnovers-per-game',
# '3mthassist--per--turnover-ratio',
# '2wkfloor-percentage',
# '2wkpossessions-per-game',
# '1mthpersonal-foul-pct',
# '2wkoffensive-rebounding-pct',
# '3mthoffensive-efficiency',
# '2wksteals-per-game',
# '2wkoffensive-efficiency',
# '2wkblocks-per-game',
# '2wksteals-perpossession',
# '1mthblocks-per-game',
# '3mthshooting-pct',
# '1mthassists-per-fgm',
# 'avgthree-pointers-made-per-game',
# 'avgpoints-from-3-pointers',
# 'avgpercent-of-points-from-2-pointers',
# '2wkthree-point-rate',
# '2wkftm-per-100-possessions',
# '3mthfloor-percentage', # <--------------
# '3mthdefensive-efficiency',
# 'avgfta-per-fga',
# 'avgtrue-shooting-percentage.1',
# '3mthblocks-per-game',
# '2wkextra-chances-per-game',
# '3mthturnovers-per-possession',
# '2wkpoints-from-2-pointers',
# 'avgoffensive-rebounding-pct',
# '3mthassists-per-fgm',
# 'avgdefensive-efficiency',
# '2wktrue-shooting-percentage.1',
# 'avgfloor-percentage',
# '1mthassist--per--turnover-ratio',
# '2wkshooting-pct',
# '1mthextra-chances-per-game',
# '3mthpossessions-per-game',
# '3mtheffective-field-goal-pct',
# '3mthsteal-pct',
# 'avgassist--per--turnover-ratio',
# '1mthpossessions-per-game',
# 'avgpersonal-fouls-per-possession',
# '1mthfloor-percentage',
# '3mthturnover-pct',
# '2wkpercent-of-points-from-2-pointers',
# 'avgeffective-field-goal-pct',
# '3mthsteals-perpossession',
# 'avgdefensive-rebounding-pct',
# '1mthpercent-of-points-from-free-throws',
# '1mthturnover-pct',
# '3mthextra-chances-per-game',
# '3mthturnovers-per-game',
# '1mthturnovers-per-possession',
# '1mthpersonal-fouls-per-game',
# '3mthsteals-per-game',
# '3mthpersonal-fouls-per-game',
# 'avgshooting-pct',
# '2wkeffective-field-goal-pct',
# '1mthpoints-from-2-pointers',
# 'avgpersonal-fouls-per-game',
# '1mthshooting-pct',
# '3mthoffensive-rebounding-pct',
# '1mthoffensive-rebounding-pct',
# '1mthsteals-per-game',
# '1mthoffensive-efficiency',
# '3mthpoints-from-2-pointers',
# '1mthoffensive-rebounds-per-game',
# '3mthpercent-of-points-from-free-throws',
# '1mthblock-pct',
# '1mthsteal-pct',
# '1mthfta-per-fga',
# 'avgfree-throw-rate',
# '3mthblock-pct',
# '3mthftm-per-100-possessions',
# '1mthftm-per-100-possessions',
# '3mthtrue-shooting-percentage.1',
# 'avgpersonal-foul-pct',
# '1mthfree-throw-rate',
# '1mthpercent-of-points-from-2-pointers',
# '3mthpercent-of-points-from-2-pointers',
# 'avgpercent-of-points-from-free-throws',
# '1mthpoints-from-3-pointers',
# 'avgturnovers-per-possession',
# '3mthfta-per-fga',
# '1mthsteals-perpossession',
# 'avgpossessions-per-game',
# '1mthturnovers-per-game',
# '1mtheffective-field-goal-pct',
# '3mthoffensive-rebounds-per-game',
# '3mthfree-throw-rate',
# 'avgpercent-of-points-from-3-pointers',
# 'avgblock-pct',
# '1mthpercent-of-points-from-3-pointers',
# 'avgoffensive-rebounds-per-game',
# '1mthtrue-shooting-percentage.1',
# '3mththree-point-rate',
# 'avgturnover-pct',
# 'avgpoints-from-2-pointers',
# '1mthtwo-point-rate',
# 'avgsteals-perpossession',
# 'avgextra-chances-per-game',
# 'avgturnovers-per-game',
# '1mththree-pointers-made-per-game',
# '1mththree-point-rate',
# 'avgthree-point-rate',
# 'avgblocks-per-game',
# 'avgsteal-pct',
# '3mththree-pointers-made-per-game',
# '3mthtwo-point-rate',
# 'avgsteals-per-game',
# 'avgeffective-possession-ratio',
# '3mthpercent-of-points-from-3-pointers',
# '3mthpoints-from-3-pointers',
# 'avgtwo-point-rate']



labels = ['ha',
 '3mthtrue-shooting-percentage.1',
 'avgtrue-shooting-percentage.1',
 '1mthtrue-shooting-percentage.1',
 '3mtheffective-field-goal-pct',
 'avgeffective-field-goal-pct',
 '3mthoffensive-efficiency', #<-------
 '1mtheffective-field-goal-pct',
 '1mthoffensive-efficiency',
 '2wkdefensive-rebounding-pct',
 '2wktrue-shooting-percentage.1',
 '2wkdefensive-efficiency',
 '2wkdefensive-rebounds-per-game',
 '1mthshooting-pct',
 '2wkeffective-field-goal-pct',
 '2wkoffensive-efficiency',
 '3mthshooting-pct',
 '2wkblock-pct',
 '2wkshooting-pct',
 '2wkextra-chances-per-game',
 '2wkoffensive-rebounding-pct',
 '2wkpoints-per-game',
 '1mthdefensive-rebounding-pct',
 'avgshooting-pct',
 '2wkassists-per-fgm',
 '2wkoffensive-rebounds-per-game',
 '2wkpossessions-per-game',
 '2wkblocks-per-game',
 '1mthpoints-per-game',
 '1mthdefensive-efficiency',
 '2wkfloor-percentage',
 '2wkpercent-of-points-from-2-pointers',
 '2wkassist--per--turnover-ratio',
 '2wkeffective-possession-ratio',
 '2wkpoints-from-2-pointers',
 '2wkpersonal-foul-pct',
 '2wkassists-per-game',
 '2wkpersonal-fouls-per-possession',
 '2wkpersonal-fouls-per-game',
 '1mthdefensive-rebounds-per-game',
 '2wkassists-per-possession',
 '2wktwo-point-rate',
 '2wkthree-point-rate',
 '3mthpoints-per-game',
 '2wkftm-per-100-possessions',
 '2wkfree-throw-rate',
 '2wkfta-per-fga',
 '2wkpercent-of-points-from-free-throws',
 '1mthfloor-percentage',
 '2wksteals-per-game',
 '2wksteal-pct',
 '2wksteals-perpossession',
 '1mthextra-chances-per-game',
 '2wkpercent-of-points-from-3-pointers',
 '3mthdefensive-rebounding-pct',
 '2wkturnovers-per-game',
 '2wkturnovers-per-possession',
 '1mthoffensive-rebounding-pct',
 '1mthassists-per-fgm',
 '2wkturnover-pct',
 '1mthassist--per--turnover-ratio',
 '1mthblock-pct',
 '3mthdefensive-efficiency',
 '2wkpoints-from-3-pointers',
 'avgdefensive-rebounding-pct',
 '2wkthree-pointers-made-per-game',
 '1mthpossessions-per-game',
 '1mthoffensive-rebounds-per-game',
 '1mthassists-per-possession',
 '3mthfloor-percentage',
 '1mthassists-per-game',
 '3mthdefensive-rebounds-per-game',
 '1mthblocks-per-game',
 'avgoffensive-efficiency',
 '1mthpersonal-fouls-per-possession',
 '1mthpersonal-foul-pct',
 '1mtheffective-possession-ratio',
 '1mthpersonal-fouls-per-game',
 '1mthpercent-of-points-from-2-pointers',
 '1mthftm-per-100-possessions',
 '1mthtwo-point-rate',
 '1mththree-point-rate',
 'avgdefensive-efficiency',
 '3mthoffensive-rebounding-pct',
 '1mthfta-per-fga',
 '1mthfree-throw-rate',
 '1mthpoints-from-2-pointers',
 '1mthpercent-of-points-from-free-throws',
 '3mthassist--per--turnover-ratio',
 '3mththree-point-rate',
 '3mthtwo-point-rate',
 '3mthassists-per-fgm',
 'avgdefensive-rebounds-per-game',
 '1mthturnovers-per-possession',
 '1mthturnovers-per-game',
 '3mthextra-chances-per-game',
 '1mthsteals-per-game',
 '1mthpercent-of-points-from-3-pointers',
 'avgassists-per-fgm',
 '1mthsteal-pct',
 '3mthblock-pct',
 '3mthpossessions-per-game',
 '1mthturnover-pct',
 '3mthoffensive-rebounds-per-game',
 '1mthsteals-perpossession',
 '3mthassists-per-game',
 'avgoffensive-rebounding-pct',
 '3mthblocks-per-game',
 '3mthassists-per-possession',
 '1mthpoints-from-3-pointers',
 '1mththree-pointers-made-per-game',
 'avgpersonal-foul-pct',
 'avgoffensive-rebounds-per-game',
 '3mthpersonal-fouls-per-game',
 'avgblock-pct',
 'avgftm-per-100-possessions',
 'avgextra-chances-per-game',
 'avgpossessions-per-game',
 'avgpersonal-fouls-per-game',
 '3mthpersonal-fouls-per-possession',
 'avgassists-per-game',
 'avgpersonal-fouls-per-possession',
 'avgblocks-per-game',
 '3mthftm-per-100-possessions',
 '3mthpersonal-foul-pct',
 '3mthfta-per-fga',
 'avgassists-per-possession',
 '3mthpoints-from-3-pointers',
 '3mthfree-throw-rate',
 'avgassist--per--turnover-ratio',
 '3mthpercent-of-points-from-2-pointers',
 '3mthpercent-of-points-from-free-throws',
 'avgpercent-of-points-from-free-throws',
 'avgpoints-per-game',
 '3mtheffective-possession-ratio',
 'avgfree-throw-rate',
 'avgfta-per-fga',
 '3mthturnovers-per-game',
 '3mththree-pointers-made-per-game',
 '3mthpoints-from-2-pointers',
 '3mthturnovers-per-possession',
 'avgpercent-of-points-from-2-pointers',
 '3mthsteals-per-game',
 'avgfloor-percentage',
 '3mthturnover-pct',
 '3mthsteals-perpossession',
 'avgturnovers-per-game',
 'avgeffective-possession-ratio',
 '3mthsteal-pct',
 'avgsteal-pct',
 '3mthpercent-of-points-from-3-pointers',
 'avgsteals-perpossession',
 'avgsteals-per-game',
 'avgthree-pointers-made-per-game',
 'avgpoints-from-3-pointers',
 'avgturnovers-per-possession',
 'avgpoints-from-2-pointers',
 'avgturnover-pct',
 'avgtwo-point-rate',
 'avgthree-point-rate',
 'avgpercent-of-points-from-3-pointers']
maelist = []
r2list = []
for i in range(1, len(labels)+1):
    cvscores = cross_validate(LinearRegression(), data[labels[:i]], y1, scoring = ['neg_mean_absolute_error', 'r2'], cv = KFold(n_splits=10, random_state=1108, shuffle=False))
    maelist.append(np.mean(cvscores['test_neg_mean_absolute_error']) * -1)
    r2list.append(np.mean(cvscores['test_r2']))

plt.plot(maelist)
#plt.plot([maelist[i] - maelist[i-1] for i in range(1, len(maelist))])
##
#[maelist[i] - maelist[i-1] for i in range(1, len(maelist))].index(min([maelist[i] - maelist[i-1] for i in range(1, len(maelist))][3:]))
#
#[maelist[i] - maelist[i-1] for i in range(1, len(maelist))].index(-0.0020017072308682327)
#plt.plot(r2list)
#maelist.index(min(maelist))
#r2list.index(max(r2list))
#
#labels[:[maelist[i] - maelist[i-1] for i in range(1, len(maelist))].index(-0.0020017072308682327)]

#
#labels[:69]
#
#['ha',
# '3mthoffensive-efficiency',
# '3mthtrue-shooting-percentage.1',
# '1mthfloor-percentage',
# '3mthfloor-percentage',
# '1mthoffensive-efficiency',
# '3mthshooting-pct',
# 'avgtrue-shooting-percentage.1']




forest = ExtraTreesRegressor(n_estimators=500,
                              random_state=86)
forest.fit(data, y4)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indicesnum = np.argsort(importances)[::-1]
indices = [list(data)[i] for i in indicesnum]
clist = []
clist.append(0)
for i in range(2, len(indices)+1):
    Z = linkage(data[indices[:i]].T, 'ward')
    c, coph_dists = cophenet(Z, pdist(data[indices[:i]].T))
    clist.append(c)
# Plot the feature importances of the forest
fig, ax1 = plt.subplots()
ax1.bar(range(data[indices].shape[1]), importances[indicesnum],
       color="r", yerr=std[indicesnum], align="center")
ax2 = ax1.twinx()
ax2.plot(clist)
fig.tight_layout()
plt.show()