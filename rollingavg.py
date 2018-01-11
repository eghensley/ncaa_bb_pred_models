#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 15:34:03 2017

@author: eric.hensleyibm.com
"""
import mysql.connector 
import pandas as pd
passcode = 'ibm1234'
cnx = mysql.connector.connect(user='root', password=passcode,
                          host='127.0.0.1',
                          database='ncaa_bb') 
cursor = cnx.cursor()
query = 'SELECT \
	ss.`teamname`,\
    ss.`scoredate`,\
    ss.`shooting-efficiency`,\
    ss.`teamwork`,\
    ss.`chemistry`,\
    ss.`true-shooting-percentage`,\
    (select AVG(`points-per-game`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`offensive-efficiency`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
	(select AVG(`floor-percentage`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`points-from-2-pointers`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`points-from-3-pointers`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`percent-of-points-from-2-pointers`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`percent-of-points-from-3-pointers`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`percent-of-points-from-free-throws`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`defensive-efficiency`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`shooting-pct`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`fta-per-fga`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`ftm-per-100-possessions`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`free-throw-rate`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`three-point-rate`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`two-point-rate`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`three-pointers-made-per-game`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`effective-field-goal-pct`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`true-shooting-percentage`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`offensive-rebounds-per-game`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`offensive-rebounding-pct`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`defensive-rebounds-per-game`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`defensive-rebounding-pct`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`blocks-per-game`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`steals-per-game`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`block-pct`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`steals-perpossession`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`steal-pct`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`assists-per-game`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`turnovers-per-game`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`turnovers-per-possession`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`assist--per--turnover-ratio`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`assists-per-fgm`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`assists-per-possession`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`turnover-pct`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
 	(select AVG(`personal-fouls-per-game`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`personal-fouls-per-possession`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`personal-foul-pct`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`possessions-per-game`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`extra-chances-per-game`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname),\
    (select AVG(`effective-possession-ratio`) from basestats as bs where bs.statdate < ss.scoredate and bs.teamname = ss.teamname)\
FROM\
    score_stats as ss'

names = ['teamname', 'date', 'shooting-efficiency', 'teamwork', 'chemistry', 'true-shooting-percentage', 'points-per-game','offensive-efficiency', 'floor-percentage', 'points-from-2-pointers', 'points-from-3-pointers', 'percent-of-points-from-2-pointers', 'percent-of-points-from-3-pointers', 'percent-of-points-from-free-throws', 'defensive-efficiency', 'shooting-pct', 'fta-per-fga', 'ftm-per-100-possessions', 'free-throw-rate', 'three-point-rate', 'two-point-rate', 'three-pointers-made-per-game', 'effective-field-goal-pct', 'true-shooting-percentage', 'offensive-rebounds-per-game', 'offensive-rebounding-pct', 'defensive-rebounds-per-game', 'defensive-rebounding-pct', 'blocks-per-game', 'steals-per-game', 'block-pct', 'steals-perpossession', 'steal-pct', 'assists-per-game', 'turnovers-per-game', 'turnovers-per-possession', 'assist--per--turnover-ratio', 'assists-per-fgm', 'assists-per-possession', 'turnover-pct', 'personal-fouls-per-game', 'personal-fouls-per-possession', 'personal-foul-pct', 'possessions-per-game', 'extra-chances-per-game', 'effective-possession-ratio']  
cursor.execute(query)
data = pd.DataFrame(cursor.fetchall(), columns = names)

cursor.close()
cnx.close()

data.to_csv('average_stats.csv')