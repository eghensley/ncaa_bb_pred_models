#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 16:12:16 2017

@author: eric.hensleyibm.com
"""

import mysql.connector 
import pandas as pd
passcode = 'ibm1234'
cnx = mysql.connector.connect(user='root', password=passcode,
                          host='127.0.0.1',
                          database='ncaa_bb') 
cursor = cnx.cursor()
query = "SELECT \
	ss.`teamname`,\
    ss.`scoredate`,\
    od.`favorite`,\
    od.`underdog`,\
	od.`homeaway`\
FROM\
    score_stats as ss\
    join oddsdata as od\
    on od.oddsdate = ss.scoredate and\
    (ss.teamname = od.favorite or ss.teamname = od.underdog)"

names = ['teamname', 'date', 'favorite', 'underdog', 'homeaway']  
cursor.execute(query)
data = pd.DataFrame(cursor.fetchall(), columns = names)

cursor.close()
cnx.close()

data.to_csv('home_away.csv')