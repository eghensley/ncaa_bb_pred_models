#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 11:06:24 2017

@author: eric.hensleyibm.com
"""

import mysql.connector  
passcode = 'ibm1234' 
cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
cursor = cnx.cursor()
teamnames = ['Purdue', 'Duke', 'Wichita St', 'Arizona', 'Kansas', 'Xavier', 'Villanova', 'Florida', 
                 'N Carolina', 'Michigan St', 'W Virginia', 'Cincinnati', 'Texas A&M', 'Virginia', 'Miami (FL)', 
                 'Arkansas', 'Minnesota', 'Notre Dame', 'Gonzaga', 'Baylor', 'Texas Tech', 'Texas', 
                 'TX Christian', 'Oregon', 'Seton Hall', 'Oklahoma', 'Alabama', 'USC', 'Kentucky', 'Creighton', 
                 'St Marys', 'Maryland', 'Providence', 'Wisconsin', 'Kansas St', 'Louisville', 'Rhode Island', 
                 'S Methodist', 'Oklahoma St', 'Florida St', 'Nevada', 'S Carolina', 'Missouri', 'VA Tech',
                 'Tennessee', 'Butler', 'Mississippi', 'Utah', 'Temple', 'St Johns', 'Clemson', 'Penn State',
                 'Ohio State', 'Davidson', 'Marquette', 'Michigan', 'Syracuse', 'Auburn', 'Vanderbilt', 'Iowa',
                 'UCLA', 'San Diego St', 'Arizona St', 'Bucknell', 'Georgetown', 'LSU', 'Boston Col', 'Central FL', 
                 'Iowa State', 'Miss State', 'Illinois', 'Vermont', 'LA Lafayette', 'Georgia', 'Northwestern',
                 'Boise State', 'St Bonavent', 'Houston', 'Fla Gulf Cst', 'UNLV', 'VCU', 'Col Charlestn', 
                 'GA Southern', 'BYU', 'Mercer', 'Belmont', 'TX-Arlington', 'Towson', 'Middle Tenn', 'Connecticut',
                 'N Mex State', 'Georgia St', 'Fresno St', 'Valparaiso', 'Old Dominion', 'GA Tech', 'Colorado', 
                 'N Iowa', 'Indiana', 'Loyola-Chi', 'Stanford', 'Wyoming', 'NC State', 'Murray St', 'St Josephs',
                 'LA Tech', 'N Kentucky', 'Wake Forest', 'Rutgers', 'Illinois St', 'Dayton', 'Yale', 'New Mexico',
                 'Jksnville St', 'Oakland', 'Albany', 'South Dakota', 'Missouri St', 'Iona', 'Monmouth', 'Tulsa',
                 'Grand Canyon', 'Furman', 'Nebraska', 'U Mass', 'E Tenn St', 'DePaul', 'Princeton', 'NC-Grnsboro',
                 'U Penn', 'NC-Asheville', 'Toledo', 'Buffalo', 'Kent State', 'Oregon St', 'California', 'San Fransco', 
                 'IPFW', 'Elon', 'La Salle', 'UAB', 'Utah Val St', 'S Dakota St', 'Bradley', 'Harvard', 'Akron',
                 'S Illinois', 'Utah State', 'Washington', 'Tulane', 'W Michigan', 'Troy', 'Saint Louis', 'UC Irvine',
                 'E Michigan', 'Hofstra', 'Weber State', 'N Dakota St', 'NC-Wilmgton', 'Ste F Austin', 'Army', 
                 'Lipscomb', 'Evansville', 'UCSB', 'N Hampshire', 'Memphis', 'Ohio', 'San Diego', 'Liberty', 'Rider',
                 'Northeastrn', 'Montana', 'Ball State', 'LA Monroe', 'Coastal Car', 'Drake', 'Columbia', 'CS Bakersfld',
                 'TX El Paso', 'Central Mich', 'Richmond', 'Geo Mason', 'Indiana St', 'Colgate', 'Wash State',
                 'Idaho', 'Montana St', 'IL-Chicago', 'Pacific', 'Geo Wshgtn', 'Portland St', 'Samford', 'Arkansas St',
                 'Campbell', 'UC Davis', 'Winthrop', 'St Fran (PA)', 'WI-Milwkee', 'Air Force', 'Stony Brook', 'Lamar', 
                 'Maryland BC', 'Canisius', 'Lehigh', 'Lg Beach St', 'Hawaii', 'E Washingtn', 'Santa Clara', 'Radford', 
                 'Navy', 'TN Tech', 'E Kentucky', 'TN Martin', 'Fairfield', 'Pittsburgh', 'Colorado St', 'Marshall', 
                 'Niagara', 'N Illinois', 'Delaware', 'W Kentucky', 'WI-Grn Bay', 'App State', 'Denver', 'Wofford', 
                 'Wright State', 'St Peters', 'E Carolina', 'Texas State', 'Gard-Webb', 'TX Southern', 'Wm & Mary',
                 'IUPUI', 'Seattle', 'TN State', 'F Dickinson', 'Bowling Grn', 'Cleveland St', 'Fordham', 'Charlotte',
                 'S Alabama', 'Holy Cross', 'Loyola Mymt', 'Drexel', 'Cal Poly', 'North Dakota', 'Duquesne', 
                 'Massachusetts Lowell', 'Manhattan', 'Dartmouth', 'Sam Hous St', 'TX A&M-CC', 'Boston U', 'Neb Omaha', 
                 'Loyola-MD', 'TX-San Ant', 'Chattanooga', 'High Point', 'NC Central', 'E Illinois', 'N Colorado',
                 'Incarnate Word', 'SC Upstate', 'James Mad', 'Siena', 'American', 'W Illinois', 'S Mississippi',
                 'TX-Pan Am', 'Abilene Christian', 'Miami (OH)', 'Portland', 'UC Riverside', 'Austin Peay', 'Brown',
                 'LIU-Brooklyn', 'CS Fullerton', 'Binghamton', 'Rice', 'Mt St Marys', 'Cornell', 'UMKC', 'SE Missouri', 
                 'Morehead St', 'Detroit', 'New Orleans', 'Rob Morris', 'Fla Atlantic', 'Charl South', 'Hampton', 'NC A&T', 
                 'Central Ark', 'Youngs St', 'N Florida', 'Wagner', 'Houston Bap', 'SE Louisiana', 'Cal St Nrdge',
                 'Quinnipiac', 'S Florida', 'Central Conn', 'NJIT', 'Oral Roberts', 'Sac State', 'Sacred Hrt', 'San Jose St', 
                 'Kennesaw St', 'Bryant', 'North Texas', 'St Fran (NY)', 'AR Lit Rock', 'Nicholls St', 'SIU Edward', 
                 'Jackson St', 'Lafayette', 'W Carolina', 'Marist', 'Norfolk St', 'S Utah', 'Pepperdine', 'Jacksonville',
                 'Southern', 'Hartford', 'Stetson', 'McNeese St', 'Prairie View', 'Citadel', 'Morgan St', 'Howard', 
                 'Savannah St', 'Florida Intl', 'N Arizona', 'Idaho State', 'Beth-Cook', 'VA Military', 'Alcorn State', 
                 'Grambling St', 'Maine', 'Ark Pine Bl', 'Florida A&M', 'Longwood', 'S Car State', 'Maryland ES', 'Alab A&M',
                 'Coppin State', 'Delaware St', 'Chicago St', 'NW State', 'Presbyterian', 'Alabama St', 'Miss Val St'] 
baseinsert = []
for each in teamnames:
    baseinsert = []
    baseinsert.append("'"+each+"'")
    baseinsertx = ','.join(baseinsert)
    baselist = ['INSERT INTO teamnames VALUES (', baseinsertx, ');']
    initialbaseinsert = ' '.join(baselist)  
    add_base = initialbaseinsert  
    cursor.execute(add_base)
cnx.commit()
cursor.close()
cnx.close()