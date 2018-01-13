#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 12:50:54 2017

@author: eric.hensleyibm.com
"""


def pull_targets_train(stat):
    import mysql.connector 
    import pandas as pd
    passcode = 'ibm1234'
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()
    query = "select al.teamname, avg(%s) from allow_stats as al join score_stats as sc on al.teamname = sc.teamname and al.allowdate = sc.scoredate where allowdate < '2010-11-01' group by teamname" % (stat) 
    labels = ['teamname', 'stat']
    cursor.execute(query)
    gamedata = pd.DataFrame(cursor.fetchall(), columns = labels)
    return gamedata



def pull_targets_test(stat, fa):
    import mysql.connector 
    import pandas as pd
    passcode = 'ibm1234'
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()
    query = "SELECT \
        oddsdate, favorite, underdog, bs1.`%s`, bs2.`%s`, homeaway\
    FROM\
        oddsdata AS od\
            JOIN\
        %s_stats AS bs1 ON od.oddsdate = bs1.%sdate\
            AND bs1.teamname = od.favorite\
            JOIN\
        %s_stats AS bs2 ON od.oddsdate = bs2.%sdate\
            AND bs2.teamname = od.underdog\
    WHERE\
        oddsdate > '2010-11-01'\
    ORDER BY oddsdate ASC" % (stat, stat, fa, fa, fa, fa)
    labels = ['date', 'fav', 'dog', 'favstat', 'dogstat', 'ha']
    cursor.execute(query)
    gamedata = pd.DataFrame(cursor.fetchall(), columns = labels)
    return gamedata

def pull_targets():
    import mysql.connector 
    import pandas as pd
    passcode = 'ibm1234'
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()
    query = 'SELECT * FROM ncaa_bb.allow_stats join ncaa_bb.score_stats on allow_stats.teamname = score_stats.teamname and allow_stats.allowdate = score_stats.scoredate'
    labels = ['teamname', 'allowdate', 'rebounding', 'fouling', 'foulrate', 'post', 'guarding', 'stealing', 'blocking', 'teamname', 'scoredate', 'shooting-efficiency', 'teamwork', 'chemistry', 'true-shooting-percentage']
    cursor.execute(query)
    gamedata = pd.DataFrame(cursor.fetchall(), columns = labels)
    return gamedata
    
    
    
def pull():
    import mysql.connector   
    import pandas as pd
    passcode = 'ibm1234'
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()
    
    cursor.execute('select favorite, \
    	underdog,\
        line,\
        overunder,\
        favscore,\
        dogscore,\
        homeaway,\
        bsfav.*,\
        bsdog.*\
        from oddsdata as od\
        join basestats as bsfav\
    		on od.oddsdate = bsfav.statdate AND\
            od.favorite = bsfav.teamname\
    	join basestats as bsdog\
    		on od.oddsdate = bsdog.statdate AND\
            od.underdog = bsdog.teamname;')
    
    labels = ["fav", "dog", "line", "ou", "favscore", "dogscore", "homeaway", "favteam", "favdate", "fav-points-per-game",
              "fav-offensive-efficiency","fav-floor-percentage","fav-points-from-2-pointers",
    "fav-points-from-3-pointers","fav-percent-of-points-from-2-pointers","fav-percent-of-points-from-3-pointers",
    "fav-percent-of-points-from-free-throws","fav-defensive-efficiency","fav-shooting-pct","fav-fta-per-fga","fav-ftm-per-100-possessions",
    "fav-free-throw-rate","fav-three-point-rate","fav-two-point-rate","fav-three-pointers-made-per-game","fav-effective-field-goal-pct",
    "fav-true-shooting-percentage","fav-offensive-rebounds-per-game","fav-offensive-rebounding-pct","fav-defensive-rebounds-per-game",
    "fav-defensive-rebounding-pct","fav-blocks-per-game","fav-steals-per-game","fav-block-pct","fav-steals-perpossession",
    "fav-steal-pct","fav-assists-per-game","fav-turnovers-per-game","fav-turnovers-per-possession","fav-assist--per--turnover-ratio",
    "fav-assists-per-fgm","fav-assists-per-possession","fav-turnover-pct","fav-personal-fouls-per-game","fav-personal-fouls-per-possession",
    "fav-personal-foul-pct","fav-possessions-per-game","fav-extra-chances-per-game","fav-effective-possession-ratio",
    "dogteam", "dogdate", "dog-points-per-game","dog-offensive-efficiency","dog-floor-percentage","dog-points-from-2-pointers",
    "dog-points-from-3-pointers","dog-percent-of-points-from-2-pointers","dog-percent-of-points-from-3-pointers","dog-percent-of-points-from-free-throws",
    "dog-defensive-efficiency","dog-shooting-pct","dog-fta-per-fga","dog-ftm-per-100-possessions","dog-free-throw-rate",
    "dog-three-point-rate","dog-two-point-rate","dog-three-pointers-made-per-game","dog-effective-field-goal-pct","dog-true-shooting-percentage",
    "dog-offensive-rebounds-per-game","dog-offensive-rebounding-pct","dog-defensive-rebounds-per-game","dog-defensive-rebounding-pct",
    "dog-blocks-per-game","dog-steals-per-game","dog-block-pct","dog-steals-perpossession","dog-steal-pct","dog-assists-per-game",
    "dog-turnovers-per-game","dog-turnovers-per-possession","dog-assist--per--turnover-ratio","dog-assists-per-fgm","dog-assists-per-possession",
    "dog-turnover-pct","dog-personal-fouls-per-game","dog-personal-fouls-per-possession","dog-personal-foul-pct","dog-possessions-per-game",
    "dog-extra-chances-per-game", "dog-effective-possession-ratio"]
    
    gamedata = pd.DataFrame(cursor.fetchall(), columns = labels)
    cursor.close()
    cnx.close()
    
    del gamedata['favteam']
    del gamedata['favdate']
    del gamedata['dogteam']
    del gamedata['dogdate']   
    
    return gamedata


def pull_reg():
    import mysql.connector   
    import pandas as pd
    passcode = 'ibm1234'
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()
    
    cursor.execute('select * from basestats;')

    
    labels = ["team", "date", "points", "offensive-efficiency","floor-percentage","points-from-2-pointers",
    "points-from-3-pointers","percent-of-points-from-2-pointers","percent-of-points-from-3-pointers",
    "percent-of-points-from-free-throws","defensive-efficiency","shooting-pct","fta-per-fga","ftm-per-100-possessions",
    "free-throw-rate","three-point-rate","two-point-rate","three-pointers-made-per-game","effective-field-goal-pct",
    "true-shooting-percentage","offensive-rebounds-per-game","offensive-rebounding-pct","defensive-rebounds-per-game",
    "defensive-rebounding-pct","blocks-per-game","steals-per-game","block-pct","steals-perpossession",
    "steal-pct","assists-per-game","turnovers-per-game","turnovers-per-possession","assist--per--turnover-ratio",
    "assists-per-fgm","assists-per-possession","turnover-pct","personal-fouls-per-game","personal-fouls-per-possession",
    "personal-foul-pct","possessions-per-game","extra-chances-per-game","effective-possession-ratio"]
    
    gamedata = pd.DataFrame(cursor.fetchall(), columns = labels)
    cursor.close()
    cnx.close()
    
    del gamedata['team']
    del gamedata['date']
      
    return gamedata


def pull_reg_wteam():
    import mysql.connector   
    import pandas as pd
    passcode = 'ibm1234'
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()
    
    cursor.execute('select * from basestats;')

    
    labels = ["team", "date", "points", "offensive-efficiency","floor-percentage","points-from-2-pointers",
    "points-from-3-pointers","percent-of-points-from-2-pointers","percent-of-points-from-3-pointers",
    "percent-of-points-from-free-throws","defensive-efficiency","shooting-pct","fta-per-fga","ftm-per-100-possessions",
    "free-throw-rate","three-point-rate","two-point-rate","three-pointers-made-per-game","effective-field-goal-pct",
    "true-shooting-percentage","offensive-rebounds-per-game","offensive-rebounding-pct","defensive-rebounds-per-game",
    "defensive-rebounding-pct","blocks-per-game","steals-per-game","block-pct","steals-perpossession",
    "steal-pct","assists-per-game","turnovers-per-game","turnovers-per-possession","assist--per--turnover-ratio",
    "assists-per-fgm","assists-per-possession","turnover-pct","personal-fouls-per-game","personal-fouls-per-possession",
    "personal-foul-pct","possessions-per-game","extra-chances-per-game","effective-possession-ratio"]
    
    gamedata = pd.DataFrame(cursor.fetchall(), columns = labels)
    cursor.close()
    cnx.close()
      
    return gamedata



def pull_margin():
    import mysql.connector   
    import pandas as pd
    import numpy as np
    passcode = 'ibm1234'
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()

    cursor.execute('select favorite, \
        underdog,\
        favscore,\
        dogscore,\
        bs.*\
        from oddsdata as od\
        join basestats as bs\
    		on od.oddsdate = bs.statdate AND\
        (od.favorite = bs.teamname OR od.underdog = bs.teamname);')
    
    labels = ['fav', 'dog', 'favscore', 'dogscore', "team", "date", "points", "offensive-efficiency","floor-percentage","points-from-2-pointers",
    "points-from-3-pointers","percent-of-points-from-2-pointers","percent-of-points-from-3-pointers",
    "percent-of-points-from-free-throws","defensive-efficiency","shooting-pct","fta-per-fga","ftm-per-100-possessions",
    "free-throw-rate","three-point-rate","two-point-rate","three-pointers-made-per-game","effective-field-goal-pct",
    "true-shooting-percentage","offensive-rebounds-per-game","offensive-rebounding-pct","defensive-rebounds-per-game",
    "defensive-rebounding-pct","blocks-per-game","steals-per-game","block-pct","steals-perpossession",
    "steal-pct","assists-per-game","turnovers-per-game","turnovers-per-possession","assist--per--turnover-ratio",
    "assists-per-fgm","assists-per-possession","turnover-pct","personal-fouls-per-game","personal-fouls-per-possession",
    "personal-foul-pct","possessions-per-game","extra-chances-per-game","effective-possession-ratio"]

    gamedata = pd.DataFrame(cursor.fetchall(), columns = labels)
    cursor.close()
    cnx.close()

    margin = [(np.array(gamedata['favscore'][i]) - np.array(gamedata['dogscore'])[i] if gamedata['team'][i] == gamedata['fav'][i] else np.array(gamedata['dogscore'])[i] - np.array(gamedata['favscore'])[i]) for i in range(0, len(gamedata))]
    gamedata['margin'] = margin
    del gamedata['fav']
    del gamedata['dog']
    del gamedata['favscore']
    del gamedata['dogscore']
    del gamedata['team']
    del gamedata['date']
    del gamedata['points']    
    return gamedata

def pull_pointsallowed():
    import mysql.connector   
    import pandas as pd
    import numpy as np
    passcode = 'ibm1234'
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()

    cursor.execute('select favorite, \
        underdog,\
        favscore,\
        dogscore,\
        bs.*\
        from oddsdata as od\
        join basestats as bs\
    		on od.oddsdate = bs.statdate AND\
        (od.favorite = bs.teamname OR od.underdog = bs.teamname);')
    
    labels = ['fav', 'dog', 'favscore', 'dogscore', "team", "date", "points", "offensive-efficiency","floor-percentage","points-from-2-pointers",
    "points-from-3-pointers","percent-of-points-from-2-pointers","percent-of-points-from-3-pointers",
    "percent-of-points-from-free-throws","defensive-efficiency","shooting-pct","fta-per-fga","ftm-per-100-possessions",
    "free-throw-rate","three-point-rate","two-point-rate","three-pointers-made-per-game","effective-field-goal-pct",
    "true-shooting-percentage","offensive-rebounds-per-game","offensive-rebounding-pct","defensive-rebounds-per-game",
    "defensive-rebounding-pct","blocks-per-game","steals-per-game","block-pct","steals-perpossession",
    "steal-pct","assists-per-game","turnovers-per-game","turnovers-per-possession","assist--per--turnover-ratio",
    "assists-per-fgm","assists-per-possession","turnover-pct","personal-fouls-per-game","personal-fouls-per-possession",
    "personal-foul-pct","possessions-per-game","extra-chances-per-game","effective-possession-ratio"]

    gamedata = pd.DataFrame(cursor.fetchall(), columns = labels)
    cursor.close()
    cnx.close()

    allowed = [np.array(gamedata['dogscore'])[i] if np.array(gamedata['team'])[i] == np.array(gamedata['fav'])[i] else np.array(gamedata['favscore'])[i] for i in range(0, len(gamedata))]
    gamedata['allowed'] = allowed
    del gamedata['fav']
    del gamedata['dog']
    del gamedata['favscore']
    del gamedata['dogscore']
    del gamedata['team']
    del gamedata['date']
    del gamedata['points']    
    return gamedata

def pull_pointsallowed_wteam():
    import mysql.connector   
    import pandas as pd
    import numpy as np
    passcode = 'ibm1234'
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()

    cursor.execute('select favorite, \
        underdog,\
        favscore,\
        dogscore,\
        bs.*\
        from oddsdata as od\
        join basestats as bs\
    		on od.oddsdate = bs.statdate AND\
        (od.favorite = bs.teamname OR od.underdog = bs.teamname);')
    
    labels = ['fav', 'dog', 'favscore', 'dogscore', "team", "date", "points", "offensive-efficiency","floor-percentage","points-from-2-pointers",
    "points-from-3-pointers","percent-of-points-from-2-pointers","percent-of-points-from-3-pointers",
    "percent-of-points-from-free-throws","defensive-efficiency","shooting-pct","fta-per-fga","ftm-per-100-possessions",
    "free-throw-rate","three-point-rate","two-point-rate","three-pointers-made-per-game","effective-field-goal-pct",
    "true-shooting-percentage","offensive-rebounds-per-game","offensive-rebounding-pct","defensive-rebounds-per-game",
    "defensive-rebounding-pct","blocks-per-game","steals-per-game","block-pct","steals-perpossession",
    "steal-pct","assists-per-game","turnovers-per-game","turnovers-per-possession","assist--per--turnover-ratio",
    "assists-per-fgm","assists-per-possession","turnover-pct","personal-fouls-per-game","personal-fouls-per-possession",
    "personal-foul-pct","possessions-per-game","extra-chances-per-game","effective-possession-ratio"]

    gamedata = pd.DataFrame(cursor.fetchall(), columns = labels)
    cursor.close()
    cnx.close()

    allowed = [np.array(gamedata['dogscore'])[i] if np.array(gamedata['team'])[i] == np.array(gamedata['fav'])[i] else np.array(gamedata['favscore'])[i] for i in range(0, len(gamedata))]
    gamedata['allowed'] = allowed
    del gamedata['fav']
    del gamedata['dog']
    del gamedata['favscore']
    del gamedata['dogscore']
#    del gamedata['team']
#    del gamedata['date']
    del gamedata['points']    
    return gamedata

def pull_share():
    import mysql.connector   
    import pandas as pd
    import numpy as np
    passcode = 'ibm1234'
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()

    cursor.execute('select favorite, \
        underdog,\
        favscore,\
        dogscore,\
        bs.*\
        from oddsdata as od\
        join basestats as bs\
    		on od.oddsdate = bs.statdate AND\
        (od.favorite = bs.teamname OR od.underdog = bs.teamname);')
    
    labels = ['fav', 'dog', 'favscore', 'dogscore', "team", "date", "points", "offensive-efficiency","floor-percentage","points-from-2-pointers",
    "points-from-3-pointers","percent-of-points-from-2-pointers","percent-of-points-from-3-pointers",
    "percent-of-points-from-free-throws","defensive-efficiency","shooting-pct","fta-per-fga","ftm-per-100-possessions",
    "free-throw-rate","three-point-rate","two-point-rate","three-pointers-made-per-game","effective-field-goal-pct",
    "true-shooting-percentage","offensive-rebounds-per-game","offensive-rebounding-pct","defensive-rebounds-per-game",
    "defensive-rebounding-pct","blocks-per-game","steals-per-game","block-pct","steals-perpossession",
    "steal-pct","assists-per-game","turnovers-per-game","turnovers-per-possession","assist--per--turnover-ratio",
    "assists-per-fgm","assists-per-possession","turnover-pct","personal-fouls-per-game","personal-fouls-per-possession",
    "personal-foul-pct","possessions-per-game","extra-chances-per-game","effective-possession-ratio"]

    gamedata = pd.DataFrame(cursor.fetchall(), columns = labels)
    cursor.close()
    cnx.close()

    share = [np.array(gamedata['favscore'][i])/(np.array(gamedata['favscore'][i]) + np.array(gamedata['dogscore'])[i]) if np.array(gamedata['team'])[i] == np.array(gamedata['fav'])[i] else np.array(gamedata['dogscore'])[i]/(np.array(gamedata['dogscore'])[i] + np.array(gamedata['favscore'])[i]) for i in range(0, len(gamedata))]
    gamedata['share'] = share
    del gamedata['fav']
    del gamedata['dog']
    del gamedata['favscore']
    del gamedata['dogscore']
    del gamedata['team']
    del gamedata['date']
    del gamedata['points']    
    return gamedata



def pull_elo():
    import mysql.connector   
    import pandas as pd
    passcode = 'ibm1234'
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()
    
    cursor.execute('select favorite, \
    	underdog,\
        line,\
        overunder,\
        favscore,\
        dogscore,\
        homeaway,\
        bsfav.*,\
        bsdog.*\
        from oddsdata as od\
        join basestats as bsfav\
    		on od.oddsdate = bsfav.statdate AND\
            od.favorite = bsfav.teamname\
    	join basestats as bsdog\
    		on od.oddsdate = bsdog.statdate AND\
            od.underdog = bsdog.teamname;')
    
    labels = ["fav", "dog", "line", "ou", "favscore", "dogscore", "homeaway", "favteam", "favdate", "fav-points-per-game",
              "fav-offensive-efficiency","fav-floor-percentage","fav-points-from-2-pointers",
    "fav-points-from-3-pointers","fav-percent-of-points-from-2-pointers","fav-percent-of-points-from-3-pointers",
    "fav-percent-of-points-from-free-throws","fav-defensive-efficiency","fav-shooting-pct","fav-fta-per-fga","fav-ftm-per-100-possessions",
    "fav-free-throw-rate","fav-three-point-rate","fav-two-point-rate","fav-three-pointers-made-per-game","fav-effective-field-goal-pct",
    "fav-true-shooting-percentage","fav-offensive-rebounds-per-game","fav-offensive-rebounding-pct","fav-defensive-rebounds-per-game",
    "fav-defensive-rebounding-pct","fav-blocks-per-game","fav-steals-per-game","fav-block-pct","fav-steals-perpossession",
    "fav-steal-pct","fav-assists-per-game","fav-turnovers-per-game","fav-turnovers-per-possession","fav-assist--per--turnover-ratio",
    "fav-assists-per-fgm","fav-assists-per-possession","fav-turnover-pct","fav-personal-fouls-per-game","fav-personal-fouls-per-possession",
    "fav-personal-foul-pct","fav-possessions-per-game","fav-extra-chances-per-game","fav-effective-possession-ratio",
    "dogteam", "dogdate", "dog-points-per-game","dog-offensive-efficiency","dog-floor-percentage","dog-points-from-2-pointers",
    "dog-points-from-3-pointers","dog-percent-of-points-from-2-pointers","dog-percent-of-points-from-3-pointers","dog-percent-of-points-from-free-throws",
    "dog-defensive-efficiency","dog-shooting-pct","dog-fta-per-fga","dog-ftm-per-100-possessions","dog-free-throw-rate",
    "dog-three-point-rate","dog-two-point-rate","dog-three-pointers-made-per-game","dog-effective-field-goal-pct","dog-true-shooting-percentage",
    "dog-offensive-rebounds-per-game","dog-offensive-rebounding-pct","dog-defensive-rebounds-per-game","dog-defensive-rebounding-pct",
    "dog-blocks-per-game","dog-steals-per-game","dog-block-pct","dog-steals-perpossession","dog-steal-pct","dog-assists-per-game",
    "dog-turnovers-per-game","dog-turnovers-per-possession","dog-assist--per--turnover-ratio","dog-assists-per-fgm","dog-assists-per-possession",
    "dog-turnover-pct","dog-personal-fouls-per-game","dog-personal-fouls-per-possession","dog-personal-foul-pct","dog-possessions-per-game",
    "dog-extra-chances-per-game", "dog-effective-possession-ratio"]
    
    gamedata = pd.DataFrame(cursor.fetchall(), columns = labels)
    cursor.close()
    cnx.close()
    
    keep = gamedata[['fav', 'dog', 'favdate']]
    keep['margin'] = gamedata['favscore'] - gamedata['dogscore']

    min(keep.favdate)
    del gamedata['team']
    del gamedata['date']
      
    return gamedata