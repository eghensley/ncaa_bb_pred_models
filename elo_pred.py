import math 
import pandas as pd
import mysql.connector 
import numpy as np


def stat_pred(stat, hf, pwr, shrink, adj):
#    stat, hf, pwr, shrink, adj='true-shooting-percentage', 5.03159923, 3.58803079, 69.86241153, 0.13186422
    passcode = 'ibm1234'
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()
    query = "select teamname, (select avg(`%s`) from basestats as bs join gamedata as gd on bs.teamname = gd.teamname and bs.statdate = gd.`date` where gd.teamname = tn.teamname and bs.statdate < '2010-11-01'), (select avg(`%s`) from basestats as bs join gamedata as gd on bs.teamname = gd.teamname and bs.statdate = gd.`date` where gd.opponent = tn.teamname and bs.statdate < '2010-11-01') from teamnames as tn" % (stat, stat)
    cursor.execute(query)
    names = ['name', 'for', 'against']
    pastdata = pd.DataFrame(cursor.fetchall(), columns = names)
    cursor.close()
    cnx.close()
    
    #print(fordict)    
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
            WHERE\
            oddsdate > '2010-11-01'\
            ORDER BY oddsdate ASC" % (stat, stat)
    cursor.execute(query)
    names = ['date', 'fav', 'dog', 'favstat', 'dogstat', 'ha']
    data = pd.DataFrame(cursor.fetchall(), columns = names)
    data=data.dropna(how='any')
    cursor.close()
    cnx.close()
#    record_list = []
    stat_for = {}
    stat_against = {}
    fordict = {}
    for i in range(0, len(pastdata['name'])):
        if math.isnan(pastdata['for'][i]):
            fordict[pastdata['name'][i]] = np.mean(pastdata['for']) - (np.std(pastdata['for']) * 1.5)
        else:
            fordict[pastdata['name'][i]] = pastdata['for'][i]
    againstdict = {}
    for i in range(0, len(pastdata['name'])):
        if math.isnan(pastdata['against'][i]):
            againstdict[pastdata['name'][i]] = np.mean(pastdata['for']) + (np.std(pastdata['for']) * 1.5)
        else:
            againstdict[pastdata['name'][i]] = pastdata['against'][i]
    season = np.array(data['date'])[0].year
    for date, t1, t2, s1, s2, loc in np.array(data):
        if date.month == 11 and date.year > season:
            fordictmean = np.mean(list(fordict.values()))
            againstdictmean = np.mean(list(againstdict.values()))
            for key in fordict.keys():
                fordict[key] = fordict[key] + (fordictmean - fordict[key])*adj
            for key in againstdict.keys():
                againstdict[key] = againstdict[key] + (againstdictmean - againstdict[key])*adj
            season += 1
        if loc == 1:
             loc = -1
        elif loc == 0:
             loc = 1
        stat_for[str(date)+t1+t2] = {'date':date, 'team1':t1, 'team2':t2, 'forstat1':fordict[t1], 'forstat2':fordict[t2]}
        stat_against[str(date)+t1+t2] = {'date':date, 'team1':t1, 'team2':t2, 'againststat1':againstdict[t1], 'againststat2':againstdict[t2]}

        s1_exp = (fordict[t1]+againstdict[t2])/2 + (loc * hf)
        s2_exp = (fordict[t2]+againstdict[t1])/2 - (loc * hf)
        s1_error = (s1 - s1_exp)/s1_exp
        s2_error = (s2 - s2_exp)/s2_exp
        fordict[t1] = fordict[t1] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink
        againstdict[t2] = againstdict[t2] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink
        fordict[t2] = fordict[t2] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink
        againstdict[t1] = againstdict[t1] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink 
#        record = (date, t1, t2, fordict[t1], againstdict[t2])
#        record_list.append(record)
    return stat_for, stat_against
    
    
    
def target_pred(stat, hf, pwr, shrink, adj):
#    stat, hf, pwr, shrink, adj='true-shooting-percentage', 5.03159923, 3.58803079, 69.86241153, 0.13186422
    import singlegamestats 
    pastdata = singlegamestats.pull_targets_train(stat)

    if stat in ['rebounding', 'fouling','foulrate','post', 'guarding','stealing','blocking']:
        fa = 'allow'
    elif stat in ['shooting-efficiency','teamwork','chemistry','true-shooting-percentage']:
        fa = 'score'
    data = singlegamestats.pull_targets_test(stat, fa)
    data=data.dropna(how='any')
