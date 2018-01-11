#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 13:57:20 2017

@author: eric.hensleyibm.com
"""


#def update():


import requests
from lxml import html
import re
import pandas as pd
import numpy as np
import unicodedata
import mysql.connector   
import datetime
passcode = 'ibm1234'

cnx = mysql.connector.connect(user='root', password=passcode,
                          host='127.0.0.1',
                          database='ncaa_bb')    
cursor = cnx.cursor()       
teamnames = ['AR Lit Rock', 'Abilene Christian', 'Air Force', 'Akron', 'Alab A&M', 'Alabama', 'Alabama St', 
             'Albany', 'Alcorn State', 'American', 'App State', 'Arizona', 'Arizona St', 'Ark Pine Bl', 
             'Arkansas', 'Arkansas St', 'Army', 'Auburn', 'Austin Peay', 'BYU', 'Ball State', 'Baylor', 
             'Belmont', 'Beth-Cook', 'Binghamton', 'Boise State', 'Boston Col', 'Boston U', 'Bowling Grn',
             'Bradley', 'Brown', 'Bryant', 'Bucknell', 'Buffalo', 'Butler', 'CS Bakersfld', 'CS Fullerton', 
             'Cal Poly', 'Cal St Nrdge', 'California', 'Campbell', 'Canisius', 'Central Ark', 'Central Conn', 
             'Central FL', 'Central Mich', 'Charl South', 'Charlotte', 'Chattanooga', 'Chicago St', 'Cincinnati',
             'Citadel', 'Clemson', 'Cleveland St', 'Coastal Car', 'Col Charlestn', 'Colgate', 'Colorado', 
             'Colorado St', 'Columbia', 'Connecticut', 'Coppin State', 'Cornell', 'Creighton', 'Dartmouth', 
             'Davidson', 'Dayton', 'DePaul', 'Delaware', 'Delaware St', 'Denver', 'Detroit', 'Drake', 'Drexel',
             'Duke', 'Duquesne', 'E Carolina', 'E Illinois', 'E Kentucky', 'E Michigan', 'E Tenn St', 'E Washingtn',
             'Elon', 'Evansville', 'F Dickinson', 'Fairfield', 'Fla Atlantic', 'Fla Gulf Cst', 'Florida', 'Florida A&M', 
             'Florida Intl', 'Florida St', 'Fordham', 'Fresno St', 'Furman', 'GA Southern', 'GA Tech', 'Gard-Webb', 
             'Geo Mason', 'Geo Wshgtn', 'Georgetown', 'Georgia', 'Georgia St', 'Gonzaga', 'Grambling St', 'Grand Canyon',
             'Hampton', 'Hartford', 'Harvard', 'Hawaii', 'High Point', 'Hofstra', 'Holy Cross', 'Houston', 'Houston Bap', 
             'Howard', 'IL-Chicago', 'IPFW', 'IUPUI', 'Idaho', 'Idaho State', 'Illinois', 'Illinois St', 'Incarnate Word',
             'Indiana', 'Indiana St', 'Iona', 'Iowa', 'Iowa State', 'Jackson St', 'Jacksonville', 'James Mad',
             'Jksnville St', 'Kansas', 'Kansas St', 'Kennesaw St', 'Kent State', 'Kentucky', 'LA Lafayette', 'LA Monroe', 
             'LA Tech', 'LIU-Brooklyn', 'LSU', 'La Salle', 'Lafayette', 'Lamar', 'Lehigh', 'Lg Beach St', 'Liberty', 
             'Lipscomb', 'Longwood', 'Louisville', 'Loyola Mymt', 'Loyola-Chi', 'Loyola-MD', 'Maine', 'Manhattan', 'Marist',
             'Marquette', 'Marshall', 'Maryland', 'Maryland BC', 'Maryland ES', 'Massachusetts Lowell', 'McNeese St', 
             'Memphis', 'Mercer', 'Miami (FL)', 'Miami (OH)', 'Michigan', 'Michigan St', 'Middle Tenn', 'Minnesota', 
             'Miss State', 'Miss Val St', 'Mississippi', 'Missouri', 'Missouri St', 'Monmouth', 'Montana', 'Montana St', 
             'Morehead St', 'Morgan St', 'Mt St Marys', 'Murray St', 'N Arizona', 'N Carolina', 'N Colorado', 'N Dakota St',
             'N Florida', 'N Hampshire', 'N Illinois', 'N Iowa', 'N Kentucky', 'N Mex State', 'NC A&T', 'NC Central', 
             'NC State', 'NC-Asheville', 'NC-Grnsboro', 'NC-Wilmgton', 'NJIT','NW State', 'Navy', 'Neb Omaha', 'Nebraska', 
             'Nevada', 'New Mexico', 'New Orleans', 'Niagara', 'Nicholls St', 'Norfolk St', 'North Dakota', 'North Texas',
             'Northeastrn', 'Northwestern', 'Notre Dame', 'Oakland', 'Ohio', 'Ohio State', 'Oklahoma', 'Oklahoma St', 
             'Old Dominion', 'Oral Roberts', 'Oregon', 'Oregon St', 'Pacific', 'Penn State', 'Pepperdine', 'Pittsburgh', 
             'Portland', 'Portland St', 'Prairie View', 'Presbyterian', 'Princeton', 'Providence', 'Purdue', 'Quinnipiac',
             'Radford', 'Rhode Island', 'Rice', 'Richmond', 'Rider', 'Rob Morris', 'Rutgers', 'S Alabama', 'S Car State', 
             'S Carolina', 'S Dakota St', 'S Florida', 'S Illinois', 'S Methodist', 'S Mississippi', 'S Utah', 'SC Upstate',
             'SE Louisiana', 'SE Missouri', 'SIU Edward', 'Sac State', 'Sacred Hrt', 'Saint Louis', 'Sam Hous St', 'Samford',
             'San Diego', 'San Diego St', 'San Fransco', 'San Jose St', 'Santa Clara', 'Savannah St', 'Seattle', 'Seton Hall',
             'Siena', 'South Dakota', 'Southern', 'St Bonavent', 'St Fran (NY)', 'St Fran (PA)', 'St Johns', 'St Josephs', 
             'St Marys', 'St Peters', 'Stanford', 'Ste F Austin', 'Stetson', 'Stony Brook', 'Syracuse', 'TN Martin', 'TN State',
             'TN Tech', 'TX A&M-CC', 'TX Christian', 'TX El Paso', 'TX Southern', 'TX-Arlington', 'TX-Pan Am', 'TX-San Ant', 
             'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas State', 'Texas Tech', 'Toledo', 'Towson', 'Troy', 'Tulane', 
             'Tulsa', 'U Mass', 'U Penn', 'UAB', 'UC Davis', 'UC Irvine', 'UC Riverside', 'UCLA', 'UCSB', 'UMKC', 'UNLV', 
             'USC', 'Utah', 'Utah State', 'Utah Val St', 'VA Military', 'VA Tech', 'VCU', 'Valparaiso', 'Vanderbilt', 
             'Vermont', 'Villanova', 'Virginia', 'W Carolina', 'W Illinois', 'W Kentucky', 'W Michigan', 'W Virginia', 
             'WI-Grn Bay', 'WI-Milwkee', 'Wagner', 'Wake Forest', 'Wash State', 'Washington', 'Weber State', 'Wichita St',
             'Winthrop', 'Wisconsin', 'Wm & Mary', 'Wofford', 'Wright State', 'Wyoming', 'Xavier', 'Yale', 'Youngs St']

teamlist = ['Ark Little Rock', 'Abilene Christian', 'Air Force', 'Akron', 'Alabama A&M', 'Alabama', 'Alabama St', 
             'Albany NY', 'Alcorn St', 'American Univ', 'Appalachian St', 'Arizona', 'Arizona St', 'Ark Pine Bluff', 
             'Arkansas', 'Arkansas St', 'Army', 'Auburn', 'Austin Peay', 'BYU', 'Ball St', 'Baylor', 
             'Belmont', 'Bethune-Cookman', 'Binghamton', 'Boise St', 'Boston College', 'Boston Univ', 'Bowling Green',
             'Bradley', 'Brown', 'Bryant', 'Bucknell', 'Buffalo', 'Butler', 'CS Bakersfld', 'CS Fullerton', 
             'Cal Poly SLO', 'CS Northridge', 'California', 'Campbell', 'Canisius', 'Central Ark', 'Central Conn', 
             'UCF', 'C Michigan', 'Charleston So', 'Charlotte', 'Chattanooga', 'Chicago St', 'Cincinnati',
             'Citadel', 'Clemson', 'Cleveland St', 'Coastal Car', 'Col Charleston', 'Colgate', 'Colorado', 
             'Colorado St', 'Columbia', 'Connecticut', 'Coppin St', 'Cornell', 'Creighton', 'Dartmouth', 
             'Davidson', 'Dayton', 'DePaul', 'Delaware', 'Delaware St', 'Denver', 'Detroit', 'Drake', 'Drexel',
             'Duke', 'Duquesne', 'East Carolina', 'E Illinois', 'E Kentucky', 'E Michigan', 'E Tennessee St', 'E Washington',
             'Elon', 'Evansville', 'F Dickinson', 'Fairfield', 'FL Atlantic', 'Fla Gulf Cst', 'Florida', 'Florida A&M', 
             'Florida Intl', 'Florida St', 'Fordham', 'Fresno St', 'Furman', 'Ga Southern', 'Georgia Tech', 'Gardner Webb', 
             'George Mason', 'G Washington', 'Georgetown', 'Georgia', 'Georgia St', 'Gonzaga', 'Grambling', 'Grand Canyon',
             'Hampton', 'Hartford', 'Harvard', 'Hawaii', 'High Point', 'Hofstra', 'Holy Cross', 'Houston', 'Houston Bap', 
             'Howard', 'IL Chicago', 'IUPU Ft Wayne', 'IUPUI', 'Idaho', 'Idaho St', 'Illinois', 'Illinois St', 'Incarnate Word',
             'Indiana', 'Indiana St', 'Iona', 'Iowa', 'Iowa St', 'Jackson St', 'Jacksonville', 'James Madison',
             'Jacksonville St', 'Kansas', 'Kansas St', 'Kennesaw', 'Kent', 'Kentucky', 'LA Lafayette', 'LA Monroe', 
             'Louisiana Tech', 'Long Island', 'LSU', 'La Salle', 'Lafayette', 'Lamar', 'Lehigh', 'Long Beach St', 'Liberty', 
             'Lipscomb', 'Longwood', 'Louisville', 'Loy Marymount', 'Loyola-Chicago', 'Loyola MD', 'Maine', 'Manhattan', 'Marist',
             'Marquette', 'Marshall', 'Maryland', 'MD Baltimore Co', 'MD E Shore', 'Massachusetts Lowell', 'McNeese St', 
             'Memphis', 'Mercer', 'Miami FL', 'Miami OH', 'Michigan', 'Michigan St', 'Middle Tenn St', 'Minnesota', 
             'Mississippi St', 'MS Valley St', 'Mississippi', 'Missouri', 'Missouri St', 'Monmouth NJ', 'Montana', 'Montana St', 
             'Morehead St', 'Morgan St', "Mt St Mary's", 'Murray St', 'N Arizona', 'North Carolina', 'N Colorado', 'N Dakota St',
             'N Florida', 'New Hampshire', 'N Illinois', 'Northern Iowa', 'N Kentucky', 'New Mexico St', 'NC A&T', 'NC Central', 
             'NC State', 'UNC Asheville', 'UNC Greensboro', 'UNC Wilmington', 'NJIT', 'Northwestern LA', 'Navy', 'Neb Omaha', 'Nebraska', 
             'Nevada', 'New Mexico', 'New Orleans', 'Niagara', 'Nicholls St', 'Norfolk St', 'North Dakota', 'North Texas',
             'Northeastern', 'Northwestern', 'Notre Dame', 'Oakland', 'Ohio', 'Ohio St', 'Oklahoma', 'Oklahoma St', 
             'Old Dominion', 'Oral Roberts', 'Oregon', 'Oregon St', 'Pacific', 'Penn St', 'Pepperdine', 'Pittsburgh', 
             'Portland', 'Portland St', 'Prairie View', 'Presbyterian', 'Princeton', 'Providence', 'Purdue', 'Quinnipiac',
             'Radford', 'Rhode Island', 'Rice', 'Richmond', 'Rider', 'Robert Morris', 'Rutgers', 'S Alabama', 'S Carolina St', 
             'South Carolina', 'S Dakota St', 'South Florida', 'S Illinois', 'SMU', 'Southern Miss', 'Southern Utah', 'SC Upstate',
             'SE Louisiana', 'SE Missouri St', 'SIU Edward', 'CS Sacramento', 'Sacred Ht', 'St Louis', 'Sam Houston St', 'Samford',
             'San Diego', 'San Diego St', 'San Francisco', 'San Jose St', 'Santa Clara', 'Savannah St', 'Seattle', 'Seton Hall',
             'Siena', 'South Dakota', 'Southern Univ', 'St Bonaventure', 'St Francis NY', 'St Francis PA', "St John's", "St Joseph's PA", 
              "St Mary's CA", "St Peter's", 'Stanford', 'SF Austin', 'Stetson', 'Stony Brook', 'Syracuse', 'TN Martin', 'Tennessee St',
             'Tennessee Tech', 'TAM C. Christi', 'TCU', 'Texas-El Paso', 'TX Southern', 'TX Arlington', 'TX Pan American', 'TX San Antonio', 
             'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas St', 'Texas Tech', 'Toledo', 'Towson', 'Troy', 'Tulane', 
             'Tulsa', 'Massachusetts', 'Penn', 'UAB', 'UC Davis', 'UC Irvine', 'UC Riverside', 'UCLA', 'Santa Barbara', 'Missouri KC', 'UNLV', 
             'USC', 'Utah', 'Utah St', 'Utah Val St', 'VMI', 'Virginia Tech', 'VA Commonwealth', 'Valparaiso', 'Vanderbilt', 
             'Vermont', 'Villanova', 'Virginia', 'W Carolina', 'W Illinois', 'W Kentucky', 'W Michigan', 'West Virginia', 
             'WI Green Bay', 'WI Milwaukee', 'Wagner', 'Wake Forest', 'Washington St', 'Washington', 'Weber St', 'Wichita St',
             'Winthrop', 'Wisconsin', 'William & Mary', 'Wofford', 'Wright St', 'Wyoming', 'Xavier', 'Yale', 'Youngstown St']    

espnlist = ['Ark Little Rock', 'Abilene Christian', 'Air Force', 'Akron', 'Alabama A&M', 'Alabama', 'Alabama State', 
             'Albany NY', 'Alcorn State', 'American Univ', 'Appalachian State', 'Arizona', 'Arizona State', 'Ark Pine Bluff', 
             'Arkansas', 'Arkansas State', 'Army', 'Auburn', 'Austin Peay', 'BYU', 'Ball State', 'Baylor', 
             'Belmont', 'Bethune-Cookman', 'Binghamton', 'Boise State', 'Boston College', 'Boston Univ', 'Bowling Green',
             'Bradley', 'Brown', 'Bryant', 'Bucknell', 'Buffalo', 'Butler', 'CS Bakersfld', 'CS Fullerton', 
             'Cal Poly SLO', 'CS Northridge', 'California', 'Campbell', 'Canisius', 'Central Ark', 'Central Conn', 
             'UCF', 'C Michigan', 'Charleston So', 'Charlotte', 'Chattanooga', 'Chicago State', 'Cincinnati',
             'Citadel', 'Clemson', 'Cleveland State', 'Coastal Car', 'Col Charleston', 'Colgate', 'Colorado', 
             'Colorado State', 'Columbia', 'Connecticut', 'Coppin State', 'Cornell', 'Creighton', 'Dartmouth', 
             'Davidson', 'Dayton', 'DePaul', 'Delaware', 'Delaware State', 'Denver', 'Detroit', 'Drake', 'Drexel',
             'Duke', 'Duquesne', 'East Carolina', 'E Illinois', 'E Kentucky', 'E Michigan', 'E Tennessee State', 'E Washington',
             'Elon', 'Evansville', 'F Dickinson', 'Fairfield', 'FL Atlantic', 'Fla Gulf Cst', 'Florida', 'Florida A&M', 
             'Florida Intl', 'Florida State', 'Fordham', 'Fresno State', 'Furman', 'Ga Southern', 'Georgia Tech', 'Gardner Webb', 
             'George Mason', 'G Washington', 'Georgetown', 'Georgia', 'Georgia State', 'Gonzaga', 'Grambling', 'Grand Canyon',
             'Hampton', 'Hartford', 'Harvard', 'Hawaii', 'High Point', 'Hofstra', 'Holy Cross', 'Houston', 'Houston Bap', 
             'Howard', 'IL Chicago', 'IUPU Ft Wayne', 'IUPUI', 'Idaho', 'Idaho State', 'Illinois', 'Illinois State', 'Incarnate Word',
             'Indiana', 'Indiana State', 'Iona', 'Iowa', 'Iowa State', 'Jackson State', 'Jacksonville', 'James Madison',
             'Jacksonville State', 'Kansas', 'Kansas State', 'Kennesaw', 'Kent', 'Kentucky', 'LA Lafayette', 'LA Monroe', 
             'Louisiana Tech', 'Long Island', 'LSU', 'La Salle', 'Lafayette', 'Lamar', 'Lehigh', 'Long Beach State', 'Liberty', 
             'Lipscomb', 'Longwood', 'Louisville', 'Loy Marymount', 'Loyola-Chicago', 'Loyola MD', 'Maine', 'Manhattan', 'Marist',
             'Marquette', 'Marshall', 'Maryland', 'MD Baltimore Co', 'MD E Shore', 'Massachusetts Lowell', 'McNeese State', 
             'Memphis', 'Mercer', 'Miami FL', 'Miami OH', 'Michigan', 'Michigan State', 'Middle Tenn State', 'Minnesota', 
             'Mississippi State', 'MS Valley State', 'Mississippi', 'Missouri', 'Missouri State', 'Monmouth NJ', 'Montana', 'Montana State', 
             'Morehead State', 'Morgan State', "Mt St Mary's", 'Murray State', 'N Arizona', 'North Carolina', 'N Colorado', 'N Dakota State',
             'N Florida', 'New Hampshire', 'N Illinois', 'Northern Iowa', 'N Kentucky', 'New Mexico State', 'NC A&T', 'NC Central', 
             'NC State', 'UNC Asheville', 'UNC Greensboro', 'UNC Wilmington', 'NJIT', 'Northwestern LA', 'Navy', 'Neb Omaha', 'Nebraska', 
             'Nevada', 'New Mexico', 'New Orleans', 'Niagara', 'Nicholls State', 'Norfolk State', 'North Dakota', 'North Texas',
             'Northeastern', 'Northwestern', 'Notre Dame', 'Oakland', 'Ohio', 'Ohio State', 'Oklahoma', 'Oklahoma State', 
             'Old Dominion', 'Oral Roberts', 'Oregon', 'Oregon State', 'Pacific', 'Penn State', 'Pepperdine', 'Pittsburgh', 
             'Portland', 'Portland State', 'Prairie View', 'Presbyterian', 'Princeton', 'Providence', 'Purdue', 'Quinnipiac',
             'Radford', 'Rhode Island', 'Rice', 'Richmond', 'Rider', 'Robert Morris', 'Rutgers', 'S Alabama', 'S Carolina State', 
             'South Carolina', 'S Dakota State', 'South Florida', 'S Illinois', 'SMU', 'Southern Miss', 'Southern Utah', 'SC Upstate',
             'SE Louisiana', 'SE Missouri State', 'SIU Edward', 'CS Sacramento', 'Sacred Ht', 'St Louis', 'Sam Houston State', 'Samford',
             'San Diego', 'San Diego State', 'San Francisco', 'San Jose State', 'Santa Clara', 'Savannah State', 'Seattle', 'Seton Hall',
             'Siena', 'South Dakota', 'Southern Univ', 'St Bonaventure', 'St Francis NY', 'St Francis PA', "St John's", "St Joseph's PA", 
              "Saint Mary's", "St Peter's", 'Stanford', 'SF Austin', 'Stetson', 'Stony Brook', 'Syracuse', 'TN Martin', 'Tennessee State',
             'Tennessee Tech', 'TAM C. Christi', 'TCU', 'Texas-El Paso', 'TX Southern', 'TX Arlington', 'TX Pan American', 'TX San Antonio', 
             'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas State', 'Texas Tech', 'Toledo', 'Towson', 'Troy', 'Tulane', 
             'Tulsa', 'Massachusetts', 'Penn', 'UAB', 'UC Davis', 'UC Irvine', 'UC Riverside', 'UCLA', 'Santa Barbara', 'Missouri KC', 'UNLV', 
             'USC', 'Utah', 'Utah State', 'Utah Val State', 'VMI', 'Virginia Tech', 'VA Commonwealth', 'Valparaiso', 'Vanderbilt', 
             'Vermont', 'Villanova', 'Virginia', 'W Carolina', 'W Illinois', 'W Kentucky', 'W Michigan', 'West Virginia', 
             'WI Green Bay', 'WI Milwaukee', 'Wagner', 'Wake Forest', 'Washington State', 'Washington', 'Weber State', 'Wichita State',
             'Winthrop', 'Wisconsin', 'William & Mary', 'Wofford', 'Wright State', 'Wyoming', 'Xavier', 'Yale', 'Youngstown State']    

teamsdict = {}
for i in range(0, len(teamnames)):
    teamsdict[teamlist[i]] = teamnames[i]
espndict = {}
for i in range(0, len(teamnames)):
    espndict[espnlist[i]] = teamnames[i]

#    for year in range(2006, 2017):
for year in [2016]:
    year = str(int(year+1))
    for qwerty in range(0, 20):
            qwerty = 4
            url = None
            pageContent = None
            tree = None
            espndate = None
            polls = None
            polllist = None
            polldict = {'AP Top 25':'ap', 'USA Today Coaches Poll':'us'}
            url = 'http://www.espn.com/mens-college-basketball/rankings/_/week/%s/year/%s/seasontype/2'%(qwerty+1, year)
            pageContent=requests.get(url)
            tree = html.fromstring(pageContent.content)
            monthdict = {'November':'11', 'December':'12', 'January':'01', 'February':'02', 'March':'03', 'April':'04', 'Nov.':'11','Dec.':'12', 'Jan.':'01', 'Feb.':'02','Mar.':'03', 'Apr.':'04'}

            month, day = tree.xpath('//*[@class = "h2"]/text()')[0].split('-')[1].split('(')[1][:-1].split(' ')
            month = monthdict[month]
            if len(day) == 1:
                day = '0'+day
            if month == '11' or month == '12':
                yearx = str(int(year)-1)
            elif month in ['01', '02', '03', '04']:
                yearx = year
            espndate = datetime.date(int(yearx),int(month),int(day))
            
            polls = tree.xpath('//*[@class = "tablehead"]/tr[1]/td/text()') 
            pollgrid = pd.DataFrame()
            i = 0
            for poll in polls:
                polllist = []                    
                while i != len(tree.xpath('//*[@class = "tablehead"]/tr/td/a/text()')) and tree.xpath('//*[@class = "tablehead"]/tr/td/a/text()')[i] not in polllist:
                    polllist.append(tree.xpath('//*[@class = "tablehead"]/tr/td/a/text()')[i])
                    i += 1
                pollgrid[polldict[poll]]=[polllist]    

            url = None
            pageContent = None
            tree = None
            rankingabbrev = None
            headers = None
            rankabbrev = None
            date = None
            month = None
            day = None
            yearx = None
            
            url = 'https://www.masseyratings.com/cb/arch/compare%s-%s.htm'%(year, qwerty)
            pageContent=requests.get(url)
            
            tree = html.fromstring(pageContent.content)
            rankingabbrev = tree.xpath('//html/body/pre/font/text()')[0].split(' ')
            headers = []
            rankabbrev = []
            
#            month, day, yearx = tree.xpath('//html/body/table/tr/td/h3/text()')[0].split(' ')[1:4]
            month, day, yearx = tree.xpath('//html/body/table/tr/td/table/tr/td/h4/text()')[0].split(' ')[1:4]
            month = monthdict[month]
            day = day[:-1]
            if len(day) == 1:
                day = '0'+day
            masseydate = datetime.date(int(yearx),int(month),int(day))
            
            if (masseydate - espndate).days < 7:
                for each in rankingabbrev:
                    if each.split(',')[0] != '' and each.split(',')[0] != 'Team' and each.split(',')[0] != 'Conf' and each.split(',')[0] != 'Record':
                            headers.append(each.split(',')[0])
                            if each.split(',')[0] != 'Rank':
                                rankabbrev.append(each.split(',')[0])
                
                rawteams = None
                masseyteams = None
                start = None
                endcontent = None
                startcontent = None
                rawratings = None
                ratings = None         
                rawteams = tree.xpath('//html/body/pre/a/text()')[len(rankabbrev):]
                
                errors = []
                masseyteams = []
                for each in rawteams:
                    try:
                        masseyteams.append(teamsdict[each])
                    except KeyError:
                        if each in ['Centenary', 'W Salem St']:
                            masseyteams.append(each)
                        else:
                            errors.append(each)
                            pass

                start = [m.start() for m in re.finditer('Mean Median St.Dev', str(pageContent.content))]
                endcontent = [m.start() for m in re.finditer('----------', str(pageContent.content))]
                startcontent = str(pageContent.content)[start[0]:endcontent[0]]
                rawratings = startcontent.split(' ')
                ratings = []
                for every in rawratings:
                    try:
                        every.split('.')[1]
                    except IndexError:
                        try:
                            ratings.append(int(every))
                        except ValueError:
                            try:
                                ratings.append(int(every.split('<')[0]))
                            except ValueError:
                                try:
                                    ratings.append(int(every.split('>')[1]))
                                except IndexError:
                                    pass
                                except ValueError:
                                    try:
                                        ratings.append(int(every.split('>')[1].split('<')[0]))
                                    except ValueError:
                                        pass
                
                aplist = None
                apcol = None
                uscol = None
                grid = None
                indices = None
                usspotx = None
                apspotx = None
                dataset = None
                                    
                aplist = []
                for team in pollgrid.ap[0]:
                    try:
                        aplist.append(espndict[team])
                    except KeyError:
                        aplist.append(espndict[unicodedata.normalize('NFKD', team).encode('ascii','ignore')])
                uslist = []
                for team in pollgrid.us[0]:
                    try:
                        uslist.append(espndict[team])
                    except KeyError:
                        uslist.append(espndict[unicodedata.normalize('NFKD', team).encode('ascii','ignore')])
                apcol = []
                for team in masseyteams:
                    if team in aplist:
                        apcol.append(aplist.index(team)+1)
                    else:
                        apcol.append(None)
                uscol = []
                for team in masseyteams:
                    if team in uslist:
                        uscol.append(uslist.index(team)+1)
                    else:
                        uscol.append(None)        
                        
                grid = pd.DataFrame(columns = rankabbrev)
                grid['AP'] = np.array(apcol)
                grid['USA'] = np.array(uscol)  
                indices = [i for i, x in enumerate(headers) if x == "Rank"]
                usspotx = headers.index('USA')
                apspotx = headers.index('AP')
                  
                         
                dataset = pd.DataFrame()
                stop = 0
                dbrow = 0
                dataspot = 0
                while stop != 1:
                    line = []
                    hcol = 0
                    end = 0
                    while end != 1: 
                        if hcol == usspotx:
                            if ratings[dataspot] == grid['USA'][dbrow]:
                                line.append(ratings[dataspot])
                                hcol += 1
                                dataspot += 1
                            elif grid['USA'][dbrow] == None:
                                line.append(None)
                                hcol += 1
    
                        elif hcol in indices:
                            if ratings[dataspot] == dbrow+1:
                                    dataspot += 1
                                    hcol += 1
                            else:
                                    end = 1
                                           
                        elif hcol == apspotx:
                            if ratings[dataspot] == grid['AP'][dbrow]:
                                line.append(ratings[dataspot])
                                hcol +=1
                                dataspot += 1
                            elif grid['AP'][dbrow] == None:
                                line.append(None)
                                hcol += 1
                        else:
                            line.append(ratings[dataspot])
                            dataspot += 1
                            hcol += 1                
                        if len(line) == len(list(grid)):
                            end = 1   
                    rowentries = {}
                    for v in range(0, len(list(grid))):
                        rowentries[rankabbrev[v]] = line[v]
                    dataset = dataset.append(rowentries, ignore_index = True)    
                    dbrow += 1
                    if len(grid) == len(dataset):
                        stop = 1
                sqllabels = None            
                sqlstaging = None 
                sqldb = None
                masseylist = None
                masseyinsert = None
                masseyinsertx = None
                add_massey = None
                initialmasseyinsert = None
                if len(masseyteams) == len(dataset):        
                    sqllabels = ['Team', 'PIR', 'OSC', 'UCC', 'KPK', 'COF', 'LAZ', 'RWP', 'ACU', 'PAY', 'JTR', 'MTN', 'RT', 'DII', 'ASH', 'FMG', 'RUD', 'MGS', 'ARG', 'SOR', 'WLK', 'SEL', 'HEN', 'HAT', 'MAS', 'HKB', 'DOL', 'MvG', 'KEE', 'FAS', 'SAG', 'BIH', 'HOW', 'GRS', 'ENG', 'JRT', 'STH', 'PGH', 'RTH', 'HNL', 'KH', 'EZ', 'WOB', 'ABC', 'ISR', 'JNK', 'AND', 'COL', 'BOW', 'YCM', 'PCP', 'SOL', 'WOL', 'EFI', 'BSS', 'KRA', 'WIL', 'LOG', 'BWE', 'BBT', 'RTP', 'RFL', 'WWP', 'KLK', 'REW', 'DUN', 'KEL', 'DP', 'BIL', 'ONV', 'KNT', 'MCK', 'BMC', 'SP', 'LSW', 'GLD', 'WEL', 'BCM', 'MCL', 'LSD', 'MAR', 'DOI', 'DOK', 'TRP', 'VRN', 'INP', 'MJS', 'CSL', 'DEZ', 'RME', 'DWI', 'DES', 'KEN', 'MOR', 'DCI', 'CTW', 'FPI', 'PPP', 'MRK', 'TFG', 'MDS', 'BAS', 'GRR', 'BRN', 'GBE', 'RSL', 'PIG', 'SFX', 'FEI', 'CGV', 'KAM', 'CFP', 'S&P', 'RBA', 'NOL', 'PFZ', 'MGN', 'TPR', 'BDF', 'D1A', 'ATC', 'CMV', 'MVP', 'NUT', 'RTB']
                    sqlstaging = pd.DataFrame(columns = sqllabels)
                    sqlstaging['Team'] = masseyteams
                    
                    num = 0
                    for each in sqllabels:
                        if each in list(dataset):
                            sqlstaging[each] = dataset[each]
                            num += 1
                    sqlstaging.fillna('Null', inplace = True)                    
                    sqldb = np.array(sqlstaging) 
                    print(sqldb)
            
    #            for team in sqldb:
    #                masseyinsert = []
    #                masseyinsert.append("('"+team[0]+"', '"+str(date)+"', "+str(team[1])+', '+str(team[2])+', '+str(team[3])+', '+str(team[4])+', '+str(team[5])+', '+str(team[6])+', '+str(team[7])+', '+str(team[8])+', '+str(team[9])+', '+str(team[10])+', '+str(team[11])+', '+str(team[12])+', '+str(team[13])+', '+str(team[14])+', '+str(team[15])+', '+str(team[16])+', '+str(team[17])+', '+str(team[18])+', '+str(team[19])+', '+str(team[20])+', '+str(team[21])+', '+str(team[22])+', '+str(team[23])+', '+str(team[24])+', '+str(team[25])+', '+str(team[26])+', '+str(team[27])+', '+str(team[28])+', '+str(team[29])+', '+str(team[30])+', '+str(team[31])+', '+str(team[32])+', '+str(team[33])+', '+str(team[34])+', '+str(team[35])+', '+str(team[36])+', '+str(team[37])+', '+str(team[38])+', '+str(team[39])+', '+str(team[40])+', '+str(team[41])+', '+str(team[42])+', '+str(team[43])+', '+str(team[44])+', '+str(team[45])+', '+str(team[46])+', '+str(team[47])+', '+str(team[48])+', '+str(team[49])+', '+str(team[50])+', '+str(team[51])+', '+str(team[52])+', '+str(team[53])+', '+str(team[54])+', '+str(team[55])+', '+str(team[56])+', '+str(team[57])+', '+str(team[58])+', '+str(team[59])+', '+str(team[60])+', '+str(team[61])+', '+str(team[62])+', '+str(team[63])+', '+str(team[64])+', '+str(team[65])+', '+str(team[66])+', '+str(team[67])+', '+str(team[68])+', '+str(team[69])+', '+str(team[70])+', '+str(team[71])+', '+str(team[72])+', '+str(team[73])+', '+str(team[74])+', '+str(team[75])+', '+str(team[76])+', '+str(team[77])+', '+str(team[78])+', '+str(team[79])+', '+str(team[80])+', '+str(team[81])+', '+str(team[82])+', '+str(team[83])+', '+str(team[84])+', '+str(team[85])+', '+str(team[86])+', '+str(team[87])+', '+str(team[88])+', '+str(team[89])+', '+str(team[90])+', '+str(team[91])+', '+str(team[92])+', '+str(team[93])+', '+str(team[94])+', '+str(team[95])+', '+str(team[96])+', '+str(team[97])+', '+str(team[98])+', '+str(team[99])+', '+str(team[100])+', '+str(team[101])+', '+str(team[102])+', '+str(team[103])+', '+str(team[104])+', '+str(team[105])+', '+str(team[106])+', '+str(team[107])+', '+str(team[108])+', '+str(team[109])+', '+str(team[110])+', '+str(team[111])+', '+str(team[112])+', '+str(team[113])+', '+str(team[114])+', '+str(team[115])+', '+str(team[116])+', '+str(team[117])+', '+str(team[118])+', '+str(team[119])+', '+str(team[120])+', '+str(team[121])+', '+str(team[122])+', '+str(team[123])+', '+str(team[124])+")")
    #                masseyinsertx = ','.join(masseyinsert)
    #                masseylist = ['INSERT INTO masseyratings VALUES', masseyinsertx, ';']
    #                initialmasseyinsert = ' '.join(masseylist)  
    #                add_massey = initialmasseyinsert  
    #                cursor.execute('SET foreign_key_checks = 0;')
    #                cursor.execute(add_massey)
    #            cnx.commit()
    #            cursor.execute('SET foreign_key_checks = 1;')
                print(date)
        
    cursor.close()
    cnx.close()     
