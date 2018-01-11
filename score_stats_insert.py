#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 14:09:48 2017

@author: eric.hensleyibm.com
"""

from pca_clust import scored_clust_wteam
from sklearn.preprocessing import StandardScaler
import mysql.connector 
import numpy as np  
passcode = 'ibm1234'
cnx = mysql.connector.connect(user='root', password=passcode,
                          host='127.0.0.1',
                          database='ncaa_bb') 
cursor = cnx.cursor()
    
x, y, iid = scored_clust_wteam(9, 4, StandardScaler())

x1 = x[1]
x2 = x[2]
x3 = x[3]
x4 = x[4]
names = iid['team']
dates = iid['date']

for name, date, xval1, xval2, xval3, xval4 in zip(names, dates, x1, x2, x3, x4):
    cursor.execute(('INSERT INTO ncaa_bb.score_stats VALUES ("%s", "%s", %s, %s, %s, %s' % (name, date, xval1, xval2, xval3, xval4)) + ');')
    cnx.commit()
cursor.close()
cnx.close()