#    record_list = []
    stat_for = {}
    stat_against = {}
    fordict = {}
    for i in range(0, len(pastdata['name'])):
        if math.isnan(pastdata['for'][i]):
            fordict[pastdata['name'][i]] = np.mean(pastdata['for']) - (np.std(pastdata['for']) * 1.5)
        else:
            fordict[pastdata['name'][i]] = pastdata['for'][i]
    againstdict = {}
    for i in range(0, len(pastdata['name'])):
        if math.isnan(pastdata['against'][i]):
            againstdict[pastdata['name'][i]] = np.mean(pastdata['for']) + (np.std(pastdata['for']) * 1.5)
        else:
            againstdict[pastdata['name'][i]] = pastdata['against'][i]
    season = np.array(data['date'])[0].year
    for date, t1, t2, s1, s2, loc in np.array(data):
        if date.month == 11 and date.year > season:
            fordictmean = np.mean(list(fordict.values()))
            againstdictmean = np.mean(list(againstdict.values()))
            for key in fordict.keys():
                fordict[key] = fordict[key] + (fordictmean - fordict[key])*adj
            for key in againstdict.keys():
                againstdict[key] = againstdict[key] + (againstdictmean - againstdict[key])*adj
            season += 1
        if loc == 1:
             loc = -1
        elif loc == 0:
             loc = 1
        stat_for[str(date)+t1+t2] = {'date':date, 'team1':t1, 'team2':t2, 'forstat1':fordict[t1], 'forstat2':fordict[t2]}
        stat_against[str(date)+t1+t2] = {'date':date, 'team1':t1, 'team2':t2, 'againststat1':againstdict[t1], 'againststat2':againstdict[t2]}

        s1_exp = (fordict[t1]+againstdict[t2])/2 + (loc * hf)
        s2_exp = (fordict[t2]+againstdict[t1])/2 - (loc * hf)
        s1_error = (s1 - s1_exp)/s1_exp
        s2_error = (s2 - s2_exp)/s2_exp
        fordict[t1] = fordict[t1] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink
        againstdict[t2] = againstdict[t2] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink
        fordict[t2] = fordict[t2] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink
        againstdict[t1] = againstdict[t1] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink 
#        record = (date, t1, t2, fordict[t1], againstdict[t2])
#        record_list.append(record)
    return stat_for, stat_against



    import numpy as np
    import pandas as pd
    import mysql.connector 
    
    teams = ['American', 'Beth-Cook', 'Charl South', 'AR Lit Rock', 'AR Lit Rock', 'Abilene Christian', 'Air Force', 'Akron', 'Alab A&M', 'Alabama', 'Alabama St', 
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
    
    
    #    stat, hf, pwr, shrink, adj='true-shooting-percentage', 5.03159923, 3.58803079, 69.86241153, 0.13186422
    passcode = 'ibm1234'
    cnx = mysql.connector.connect(user='root', password=passcode,
                              host='127.0.0.1',
                              database='ncaa_bb') 
    cursor = cnx.cursor()
    query = "select oddsdate, favorite, underdog, favscore, dogscore, homeaway from oddsdata"
    cursor.execute(query)
    names = ['date', 'fav', 'dog', 'fav-score', 'dog-score', 'ha']
    data = pd.DataFrame(cursor.fetchall(), columns = names)
    cursor.close()
    cnx.close()
    hf, pwr, shrink, adj = 0.43334   ,   2.61208436,  15.72657702,   0.49832657
    fordict = {}
    for team in teams:
        fordict[team] = 0
    againstdict = {}
    for team in teams:
        againstdict[team] = 0
    errors = []
    season = np.array(data['date'])[0].year
    
    score_stats = {}
    allow_stats = {}
    for date, t1, t2, s1, s2, loc in np.array(data):
        if date.month == 11 and date.year > season:
            fordictmean = np.mean(list(fordict.values()))
            againstdictmean = np.mean(list(againstdict.values()))
            for key in fordict.keys():
                fordict[key] = fordict[key] + (fordictmean - fordict[key])*adj
            for key in againstdict.keys():
                againstdict[key] = againstdict[key] + (againstdictmean - againstdict[key])*adj
            season += 1
        if loc == 1:
             loc = -1
        elif loc == 0:
             loc = 1
        if s1 == s1 and s2 == s2:
            if fordict[t1] != 0 and fordict[t2] != 0 and againstdict[t1] != 0 and againstdict[t2] != 0:
                s1_exp = (fordict[t1]+againstdict[t2])/2 + (loc * hf)
                s2_exp = (fordict[t2]+againstdict[t1])/2 - (loc * hf)
                s1_error = (s1 - s1_exp)/s1_exp
                s2_error = (s2 - s2_exp)/s2_exp
                errors.append(s1_error**2 *-1)
                errors.append(s2_error**2 *-1)
                score_stats[str(date)+t1.replace(' ', '_')] = s1
                if fordict[t1] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink != fordict[t1] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink:
                    break
                if againstdict[t2] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink != againstdict[t2] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink:
                    break
                if fordict[t2] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink != fordict[t2] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink:
                    break
                if againstdict[t1] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink != againstdict[t1] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink:
                    break        
                fordict[t1] = fordict[t1] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink
                againstdict[t2] = againstdict[t2] + ((((1 + s1_error)**pwr) -1) * s1_exp)/shrink
                fordict[t2] = fordict[t2] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink
                againstdict[t1] = againstdict[t1] + ((((1 + s2_error)**pwr) -1) * s2_exp)/shrink 
            else:
                if fordict[t1] == 0:
                    fordict[t1] = s1
                if fordict[t2] == 0:
                    fordict[t2] = s2
                if againstdict[t1] == 0:
                    againstdict[t1] = s2
                if againstdict[t2] == 0:
                    againstdict[t1] = s1