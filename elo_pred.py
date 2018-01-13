#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 16:11:48 2018

@author: eric.hensleyibm.com
"""
import math 
import pandas as pd
import mysql.connector 
import numpy as np


def stat_pred(stat, hf, pwr, shrink, adj):
#    stat, hf, pwr, shrink, adj='true-shooting-percentage', 5.03159923, 3.58803079, 69.86241153, 0.13186422
    passcode = 'ibm1234'
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()
    query = "select teamname, (select avg(`%s`) from basestats as bs join gamedata as gd on bs.teamname = gd.teamname and bs.statdate = gd.`date` where gd.teamname = tn.teamname and bs.statdate < '2010-11-01'), (select avg(`%s`) from basestats as bs join gamedata as gd on bs.teamname = gd.teamname and bs.statdate = gd.`date` where gd.opponent = tn.teamname and bs.statdate < '2010-11-01') from teamnames as tn" % (stat, stat)
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
            oddsdate, favorite, underdog, bs1.`%s`, bs2.`%s`, homeaway\
            FROM\
            oddsdata as od\
            join basestats as bs1 on od.oddsdate = bs1.statdate and bs1.teamname = od.favorite\
            join basestats as bs2 on od.oddsdate = bs2.statdate and bs2.teamname = od.underdog\
            WHERE\
            oddsdate > '2010-11-01'\
            ORDER BY oddsdate ASC" % (stat, stat)
    cursor.execute(query)
    names = ['date', 'fav', 'dog', 'favstat', 'dogstat', 'ha']
    data = pd.DataFrame(cursor.fetchall(), columns = names)
    data=data.dropna(how='any')
    cursor.close()
    cnx.close()
#    record_list = []
    stat_for = {}
    stat_against = {}
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
    for date, t1, t2, s1, s2, loc in np.array(data):
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
        stat_for[str(date)+t1+t2] = {'date':date, 'team1':t1, 'team2':t2, 'forstat1':fordict[t1], 'forstat2':fordict[t2]}
        stat_against[str(date)+t1+t2] = {'date':date, 'team1':t1, 'team2':t2, 'againststat1':againstdict[t1], 'againststat2':againstdict[t2]}

        s1_exp = (fordict[t1]+againstdict[t2])/2 + (loc * hf)
        s2_exp = (fordict[t2]+againstdict[t1])/2 - (loc * hf)
        s1_error = (s1 - s1_exp)/s1_exp
        s2_error = (s2 - s2_exp)/s2_exp
        fordict[t1] = fordict[t1] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink
        againstdict[t2] = againstdict[t2] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink
        fordict[t2] = fordict[t2] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink
        againstdict[t1] = againstdict[t1] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink 
#        record = (date, t1, t2, fordict[t1], againstdict[t2])
#        record_list.append(record)
    return stat_for, stat_against
    
    
    
def target_pred(stat, hf, pwr, shrink, adj):
#    stat, hf, pwr, shrink, adj='true-shooting-percentage', 5.03159923, 3.58803079, 69.86241153, 0.13186422
    import singlegamestats 
    pastdata = singlegamestats.pull_targets_train(stat)

    if stat in ['rebounding', 'fouling','foulrate','post', 'guarding','stealing','blocking']:
        fa = 'allow'
    elif stat in ['shooting-efficiency','teamwork','chemistry','true-shooting-percentage']:
        fa = 'score'
    data = singlegamestats.pull_targets_test(stat, fa)
    data=data.dropna(how='any')
#    record_list = []
    stat_for = {}
    stat_against = {}
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
    for date, t1, t2, s1, s2, loc in np.array(data):
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
        stat_for[str(date)+t1+t2] = {'date':date, 'team1':t1, 'team2':t2, 'forstat1':fordict[t1], 'forstat2':fordict[t2]}
        stat_against[str(date)+t1+t2] = {'date':date, 'team1':t1, 'team2':t2, 'againststat1':againstdict[t1], 'againststat2':againstdict[t2]}

        s1_exp = (fordict[t1]+againstdict[t2])/2 + (loc * hf)
        s2_exp = (fordict[t2]+againstdict[t1])/2 - (loc * hf)
        s1_error = (s1 - s1_exp)/s1_exp
        s2_error = (s2 - s2_exp)/s2_exp
        fordict[t1] = fordict[t1] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink
        againstdict[t2] = againstdict[t2] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink
        fordict[t2] = fordict[t2] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink
        againstdict[t1] = againstdict[t1] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink 
#        record = (date, t1, t2, fordict[t1], againstdict[t2])
#        record_list.append(record)
    return stat_for, stat_against