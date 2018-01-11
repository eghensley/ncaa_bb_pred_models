#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 16:09:49 2018

@author: eric.hensleyibm.com
"""
# compass


import pandas as pd
import mysql.connector 
import numpy as np

def stat_actual(stat):
    passcode = 'ibm1234'   
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
            ORDER BY oddsdate ASC" % (stat, stat)
    cursor.execute(query)
    names = ['date', 'fav', 'dog', 'favstat', 'dogstat', 'ha']
    data = pd.DataFrame(cursor.fetchall(), columns = names)
    data=data.dropna(how='any')
    cursor.close()
    cnx.close()
    statdict = {}
    for date, t1, t2, s1, s2, loc in np.array(data):
        statdict[str(date)+t1.replace(' ', '_')] = {'date':date, 'team':t1, 'stat_actual':s1}
        statdict[str(date)+t2.replace(' ', '_')] = {'date':date, 'team':t2, 'stat_actual':s2}
    return statdict


def trigger_actual(trigger):
    passcode = 'ibm1234'   
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()
    query = "SELECT scoredate, teamname, %s FROM ncaa_bb.score_stats ORDER BY scoredate ASC" % (trigger)
    cursor.execute(query)
    names = ['date', 'team', 'trigger']
    data = pd.DataFrame(cursor.fetchall(), columns = names)
    data=data.dropna(how='any')
    cursor.close()
    cnx.close()
    statdict = {}
    for date, t, s in np.array(data):
        statdict[str(date)+t.replace(' ', '_')] = {'date':date, 'team':t, 'trigger':s}
    return statdict




def team_rolling_avg_weighted(stat, length):
#    stat = 'true-shooting-percentage'
#    length = 6      
    passcode = 'ibm1234'   
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
            ORDER BY oddsdate ASC" % (stat, stat)
    cursor.execute(query)
    names = ['date', 'fav', 'dog', 'favstat', 'dogstat', 'ha']
    data = pd.DataFrame(cursor.fetchall(), columns = names)
    data=data.dropna(how='any')
    cursor.close()
    cnx.close()
    
#    forlist = []
#    againstlist = []
    fordict = {}
    againstdict = {}
    alloweddict = {}
    scoredict = {}
    
    for date, t1, t2, s1, s2, loc in np.array(data):
        t1_current_allow = None
        t2_current_allow = None
        t1_current_score = None
        t2_current_score = None
        
        t1_weighted_score = None
        t2_weighted_score = None
        t1_weighted_allowed = None
        t2_weighted_allowed = None
        try:
            t1_current_allow = alloweddict[t1]
        except KeyError:
            t1_current_allow = False
        try:
            t2_current_allow = alloweddict[t2]
        except KeyError:
            t2_current_allow = False
    
        try:
            t1_current_score = scoredict[t1]
        except KeyError:
            t1_current_score= False
    
        try:
            t2_current_score = scoredict[t2]
        except KeyError:
            t2_current_score = False
    
    
        if not t2_current_allow:
            t1_weighted_score = 'NULL'
        else:
            t1_weighted_score = s1/np.mean(t2_current_allow)
        if not t1_current_allow:
            t2_weighted_score = 'NULL'
        else:
            t2_weighted_score = s2/np.mean(t1_current_allow)
                  
    
        if not t2_current_score:
            t1_weighted_allowed = 'NULL'
        else:
            t1_weighted_allowed = s1/np.mean(t2_current_score)
        if not t1_current_score:
            t2_weighted_allowed = 'NULL'
        else:
            t2_weighted_allowed = s2/np.mean(t1_current_score)        
           
#        for_record = (date, t1, t2, t1_weighted_score, t2_weighted_score)
#        against_record = (date, t1, t2, t1_weighted_allowed, t2_weighted_allowed)
        fordict[str(date)+t1.replace(' ', '_')] = {'date':date, 'team':t1, '%s_g_Tweight_for_%s'%(length, stat):t1_weighted_score}
        fordict[str(date)+t2.replace(' ', '_')] = {'date':date, 'team':t2, '%s_g_Tweight_for_%s'%(length, stat):t2_weighted_score}
        againstdict[str(date)+t1.replace(' ', '_')] = {'date':date, 'team':t1, '%s_g_Tweight_allow_%s'%(length, stat):t1_weighted_allowed}
        againstdict[str(date)+t2.replace(' ', '_')] = {'date':date, 'team':t2, '%s_g_Tweight_allow_%s'%(length, stat):t2_weighted_allowed}
        
#        forlist.append(for_record)    
#        againstlist.append(against_record)    
        
        if not t1_current_allow:
            t1_current_allow = [s2]
        else:
            t1_current_allow.append(s2)
        if not t1_current_score:
            t1_current_score = [s1]
        else:
            t1_current_score.append(s1)        
    
        if not t2_current_score:
            t2_current_score = [s2]
        else:
            t2_current_score.append(s2)
        if not t2_current_allow:
            t2_current_allow = [s1]
        else:
            t2_current_allow.append(s1) 
        
        if t1_current_allow and len(t1_current_allow) > length:
            t1_current_allow = t1_current_allow[len(t1_current_allow)-(length):]
        if t2_current_allow and len(t2_current_allow) > length:
            t2_current_allow = t2_current_allow[len(t2_current_allow)-(length):]
        if t1_current_score and len(t1_current_score) > length:
            t1_current_score = t1_current_score[len(t1_current_score)-(length):]
        if t2_current_score and len(t2_current_score) > length:
            t2_current_score = t2_current_score[len(t2_current_score)-(length):]    

        if len(t2_current_score) != len(t2_current_allow):
            print('team 2 mismatch')
            break
        if len(t1_current_score) != len(t1_current_allow):
            print('team 1 mismatch')
            break    
        if len(t2_current_score) > length:
            print('team 2 over 5')
            break
        if len(t1_current_score) > length:
            print('team 1 over 5')
            break  
        alloweddict[t1] = t1_current_allow
        alloweddict[t2] = t2_current_allow
        scoredict[t1] = t1_current_score
        scoredict[t2] = t2_current_score
    
    return fordict, againstdict

def ha_switch(in_num):
    if in_num == 0:
        return 1
    elif in_num == 1:
        return 0

def ha_rolling_avg_weighted(stat, length):
    import pandas as pd
    import mysql.connector 
    import numpy as np   
#    stat = 'true-shooting-percentage'
#    length = 6  
    passcode = 'ibm1234'   
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
            ORDER BY oddsdate ASC" % (stat, stat)
    cursor.execute(query)
    names = ['date', 'fav', 'dog', 'favstat', 'dogstat', 'ha']
    data = pd.DataFrame(cursor.fetchall(), columns = names)
    data=data.dropna(how='any')
    cursor.close()
    cnx.close()
    
#    forlist = []
#    againstlist = []
    fordict = {}
    againstdict = {}
    alloweddict = {}
    scoredict = {}
    for date, t1, t2, s1, s2, loc in np.array(data):
        t1_current_allow = None
        t2_current_allow = None
        t1_current_score = None
        t2_current_score = None
        
        t1_weighted_score = None
        t2_weighted_score = None
        t1_weighted_allowed = None
        t2_weighted_allowed = None
        
        t1_ha_score_spread = None
        t1_ha_allow_spread = None
        t2_ha_score_spread = None
        t2_ha_allow_spread = None
        try:
            t1_current_allow = alloweddict[t1][loc]
        except KeyError:
            t1_current_allow = False
            alloweddict[t1] = [False, False]
        try:
            t2_current_allow = alloweddict[t2][ha_switch(loc)]
        except KeyError:
            t2_current_allow = False
            alloweddict[t2] = [False, False]
    
        try:
            t1_current_score = scoredict[t1][loc]
        except KeyError:
            t1_current_score= False
            scoredict[t1] = [False, False]
            
        try:
            t2_current_score = scoredict[t2][ha_switch(loc)]
        except KeyError:
            t2_current_score = False
            scoredict[t2] = [False, False]
    
        if not t2_current_allow:
            t1_weighted_score = 'NULL'
        else:
            t1_weighted_score = s1/np.mean(t2_current_allow)
        if not t1_current_allow:
            t2_weighted_score = 'NULL'
        else:
            t2_weighted_score = s2/np.mean(t1_current_allow)
                  
    
        if not t2_current_score:
            t1_weighted_allowed = 'NULL'
        else:
            t1_weighted_allowed = s1/np.mean(t2_current_score)
        if not t1_current_score:
            t2_weighted_allowed = 'NULL'
        else:
            t2_weighted_allowed = s2/np.mean(t1_current_score)        
        
        
        
        if t1_current_score and scoredict[t1][ha_switch(loc)]:
            try:
                t1_ha_score_spread = np.mean(scoredict[t1][0]) - np.mean(scoredict[t1][1])
            except IndexError:
                t1_ha_score_spread = 'NULL'
        else:
            t1_ha_score_spread = 'NULL'
    
        if t2_current_score and scoredict[t2][loc]:
            try:
                t2_ha_score_spread = np.mean(scoredict[t2][0]) - np.mean(scoredict[t2][1])
            except IndexError:
                t2_ha_score_spread = 'NULL'
        else:
            t2_ha_score_spread = 'NULL'
        
     
        
        if t1_current_allow and alloweddict[t1][ha_switch(loc)]:
            try:
                t1_ha_allow_spread = np.mean(alloweddict[t1][0]) - np.mean(alloweddict[t1][1])
            except IndexError:
                t1_ha_allow_spread = 'NULL'
        else:
            t1_ha_allow_spread = 'NULL'
    
        if t2_current_allow and alloweddict[t2][loc]:
            try:
                t2_ha_allow_spread = np.mean(alloweddict[t2][0]) - np.mean(alloweddict[t2][1])
            except IndexError:
                t2_ha_allow_spread = 'NULL'
        else:
            t2_ha_allow_spread = 'NULL'           
        
#        for_record = (date, t1, t2, t1_weighted_score, t2_weighted_score, t1_ha_score_spread, t2_ha_score_spread)
#        against_record = (date, t1, t2, t1_weighted_allowed, t2_weighted_allowed, t1_ha_allow_spread, t2_ha_allow_spread)

        fordict[str(date)+t1.replace(' ', '_')] = {'date':date, 'team':t1, '%s_g_HAweight_for_%s' % (length, stat):t1_weighted_score, '%s_g_HAspread_for_%s'%(length, stat): t1_ha_score_spread}
        fordict[str(date)+t2.replace(' ', '_')] = {'date':date, 'team':t2, '%s_g_HAweight_for_%s' % (length, stat):t2_weighted_score, '%s_g_HAspread_for_%s'%(length, stat): t2_ha_score_spread}
        againstdict[str(date)+t1.replace(' ', '_')] = {'date':date, 'team':t1, '%s_g_HAweight_allow_%s' % (length, stat):t1_weighted_allowed, '%s_g_HAspread_allow_%s'%(length, stat): t1_ha_allow_spread}
        againstdict[str(date)+t2.replace(' ', '_')] = {'date':date, 'team':t2, '%s_g_HAweight_allow_%s' % (length, stat):t2_weighted_allowed, '%s_g_HAspread_allow_%s'%(length, stat): t2_ha_allow_spread}
    
#        forlist.append(for_record)    
#        againstlist.append(against_record)    
        
        if not t1_current_allow:
            t1_current_allow = [s2]
        else:
            t1_current_allow.append(s2)
        if not t1_current_score:
            t1_current_score = [s1]
        else:
            t1_current_score.append(s1)        
    
        if not t2_current_score:
            t2_current_score = [s2]
        else:
            t2_current_score.append(s2)
        if not t2_current_allow:
            t2_current_allow = [s1]
        else:
            t2_current_allow.append(s1) 
        
        if t1_current_allow and len(t1_current_allow) > length:
            t1_current_allow = t1_current_allow[len(t1_current_allow)-(length):]
        if t2_current_allow and len(t2_current_allow) > length:
            t2_current_allow = t2_current_allow[len(t2_current_allow)-(length):]
        if t1_current_score and len(t1_current_score) > length:
            t1_current_score = t1_current_score[len(t1_current_score)-(length):]
        if t2_current_score and len(t2_current_score) > length:
            t2_current_score = t2_current_score[len(t2_current_score)-(length):]    
    
        if len(t2_current_score) != len(t2_current_allow):
            print('team 2 mismatch')
            break
        if len(t1_current_score) != len(t1_current_allow):
            print('team 1 mismatch')
            break    
        if len(t2_current_score) > length:
            print('team 2 over %s' % (length))
            break
        if len(t1_current_score) > length:
            print('team 1 over %' % (length))
            break  
        if loc == 0:
            scoredict[t1] = [t1_current_score, scoredict[t1][1]]
            alloweddict[t1] = [t1_current_allow, alloweddict[t1][1]]
            alloweddict[t2] = [alloweddict[t2][0], t2_current_allow]
            scoredict[t2] = [scoredict[t2][0], t2_current_score]
        else:
            alloweddict[t1] = [alloweddict[t1][0], t1_current_allow]
            scoredict[t1] = [scoredict[t1][0], t1_current_score]
            scoredict[t2] = [t2_current_score, scoredict[t2][1]]
            alloweddict[t2] = [t2_current_allow, alloweddict[t2][1]]        
    return fordict, againstdict
    
        
        
        
        