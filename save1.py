#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 09:35:17 2018

@author: eric.hensleyibm.com
"""


import mysql.connector 
import pandas as pd
import numpy as np
import math 
from gp import bayesian_optimisation

passcode = 'ibm1234'
cnx = mysql.connector.connect(user='root', password=passcode,
                          host='127.0.0.1',
                          database='ncaa_bb') 
cursor = cnx.cursor()
query = "select teamname, (select avg(`offensive-efficiency`) from basestats as bs join gamedata as gd on bs.teamname = gd.teamname and bs.statdate = gd.`date` where gd.teamname = tn.teamname and bs.statdate < '2010-11-01'), (select avg(`offensive-efficiency`) from basestats as bs join gamedata as gd on bs.teamname = gd.teamname and bs.statdate = gd.`date` where gd.opponent = tn.teamname and bs.statdate < '2010-11-01') from teamnames as tn"
cursor.execute(query)
names = ['name', 'for', 'against']
pastdata = pd.DataFrame(cursor.fetchall(), columns = names)
cursor.close()
cnx.close()

#print(fordict)    
cnx = mysql.connector.connect(user='root', password=passcode,
                          host='127.0.0.1',
                          database='ncaa_bb') 
cursor = cnx.cursor()
query = "SELECT \
        oddsdate, favorite, underdog, bs1.`offensive-efficiency`, bs2.`offensive-efficiency`, homeaway\
        FROM\
        oddsdata as od\
        join basestats as bs1 on od.oddsdate = bs1.statdate and bs1.teamname = od.favorite\
        join basestats as bs2 on od.oddsdate = bs2.statdate and bs2.teamname = od.underdog\
        WHERE\
        oddsdate > '2010-11-01'\
        ORDER BY oddsdate ASC"
cursor.execute(query)
names = ['date', 'fav', 'dog', 'favstat', 'dogstat', 'ha']
data = pd.DataFrame(cursor.fetchall(), columns = names)
data=data.dropna(how='any')
cursor.close()
cnx.close()

#all_s1_error = []
#all_s2_error = []
#fordict = {}
#for i in range(0, len(pastdata['name'])):
#    if math.isnan(pastdata['for'][i]):
#        fordict[pastdata['name'][i]] = np.mean(pastdata['for']) - (np.std(pastdata['for']) * 1.5)
#    else:
#        fordict[pastdata['name'][i]] = pastdata['for'][i]
#againstdict = {}
#for i in range(0, len(pastdata['name'])):
#    if math.isnan(pastdata['against'][i]):
#        againstdict[pastdata['name'][i]] = np.mean(pastdata['for']) + (np.std(pastdata['for']) * 1.5)
#    else:
#        againstdict[pastdata['name'][i]] = pastdata['against'][i]
#season = np.array(data['date'])[0].year
#for date, t1, t2, s1, s2, loc in np.array(data):
#    if date.month == 11 and date.year > season:
#        fordictmean = np.mean(list(fordict.values()))
#        againstdictmean = np.mean(list(againstdict.values()))
#        for key in fordict.keys():
#            fordict[key] = fordict[key] + (fordictmean - fordict[key])*adj
#        for key in againstdict.keys():
#            againstdict[key] = againstdict[key] + (againstdictmean - againstdict[key])*adj
#        season += 1
#    if loc == 1:
#         loc = -1
#    elif loc == 0:
#         loc = 1
#    s1_exp = (fordict[t1]+againstdict[t2])/2 + (loc * hf)
#    s2_exp = (fordict[t2]+againstdict[t1])/2 - (loc * hf)
#    s1_error = (s1 - s1_exp)/s1_exp
#    s2_error = (s2 - s2_exp)/s2_exp
#    all_s1_error.append(math.fabs(s1_error))
#    all_s2_error.append(math.fabs(s2_error))
#    if math.isnan(fordict[t1] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink):
#        break
#    else:
#        fordict[t1] = fordict[t1] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink
#    if math.isnan(againstdict[t2] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink):
#        break
#    else:
#        againstdict[t2] = againstdict[t2] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink
#    fordict[t2] = fordict[t2] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink
#    againstdict[t1] = againstdict[t1] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink    
#
#errors = (np.array(all_s1_error)+np.array(all_s2_error))/2
#avg_error = np.mean(errors)
#print(avg_error) 
#
#errors = (np.array(all_s1_error)+np.array(all_s2_error))/2
#avg_error = np.mean(errors)
#avg_std = np.std(all_s1_error)
#gpd_error = [np.mean(errors[i:i + 100]) for i in range(0, len(errors), 100)]
#gpd_std = [np.std(errors[i:i + 100]) for i in range(0, len(errors), 100)]
#from matplotlib import pyplot as plt
#fig, ax1 = plt.subplots()
#ax1.plot(gpd_error, 'b')
##ax1.set_ylim(-.06, .10)
#ax2 = ax1.twinx()
#ax2.plot(gpd_std, 'r')
#fig.tight_layout()
#plt.show()

parameters = [ 0.00312273,  .75881657,  0.09400018,  0.16018282]
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

from matplotlib import pyplot as plt
plt.plot(results[1])

results[0][list(results[1]).index(min(list(results[1])))]   # [  5.03159923,   3.58803079,  69.86241153,   0.13186422]
