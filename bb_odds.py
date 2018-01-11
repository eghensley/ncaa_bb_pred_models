#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 18:54:13 2017

@author: eric.hensleyibm.com
"""

import mysql.connector   
import requests
from lxml import html
import datetime
from mysql.connector import IntegrityError
from datetime import date

passcode = 'ibm1234'
cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb')    
cursor = cnx.cursor() 
cursor.execute('SET SQL_SAFE_UPDATES = 0;')
cursor.execute('DELETE FROM ncaa.oddsdata WHERE favscore is NULL;')
cursor.execute('SET SQL_SAFE_UPDATES = 1;')
cnx.commit()
offseason = [5,6,7,8,9,10]
start_date = date(2009, 11, 10)
date1 = datetime.datetime.now()
date1 = date1 + datetime.timedelta(days=-1)
dates = []
while 1 != 2:
    new_date = start_date + datetime.timedelta(days=1)
    if new_date != date(date1.year,date1.month,date1.day):
        urldate = '%s-%s-%s' % (new_date.year, new_date.month, new_date.day)
        if new_date.month not in offseason:
            dates.append(urldate)
        start_date = new_date
    else:
        break     
teamnames = ['American', 'Beth-Cook', 'Charl South', 'AR Lit Rock', 'AR Lit Rock', 'Abilene Christian', 'Air Force', 'Akron', 'Alab A&M', 'Alabama', 'Alabama St', 
             'Albany', 'Alcorn State', 'American', 'App State', 'App State', 'Arizona', 'Arizona St', 'Ark Pine Bl', 
             'Arkansas', 'Arkansas St', 'Army', 'Auburn', 'Austin Peay', 'BYU', 'BYU', 'Ball State', 'Baylor', 
             'Belmont', 'Beth-Cook', 'Binghamton', 'Boise State', 'Boston Col', 'Boston U', 'Bowling Grn',
             'Bradley', 'Brown', 'Bryant', 'Bucknell', 'Buffalo', 'Butler', 'CS Bakersfld', 'CS Bakersfld', 'CS Fullerton', 
             'Cal Poly', 'Cal St Nrdge', 'California', 'Campbell', 'Canisius', 'Central Ark', 'Central Conn', 'Central Ark',
             'Central FL', 'Central Mich', 'Charl South', 'Charlotte', 'Chattanooga', 'Chattanooga', 'Chattanooga', 'Chicago St', 'Chicago St', 'Chicago St', 'Cincinnati',
             'Citadel', 'Clemson', 'Cleveland St', 'Coastal Car', 'Col Charlestn', 'Colgate', 'Colorado', 
             'Colorado St', 'Columbia', 'Connecticut', 'Coppin State', 'Coppin State', 'Cornell', 'Creighton', 'Dartmouth', 
             'Davidson', 'Dayton', 'DePaul', 'Delaware', 'Delaware St', 'Denver', 'Denver', 'Detroit', 'Drake', 'Drexel',
             'Duke', 'Duquesne', 'E Carolina', 'E Illinois', 'E Kentucky', 'E Michigan', 'E Tenn St', 'E Washingtn', 'E Washingtn', 'E Tenn St', 
             'Elon', 'Evansville', 'F Dickinson', 'Fairfield', 'Fla Atlantic', 'Fla Gulf Cst', 'Fla Gulf Cst', 'Florida', 'Florida A&M', 'Florida A&M', 
             'Florida Intl', 'Florida St', 'Fordham', 'Fresno St', 'Furman', 'GA Southern', 'GA Tech', 'Gard-Webb', 
             'Geo Mason', 'Geo Wshgtn', 'Georgetown', 'Georgia', 'Georgia St', 'Gonzaga', 'Grambling St', 'Grand Canyon',
             'Hampton', 'Hartford', 'Harvard', 'Hawaii', 'High Point', 'High Point', 'Hofstra', 'Holy Cross', 'Holy Cross', 'Houston', 'Houston Bap', 
             'Howard', 'IL-Chicago', 'IPFW', 'IUPUI', 'Idaho', 'Idaho State', 'Illinois', 'Illinois St', 'Incarnate Word','Idaho',
             'Indiana', 'Indiana', 'Indiana St', 'Iona', 'Iowa', 'Iowa State', 'Jackson St', 'Jacksonville', 'James Mad',
             'Jksnville St', 'Kansas', 'Kansas St', 'Kennesaw St', 'Kent State', 'Kentucky', 'LA Lafayette', 'LA Lafayette', 'LA Monroe', 'LA Monroe', 'Kennesaw St',
             'LA Tech', 'LIU-Brooklyn', 'LIU-Brooklyn', 'LIU-Brooklyn', 'LSU', 'La Salle', 'La Salle', 'Lafayette', 'Lamar', 'Lehigh', 'Lg Beach St', 'Liberty', 
             'Lipscomb', 'Longwood', 'Louisville', 'Loyola Mymt', 'Loyola-Chi', 'Loyola-MD', 'Maine', 'Manhattan', 'Marist',
             'Marquette', 'Marshall', 'Maryland', 'Maryland BC', 'Maryland BC', 'Maryland ES', 'Maryland ES', 'Massachusetts Lowell', 'Massachusetts Lowell', 'McNeese St', 
             'Memphis', 'Memphis', 'Mercer', 'Miami (FL)', 'Miami (OH)', 'Michigan', 'Michigan St', 'Middle Tenn', 'Minnesota','Minnesota', 
             'Miss State', 'Miss Val St', 'Mississippi', 'Missouri', 'Missouri St', 'Monmouth', 'Montana', 'Montana St', 
             'Morehead St', 'Morgan St', 'Mt St Marys', 'Mt St Marys', 'Murray St', 'N Arizona', 'N Carolina', 'N Carolina', 'N Colorado', 'N Colorado', 'N Dakota St',  'N Dakota St',  'N Dakota St',
             'N Florida', 'N Hampshire', 'N Illinois', 'N Iowa', 'N Kentucky',  'N Kentucky', 'N Mex State', 'NC A&T', 'NC A&T', 'NC Central',  'N Illinois',
             'NC State', 'NC State', 'NC-Asheville', 'NC-Grnsboro', 'NC-Wilmgton', 'NJIT', 'NJIT','NW State', 'Navy', 'Neb Omaha', 'Neb Omaha', 'Nebraska', 
             'Nevada', 'New Mexico', 'New Orleans', 'Niagara', 'Nicholls St', 'Norfolk St',  'Norfolk St', 'North Dakota', 'North Texas',
             'Northeastrn', 'Northwestern', 'Northwestern', 'Notre Dame', 'Oakland', 'Ohio', 'Ohio State', 'Oklahoma', 'Oklahoma St', 
             'Old Dominion', 'Oral Roberts', 'Oregon', 'Oregon St', 'Pacific', 'Penn State', 'Pepperdine', 'Pittsburgh', 
             'Portland', 'Portland', 'Portland St', 'Prairie View', 'Prairie View', 'Presbyterian', 'Princeton', 'Providence', 'Purdue', 'Quinnipiac',
             'Radford', 'Rhode Island', 'Rice', 'Richmond', 'Rider', 'Rob Morris', 'Rob Morris', 'Rutgers', 'S Alabama', 'S Car State', 'S Car State', 
             'S Carolina', 'S Dakota St', 'S Dakota St', 'S Florida', 'S Illinois', 'S Illinois', 'S Methodist', 'S Mississippi', 'S Utah', 'SC Upstate', 'S Dakota St', 'S Dakota St', 'S Mississippi', 'SC Upstate',
             'SE Louisiana', 'SE Missouri', 'SE Missouri', 'SIU Edward', 'Sac State', 'Sacred Hrt', 'Saint Louis', 'Sam Hous St', 'Sam Hous St', 'Samford',
             'San Diego', 'San Diego St', 'San Fransco', 'San Jose St', 'Santa Clara', 'Savannah St', 'Seattle', 'Seton Hall',
             'Siena', 'South Dakota', 'Southern', 'St Bonavent', 'St Bonavent', 'St Fran (NY)', 'St Fran (PA)', 'St Johns', 'St Josephs', 
             'St Marys', 'St Peters', 'Stanford', 'Ste F Austin', 'Ste F Austin', 'Stetson', 'Stony Brook', 'Syracuse', 'TN Martin', 'TN Martin', 'TN State',
             'TN Tech', 'TX A&M-CC', 'TX Christian', 'TX El Paso', 'TX Southern', 'TX-Arlington', 'TX-Pan Am', 'TX-Pan Am', 'TX-Pan Am', 'TX-San Ant', 'TX-San Ant', 'TX-Arlington',
             'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas State', 'Texas Tech', 'Toledo', 'Towson', 'Troy', 'Tulane', 
             'Tulsa', 'U Mass', 'U Penn', 'UAB', 'UC Davis', 'UC Irvine', 'UC Irvine', 'UC Riverside', 'UCLA', 'UCSB', 'UCSB', 'UMKC', 'UMKC', 'UNLV', 
             'USC', 'Utah', 'Utah', 'Utah State', 'Utah Val St', 'VA Military', 'VA Tech', 'VCU', 'Valparaiso', 'Vanderbilt', 
             'Vermont', 'Villanova', 'Virginia', 'W Carolina', 'W Illinois', 'W Kentucky', 'W Michigan', 'W Virginia', 
             'WI-Grn Bay', 'WI-Milwkee', 'Wagner', 'Wake Forest', 'Wash State', 'Washington', 'Washington', 'Weber State', 'Wichita St',
             'Winthrop', 'Wisconsin', 'Wm & Mary', 'Wofford', 'Wright State', 'Wyoming', 'Xavier', 'Yale', 'Youngs St', 'N Colorado', 'Utah Val St', 'Southern']

teamlist = ['American', 'BETHUNE COOKMAN', 'Charleston Sou','Arkansas Lr', 'ARKANSAS LITTLE ROCK', 'Abilene Christian', 'Air Force', 'Akron', 'Alabama A&M', 'Alabama', 'Alabama State', 
             'Albany NY', 'Alcorn State', 'American Univ', 'Appalachian St', 'Appalachian State', 'Arizona', 'Arizona State', 'Ark Pine Bluff', 
             'Arkansas', 'Arkansas State', 'Army', 'Auburn', 'Austin Peay', 'BYU', 'BRIGYOUNG', 'Ball State', 'Baylor', 
             'Belmont', 'Bethune-Cookman', 'Binghamton', 'Boise State', 'Boston College', 'Boston U', 'Bowling Green',
             'Bradley', 'Brown', 'Bryant', 'Bucknell', 'Buffalo', 'Butler', 'CS Bakersfld', 'CS BAKERSFIELD', 'CS Fullerton', 
             'Cal Poly SLO', 'CS Northridge', 'California', 'Campbell', 'Canisius', 'Central Ark', 'Central Conn', 'Central Arkansas',
             'Central Florida', 'Central Michigan', 'Charleston So', 'Charlotte U', 'TENNESSEE Chat', 'TENN Chat', 'TENN CHATTANOOGA', 'Chicago State', 'Chicago St', 'Chicago St.', 'Cincinnati',
             'the Citadel', 'Clemson', 'Cleveland State', 'COASTAL CAROLINA', 'Coll Charleston', 'Colgate', 'Colorado', 
             'Colorado State', 'Columbia', 'Connecticut', 'Coppin State', 'COPPIN ST', 'Cornell', 'Creighton', 'Dartmouth', 
             'Davidson', 'Dayton', 'DePaul', 'Delaware', 'Delaware State', 'Denver U',  'Denver', 'Detroit', 'Drake', 'Drexel',
             'Duke', 'Duquesne', 'East Carolina', 'Eastern Illinois', 'Eastern Kentucky', 'Eastern Michigan', 'E Tennessee State', 'E Washington', 'E. Washington', 'E Tennessee St',
             'Elon', 'Evansville', 'F Dickinson', 'Fairfield', 'FLA Atlantic', 'Fla Gulf Cst', 'FLA GULF COAST', 'Florida', 'FLORIDAAM', 'FLORIDA A&M',
             'Florida Intl', 'Florida State', 'Fordham', 'Fresno State', 'Furman', 'Georgia Southern', 'Georgia Tech', 'Gardner Webb', 
             'George Mason', 'Geo Washington', 'Georgetown', 'Georgia', 'Georgia State', 'Gonzaga', 'Grambling', 'Grand Canyon',
             'Hampton', 'Hartford', 'Harvard', 'Hawaii', 'High Point', 'HIGHPOINT', 'Hofstra', 'Holy Cross', 'HOLYCROSS', 'Houston U', 'Houston Baptist', 
             'Howard', 'ILLINOIS CHICAGO', 'IPFW', 'IUPUI', 'Idaho U', 'Idaho State', 'Illinois', 'Illinois State', 'Incarnate Word', 'Idaho',
             'Indiana U', 'Indiana', 'Indiana State', 'Iona', 'Iowa', 'Iowa State', 'Jackson State', 'Jacksonville', 'James Madison',
             'Jacksonville St', 'Kansas', 'Kansas State', 'Kennesaw', 'Kent State', 'Kentucky', 'UL - LAFAYETTE', 'UL LAFAYETTE', 'UL - MONROE',  'UL MONROE', 'Kennesaw st',
             'Louisiana Tech', 'LIU BROOKLYN', 'LONG ISLAND', 'LONGISLAND', 'LSU', 'La Salle', 'LaSalle', 'Lafayette', 'Lamar', 'Lehigh', 'Long Beach State', 'Liberty', 
             'Lipscomb', 'Longwood', 'Louisville', 'LOYOLA Marymount', 'Loyola Chicago', 'Loyola Maryland', 'Maine', 'Manhattan', 'Marist',
             'Marquette', 'Marshall', 'Maryland', 'MD Baltimore Co', 'MD BALTIMORE COUNTY', 'Md Eastern Shore', 'MARYLAND EASTERN SHORE', 'Massachusetts Lowell', 'UMASS LOWELL', 'McNeese State', 
             'Memphis', 'Memphis U', 'Mercer', 'Miami FLorida', 'Miami OHIO', 'Michigan', 'Michigan State', 'Middle Tenn St', 'Minnesota U', 'Minnesota', 
             'Mississippi St', 'Miss Valley St', 'Mississippi', 'Missouri', 'Missouri St', 'Monmouth', 'Montana', 'Montana State', 
             'Morehead State', 'Morgan State', "Mt St Mary's", 'MOUNT ST MARYS', 'Murray State', 'Northern Arizona', 'UNC', 'NORTH CAROLINA', 'Northern Colorado', 'No. Colorado', 'N Dakota St', 'NORTH DAKOTA STATE', 'NORTH DAKOTA ST', 
             'North Florida', 'New Hampshire', 'No Illinois', 'Northern Iowa', 'N Kentucky', 'Northern Kentucky', 'New Mexico State', 'NC A&T', 'N. CAROLINA A&T', 'NC Central', 'Northern Illinois',
             'NC State', 'NCState', 'NC Asheville', 'NC Greensboro', 'NC Wilmington', 'NJIT', 'NEW JERSEY TECH', 'Northwestern ST', 'Navy', 'Neb Omaha', 'NEBRASKA OMAHA',  'Nebraska', 
             'Nevada', 'New Mexico', 'New Orleans U', 'Niagara', 'Nicholls State', 'Norfolk St', 'Norfolk State', 'North Dakota', 'North Texas',
             'Northeastern', 'Northwestern', 'NORTHWSTRN', 'Notre Dame', 'Oakland', 'Ohio', 'Ohio State', 'Oklahoma', 'Oklahoma State', 
             'Old Dominion', 'Oral Roberts', 'Oregon', 'Oregon State', 'Pacific', 'Penn State', 'Pepperdine', 'Pittsburgh', 
             'Portland U', 'Portland', 'Portland State', 'Prairie View', 'PRAIRIE VIEW A&M', 'Presbyterian', 'Princeton', 'Providence', 'Purdue', 'Quinnipiac',
             'Radford', 'Rhode Island', 'Rice', 'Richmond', 'Rider', 'Robert Morris', 'ROBERTMORRIS', 'Rutgers', 'South Alabama', 'So Carolina St', 'SOUTH CAROLINA STATE',
             'South Carolina', 'South Dakota St', 'South Dakota State', 'South Florida', 'So Illinois', 'SOUTHERN ILLINOIS', 'SMU', 'SO MISSISSIPPI', 'Southern Utah', 'SC Upstate', 'S Dakota St', 'SOUTH DAKOTA STATE', 'SOUTHERN MISS', 'USC Upstate',
             'SE Louisiana', 'SE Missouri St', 'SE Missouri State', 'SIU EDWARDSVILLE', 'Sacramento state', 'Sacred Heart', 'Saint Louis', 'SAMHOUSTON', 'SAM HOUSTON ST', 'Samford',
             'San Diego', 'San Diego State', 'San Francisco', 'San Jose State', 'Santa Clara', 'Savannah State', 'Seattle U', 'Seton Hall',
             'Siena', 'South Dakota', 'Southern Univ', 'St. Bonaventure', 'St Bonaventure', 'St. Francis NY', 'St. Francis PA', "St. John's", "ST. JOSEPH'S", 
              "SAINT MARY'S CA", "St. Peter's", 'Stanford', 'STEPHEN Austin', 'STEPHEN F. AUSTIN', 'Stetson', 'Stony Brook', 'Syracuse', 'TenN Martin', 'TENNESSEE Martin', 'Tennessee State',
             'Tennessee Tech', 'TEXAS A&M CORPUS', 'TCU', 'UTEP', 'Texas Southern', 'TEXAS Arlington', 'Texas-Pan American', 'TX PAN AMERICAN', 'UT RIO GRANDE VALLEY', 'Tex San Antonio', 'TEXAS SAN ANTONIO', 'UT ARLINGTON', 
             'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas State', 'Texas Tech', 'Toledo', 'Towson', 'Troy', 'Tulane', 
             'Tulsa', 'Massachusetts', 'PENNSYLVANIA', 'UAB', 'UC Davis', 'Cal Irvine', 'UC IRVINE', 'Cal Riverside', 'UCLA', 'CAL SANTA BARB', 'CAL SANTA BARBARA', 'UMKC', 'MO KANSAS CITY', 'UNLV', 
             'USC', 'Utah U', 'Utah', 'Utah State', 'Utah Valley', 'VMI', 'Virginia Tech', 'VA Commonwealth', 'Valparaiso', 'Vanderbilt', 
             'Vermont', 'Villanova', 'Virginia', 'Western Carolina', 'WESTERN Illinois', 'WESTERN Kentucky', 'Western Michigan', 'West Virginia', 
             'Wisc Green Bay', 'Wisc Milwaukee', 'Wagner', 'Wake Forest', 'Washington State', 'Washington U', 'Washington', 'Weber State', 'Wichita State',
             'Winthrop', 'Wisconsin', 'William & Mary', 'Wofford', 'Wright State', 'Wyoming', 'Xavier', 'Yale', 'Youngstown State', 'NOCOLORADO', 'Utah Valley st', 'SOUTHERN']    


oddsteamsdict = {}
for i in range(0, len(teamnames)):
#    print(teamst[i] + " - " + teamnames[i])
    oddsteamsdict[teamlist[i].upper()] = teamnames[i]

nond1 = ['WINSTON SALEM STATE', 'CHAMINADE', 'DICKINSON STATE', 'ARK MONTICELLO', 'FAIR DICKINSON', 'ARK-FORT SMITH', 'USC UPSTATE', 'NORTHERN MICHIGAN', 'CENTENARY', 'ALASKA ANCHORAGE', 
         'UNIV SCIENCES OF PHILA', '', 'DOWLING', 'ALA ANCHORAGE', 'DOMINICAN CAL', 'WESTERN NEW MEXICO', 'MONTREAT', 'ROCHESTER COLLEGE', 'WEST ALABAMA', 'LA SIERRA', 'SAN FRANCISCO STATE', 
         'MACMURRAY', 'ALABAMA-HUNTSVILLE', 'ALASKA FAIRBANKS', 'STILLMAN COLLEGE', 'METRO STATE', 'SONOMA ST', 'CAL POLY POMONA', 'BELLARMINE', 'INDIANA (PA)', 'DRURY', 'METROST', 'CENTRAL MISSOURI ST',
         'WEST LIBERTY', 'CONCORDIA ST. PAUL']

    
nonfbsteams = []
all_games = []
all_errors = []
favorite_errors = []
spot = 0
for gameday in dates[dates.index('2011-3-16'):]:
#for gameday in dates:
        spot += 1
        print('%s percent complete' % ((float(spot)/float(len(dates)))*100 + 20.629604822505023))
        url = None
        pageContent = None
        tree = None
        day = None
        month = None
        year = None
        if len(gameday.split('-')[2]) == 1:
            day = '0'+gameday.split('-')[2]
        elif len(gameday.split('-')[2]) == 2:
            day = gameday.split('-')[2]
        if len(gameday.split('-')[1]) == 1:
            month = '0'+gameday.split('-')[1]
        elif len(gameday.split('-')[1]) == 2:
            month = gameday.split('-')[1]
        year = gameday.split('-')[0]
        url = 'http://www.scoresandodds.com/grid_%s%s%s.html' % (year, month, day)
        pageContent=requests.get(url)
        tree = html.fromstring(pageContent.content)    
        for sport in range(1, 10):                    
            root = '/html/body/div[1]/table/tr/td/div[2]/div[1]/div[1]/table/tr[1]/td[1]/div[%s]' % (sport)
            sportpath = root+'/div[5]/div[1]/text()'
            if len(tree.xpath(sportpath)) > 0 and tree.xpath(sportpath)[0] == 'NCAA BB':
                team1root = '/div[6]/div[1]/table/tbody/tr[@class = "team odd"]'
                team2root = '/div[6]/div[1]/table/tbody/tr[@class = "team even"]'
                nameroot = '/td[1]/a/text()'
                namepath1 = None
                namepath2 = None
                team1namelist = None
                team2namelist = None
                team1overunderlist = None
                team2overunderlist = None
                team1linelist = None
                team2linelist = None
                team1moneylinelist = None
                team2moneylinelist = None
                team1scorelist = None
                team2scorelist = None
    
                namepath1 = root+team1root+nameroot
                namepath2 = root+team2root+nameroot
                
                team1namelist = tree.xpath(namepath1)
                team2namelist = tree.xpath(namepath2)
    
                team1linelist = []
                for l1 in range(1, len(team1namelist)+1):
                    lpath1 = root+'/div[6]/div[1]/table/tbody/tr[@class = "team odd"][position()=%s]/td[4]/text()' % (l1)
                    try:
                        team1linelist.append(tree.xpath(lpath1)[0])
                    except IndexError:
                        if tree.xpath(lpath1) == []:
                            team1linelist.append(None)
                                                 
                team2linelist = []
                for l2 in range(1, len(team2namelist)+1):
                    lpath2 = root+'/div[6]/div[1]/table/tbody/tr[@class = "team even"][position()=%s]/td[4]/text()' % (l2)
                    try:
                        team2linelist.append(tree.xpath(lpath2)[0])
                    except IndexError:
                        if tree.xpath(lpath2) == []:
                            team2linelist.append(None)            
                
                team1overunderlist = []
                for ou1 in range(1, len(team1namelist)+1):
                    oupath1 = root+'/div[6]/div[1]/table/tbody/tr[@class = "team odd"][position()=%s]/td[4]/text()' % (ou1)
                    try:
                        team1overunderlist.append(tree.xpath(oupath1)[0])
                    except IndexError:
                        if tree.xpath(oupath1) == []:
                            team1overunderlist.append('Null')
                
                team2overunderlist = []
                for ou2 in range(1, len(team2namelist)+1):
                    oupath2 = root+'/div[6]/div[1]/table/tbody/tr[@class = "team even"][position()=%s]/td[4]/text()' % (ou2)
                    try:
                        team2overunderlist.append(tree.xpath(oupath2)[0])
                    except IndexError:
                        if tree.xpath(oupath2) == []:
                            team2overunderlist.append('Null')     
                
                team1scorelist = []
                for s1 in range(1, len(team1namelist)+1):
                    spath1 = root+'/div[6]/div[1]/table/tbody/tr[@class = "team odd"][position()=%s]/td[7]/span[1]/text()' % (s1)
                    try:
                        team1scorelist.append(tree.xpath(spath1)[0])
                    except IndexError:
                        if tree.xpath(spath1) == []:
                            team1scorelist.append('Null')
    
                team2scorelist = []            
                for s2 in range(1, len(team2namelist)+1):
                    spath2 = root+'/div[6]/div[1]/table/tbody/tr[@class = "team even"][position()=%s]/td[7]/span[1]/text()' % (s2)
                    try:
                        team2scorelist.append(tree.xpath(spath2)[0])
                    except IndexError:
                        if tree.xpath(spath2) == []:
                            team2scorelist.append('Null')
                            
                team1moneylinelist = []
                for ml1 in range(1, len(team1namelist)+1):
                    mlpath1 = root+'/div[6]/div[1]/table/tbody/tr[@class = "team odd"][position()=%s]/td[5]/text()' % (ml1)
                    try:
                        team1moneylinelist.append(tree.xpath(mlpath1)[0])
                    except IndexError:
                        team1moneylinelist.append('Null')
                team2moneylinelist = []
                for ml2 in range(1, len(team2namelist)+1):
                    mlpath2 = root+'/div[6]/div[1]/table/tbody/tr[@class = "team even"][position()=%s]/td[5]/text()' % (ml2)
                    try:
                        team2moneylinelist.append(tree.xpath(mlpath2)[0])
                    except IndexError:
                        team2moneylinelist.append('Null')
                if len(team1namelist) == len(team2namelist) == len(team2moneylinelist) == len(team1moneylinelist) == len(team1scorelist) == len(team2scorelist) == len(team1linelist) == len(team2linelist) == len(team1overunderlist) == len(team2overunderlist): 
                    for each in range(0, len(team1namelist)):
                        try:
                            fbsgame = 'yes'
                            favorite = None
                            line = None
                            team1 = None
                            team2 = None
                            moneyline1 = None
                            moneyline2 = None
                            score1 = None
                            score2 = None
                            linejuice = None
                            overunder = None
                            overunderjuice = None
                            game = []
                            
                            try:
                                team1 = oddsteamsdict[team1namelist[each][4:].upper()]
                            except KeyError:
                                if team1namelist[each][4:].upper() not in nond1:
                                    print(team1namelist[each][4:].upper())
                                    print(url)
                                fbsgame = 'no'
                                pass
                            try:
                                team2 = oddsteamsdict[team2namelist[each][4:].upper()]
                            except KeyError:
                                if team2namelist[each][4:].upper() not in nond1:
                                    print(team2namelist[each][4:].upper())
                                    print(url)
                                fbsgame = 'no'
                                pass

                            if fbsgame == 'yes':                                
                                try:
                                    moneyline1 = float(team1moneylinelist[each])
                                except ValueError:
                                    if team1moneylinelist[each] == 'Null':
                                        moneyline1 = team1moneylinelist[each]
                                try:
                                    moneyline2 = float(team2moneylinelist[each])
                                except ValueError:
                                    if team2moneylinelist[each] == 'Null':
                                        moneyline2 = team2moneylinelist[each]
                                try:
                                    score1 = int(team1scorelist[each])
                                except ValueError:
                                    if team1scorelist[each] == 'Null':
                                        score1 = team1scorelist[each]
                                try:
                                    score2 = int(team2scorelist[each])
                                except ValueError:
                                    if team2scorelist[each] == 'Null':
                                        score2 = team2scorelist[each]
                                favorite1 = False
                                favorite2 = False
                                x1 = None
                                x2 = None
                                y1 = None
                                y2 = None
                                spacesplit1 = None
                                osplit1 = None
                                usplit1 = None
                                
                                if team1linelist[each] == None and team2linelist[each] == None:
                                    x1 = 'Null'
                                    x2 = 'Null'
                                    y1 = 'Null'
                                    y2 = 'Null'
                                    favorite1 = True
                                elif team1linelist[each] == None and team2linelist[each] != None:
                                    favorite2 = True
                                    x1 = 'Null'
                                    y1 = 'Null'
                                    try:
                                        x2 = float(team2linelist[each].strip().split(' ')[0])
                                    except ValueError:
                                        if team2linelist[each].strip().split(' ')[0] == 'PK':
                                            x2 = 0
                                            favorite2 = True                                          
                                    try:    
                                        y2 = float(team2linelist[each].strip().split(' ')[1])
                                    except IndexError:
                                        y2 = 0
                                    except ValueError:
                                        if team2linelist[each].strip().split(' ')[1] == 'EVEN':
                                            y2 = 0   
                                elif team2linelist[each] == None and team1linelist[each] != None:
                                    favorite1 = True
                                    try:
                                        x1 = float(team1linelist[each].strip().split(' ')[0])
                                    except ValueError:
                                        if team1linelist[each].strip().split(' ')[0] == 'PK':
                                            x1 = 0
                                            favorite1 = True                                       
                                    try:
                                        y1 = float(team1linelist[each].strip().split(' ')[1])
                                    except IndexError:
                                        y1 = 0
                                    except ValueError:
                                        if team1linelist[each].strip().split(' ')[1] == 'EVEN':
                                            y1 = 0                                        
                                    x2 = 'Null'
                                    y2 = 'Null'
                                elif team1linelist[each] != None and team2linelist[each] != None:                           
                                    spacesplit1 = team1linelist[each].strip().split(' ')
                                    osplit1 = team1linelist[each].strip().split('o')
                                    usplit1 = team1linelist[each].strip().split('u')
                                    
                                    if len(spacesplit1) == len(osplit1) == len(usplit1) == 1:
                                        try:
                                            x1 = float(team1linelist[each].strip())
                                        except ValueError:
                                            if team1linelist[each].strip() == 'PK':
                                                x1 = 0
                                                favorite1 = True
                                        y1 = 0
                                    elif len(spacesplit1) == 1 and len(osplit1) == 1 and len(usplit1) == 2:
                                        x1 = float(team1linelist[each].strip().split('u')[0])
                                        favorite2 = True
                                        y1 = float(team1linelist[each].strip().split('u')[1])
                                    elif len(spacesplit1) == 1 and len(osplit1) == 2 and len(usplit1) == 1:
                                        x1 = float(team1linelist[each].strip().split('o')[0])
                                        favorite2 = True
                                        y1 = float(team1linelist[each].strip().split('o')[1])      
                                    elif len(spacesplit1) == 2 and len(osplit1) == 1 and len(usplit1) == 1:
                                        try:
                                            x1 = float(team1linelist[each].strip().split(' ')[0])
                                            favorite1 = True
                                        except ValueError:
                                            if team1linelist[each].strip().split(' ')[0] == 'PK':
                                                x1 = 0
                                                favorite1 = True
                                        try:
                                            y1 = float(team1linelist[each].strip().split(' ')[1])
                                        except ValueError:
                                            if team1linelist[each].strip().split(' ')[1] == 'EVEN':
                                                y1 = 0
        
                                    spacesplit2 = team2linelist[each].strip().split(' ')
                                    osplit2 = team2linelist[each].strip().split('o')
                                    usplit2 = team2linelist[each].strip().split('u')                                        
                                    if len(spacesplit2) == len(osplit2) == len(usplit2) == 1:
                                        try:
                                            x2 = float(team2linelist[each].strip())
                                        except ValueError:
                                            if team2linelist[each].strip() == 'PK':
                                                x2 = 0
                                                favorite2 = True
                                        y2 = 0
                                    elif len(spacesplit2) == 1 and len(osplit2) == 1 and len(usplit2) == 2:
                                        x2 = float(team2linelist[each].strip().split('u')[0])
                                        favorite1 = True
                                        y2 = float(team2linelist[each].strip().split('u')[1])
                                    elif len(spacesplit2) == 1 and len(osplit2) == 2 and len(usplit2) == 1:
                                        x2 = float(team2linelist[each].strip().split('o')[0])
                                        favorite1 = True
                                        y2 = float(team2linelist[each].strip().split('o')[1])      
                                    elif len(spacesplit2) == 2 and len(osplit2) == 1 and len(usplit2) == 1:
                                        try:
                                            x2 = float(team2linelist[each].strip().split(' ')[0])
                                            favorite2 = True
                                        except ValueError:
                                            if team2linelist[each].strip().split(' ')[0] == 'PK':
                                                x2 = 0
                                                favorite2 = True
                                        try:
                                            y2 = float(team2linelist[each].strip().split(' ')[1])
                                        except ValueError:
                                            if team2linelist[each].strip().split(' ')[1] == 'EVEN':
                                                y2 = 0   

                                if favorite1 == favorite2 == True:
                                    pass
                                elif favorite1 == True and favorite2 == False:
                                    favorite = 1
                                    try:
                                        line = float(x1)
                                    except ValueError:
                                        if x1 == 'Null':
                                            line = str(x1)
                                    try:
                                        linejuice = float(y1)
                                    except ValueError:
                                        if y1 == 'Null':
                                            linejuice = str(y1)
                                    try:
                                        overunder = float(x2)
                                    except ValueError:
                                        if x2 == 'Null':
                                            overunder = str(x2)
                                    try:
                                        overunderjuice = float(y2) 
                                    except ValueError:
                                        if y2 == 'Null':
                                            overunderjuice = str(y2)                                
                                elif favorite1 == False and favorite2 == True:
                                    favorite = 2
                                    try:
                                        line = float(x2)
                                    except ValueError:
                                        if x2 == 'Null':
                                            line = str(x2)
                                    try:
                                        linejuice = float(y2)
                                    except ValueError:
                                        if y2 == 'Null':
                                            linejuice = str(y2)
                                    try:
                                        overunder = float(x1)
                                    except ValueError:
                                        if x1 == 'Null':
                                            overunder = str(x1)
                                    try:
                                        overunderjuice = float(y1) 
                                    except ValueError:
                                        if y1 == 'Null':
                                            overunderjuice = str(y1)
                                elif favorite1 == favorite2 == False:
                                    if x1 < 0:
                                        favorite = 1
                                        try:
                                            line = float(x1)
                                        except ValueError:
                                            if x1 == 'Null':
                                                line = str(x1)
                                        try:
                                            linejuice = float(y1)
                                        except ValueError:
                                            if y1 == 'Null':
                                                linejuice = str(y1)
                                        try:
                                            overunder = float(x2)
                                        except ValueError:
                                            if x2 == 'Null':
                                                overunder = str(x2)
                                        try:
                                            overunderjuice = float(y2) 
                                        except ValueError:
                                            if y2 == 'Null':
                                                overunderjuice = str(y2)                                   
                                    elif x2 < 0:
                                        favorite = 2
                                        try:
                                            line = float(x2)
                                        except ValueError:
                                            if x2 == 'Null':
                                                line = str(x2)
                                        try:
                                            linejuice = float(y2)
                                        except ValueError:
                                            if y2 == 'Null':
                                                linejuice = str(y2)
                                        try:
                                            overunder = float(x1)
                                        except ValueError:
                                            if x1 == 'Null':
                                                overunder = str(x1)
                                        try:
                                            overunderjuice = float(y1) 
                                        except ValueError:
                                            if y1 == 'Null':
                                                overunderjuice = str(y1) 
                                if favorite == 1:
                                    game = [gameday, team1, team2, line, linejuice, overunder, overunderjuice, moneyline1, moneyline2, score1, score2, 1]
                                elif favorite == 2:
                                    game = [gameday, team2, team1, line, linejuice, overunder, overunderjuice, moneyline2, moneyline1, score2, score1, 0]
                                if favorite == None:
                                    favorite_errors.append(url)
                                else:
                                    all_games.append(game)
                                    oddsinsert = []
                                    oddsinsertx = None
                                    oddslist = []
                                    initialoddsinsert = None
                                    add_odds = None
                                    oddsinsert.append("('"+game[0]+"', '"+str(game[1])+"', '"+str(game[2])+"', "+str(game[3])+", "+str(game[4])+", "+str(game[5])+", "+str(game[6])+", "+str(game[7])+", "+str(game[8])+", "+str(game[9])+", "+str(game[10])+", "+str(game[11])+")")
                                    oddsinsertx = ','.join(oddsinsert)
                                    oddslist = ['INSERT INTO oddsdata VALUES', oddsinsertx, ';']
                                    initialoddsinsert = ' '.join(oddslist)  
                                    add_odds = initialoddsinsert  
#                                    print(add_odds)
                                    cursor.execute('SET foreign_key_checks = 0;')
                                    cursor.execute(add_odds)
                                    cnx.commit()
                                    cursor.execute('SET foreign_key_checks = 1;')
                        except IntegrityError:
                            pass
                else:
                    error = (team1namelist[each][4:], team2namelist[each][4:])
                    nonfbsteams.append(error)

            else:
                all_errors.append(url)  
cursor.close()
cnx.close() 