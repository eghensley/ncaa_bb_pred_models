#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 14:09:48 2017

@author: eric.hensleyibm.com
"""

from pca_clust import allowed_clust_wteam
from sklearn.preprocessing import RobustScaler
import mysql.connector 
import numpy as np  
passcode = 'ibm1234'
cnx = mysql.connector.connect(user='root', password=passcode,
                          host='127.0.0.1',
                          database='ncaa_bb') 
cursor = cnx.cursor()
    
x, y, iid = allowed_clust_wteam(9, 7, RobustScaler())

x1 = x[1]
x2 = x[2]
x3 = x[3]
x4 = x[4]
x5 = x[5]
x6 = x[6]
x7 = x[7]
names = iid['team']
dates = iid['date']

for name, date, xval1, xval2, xval3, xval4, xval5, xval6, xval7 in zip(names, dates, x1, x2, x3, x4, x5, x6, x7):
    cursor.execute(('INSERT INTO ncaa_bb.allow_stats VALUES ("%s", "%s", %s, %s, %s, %s, %s, %s, %s' % (name, date, xval1, xval2, xval3, xval4, xval5, xval6, xval7)) + ');')
    cnx.commit()
cursor.close()
cnx.close()
