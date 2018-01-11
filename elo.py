#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 13:11:21 2017

@author: eric.hensleyibm.com
"""

import mysql.connector 
import pandas as pd
passcode = 'ibm1234'
cnx = mysql.connector.connect(user='root', password=passcode,
                          host='127.0.0.1',
                          database='ncaa_bb') 
cursor = cnx.cursor()
query = "select teamname, (select avg(`points-per-game`) from basestats as bs join gamedata as gd on bs.teamname = gd.teamname and bs.statdate = gd.`date` where gd.teamname = tn.teamname and bs.statdate < '2010-11-01'), (select avg(`points-per-game`) from basestats as bs join gamedata as gd on bs.teamname = gd.teamname and bs.statdate = gd.`date` where gd.opponent = tn.teamname and bs.statdate < '2010-11-01') from teamnames as tn"
cursor.execute(query)
names = ['name', 'scored', 'allowed']
pastdata = pd.DataFrame(cursor.fetchall(), columns = names)
cursor.close()
cnx.close()

scoredict = {}
for i in range(0, len(pastdata['name'])):
    scoredict[pastdata['name'][i]] = pastdata['scored'][i]
allowdict = {}
for i in range(0, len(pastdata['name'])):
    allowdict[pastdata['name'][i]] = pastdata['scored'][i]
    
    
cnx = mysql.connector.connect(user='root', password=passcode,
                          host='127.0.0.1',
                          database='ncaa_bb') 
cursor = cnx.cursor()
query = "select favorite, underdog, favscore, dogscore, homeaway from oddsdata where oddsdate > '2010-11-01' order by oddsdate asc"
cursor.execute(query)
names = ['fav', 'dog', 'dogscore', 'favscore', 'ha']
data = pd.DataFrame(cursor.fetchall(), columns = names)
cursor.close()
cnx.close()

for i in range(0, len(data['name'])):
    
