#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 18:03:40 2017

@author: eric.hensleyibm.com
"""
def allowed_clust(n_feats, n_clusts, scale):
    import singlegamestats
    import pandas as pd
    from scipy.cluster.hierarchy import linkage, fcluster
    from sklearn.decomposition import PCA
    data = singlegamestats.pull_pointsallowed()
    fulldata = data.dropna(how='any')
    for gamestat in ['defensive-rebounds-per-game','extra-chances-per-game','offensive-rebounds-per-game','blocks-per-game']:
        fulldata[gamestat[:-4] + 'poss'] = fulldata[gamestat]/fulldata['possessions-per-game']
    scoreresults = fulldata['allowed']
    del fulldata['allowed'] 
    del fulldata['points-from-2-pointers']
    del fulldata['points-from-3-pointers']
    del fulldata['three-pointers-made-per-game']
    del fulldata['defensive-efficiency']
    del fulldata['offensive-efficiency']
    del fulldata['possessions-per-game']
    indices = ['defensive-rebounds-per-poss',
 'defensive-rebounds-per-game',
 'personal-fouls-per-game',
 'steals-perpossession',
 'steal-pct',
 'personal-fouls-per-possession',
 'steals-per-game',
 'block-pct',
 'extra-chances-per-poss',
 'blocks-per-poss',
 'extra-chances-per-game',
 'personal-foul-pct',
 'defensive-rebounding-pct',
 'floor-percentage',
 'turnover-pct',
 'effective-possession-ratio',
 'turnovers-per-possession',
 'blocks-per-game',
 'assists-per-fgm',
 'true-shooting-percentage',
 'effective-field-goal-pct',
 'percent-of-points-from-3-pointers',
 'shooting-pct',
 'percent-of-points-from-free-throws',
 'turnovers-per-game',
 'percent-of-points-from-2-pointers',
 'assist--per--turnover-ratio',
 'offensive-rebounding-pct',
 'fta-per-fga',
 'three-point-rate',
 'two-point-rate',
 'assists-per-game',
 'offensive-rebounds-per-game',
 'free-throw-rate',
 'ftm-per-100-possessions',
 'assists-per-possession',
 'offensive-rebounds-per-poss']

    X = fulldata[indices[:n_feats]]
    Z = linkage(X.T, 'ward')
    clusts = None
    clusts=fcluster(Z, n_clusts, criterion='maxclust')
    pcadf = pd.DataFrame()
    for j in set(clusts):
        varclust = None
        varclust = ([(list(X)[v] if clusts[v] == j else None) for v in range(0, len(clusts))])
        varclust = [x for x in varclust if x != None]
#        print(varclust)
        pcadf[j] = PCA(n_components = 1, random_state = 1108).fit_transform(scale.fit_transform(X[varclust])).flatten()
    return pcadf, scoreresults


def allowed_clust_wteam(n_feats, n_clusts, scale):
    import singlegamestats
    import pandas as pd
    from scipy.cluster.hierarchy import linkage, fcluster
    from sklearn.decomposition import PCA
    data = singlegamestats.pull_pointsallowed_wteam()
    fulldata = data.dropna(how='any')
    for gamestat in ['defensive-rebounds-per-game','extra-chances-per-game','offensive-rebounds-per-game','blocks-per-game']:
        fulldata[gamestat[:-4] + 'poss'] = fulldata[gamestat]/fulldata['possessions-per-game']
    scoreresults = fulldata['allowed']
    del fulldata['allowed'] 
    del fulldata['points-from-2-pointers']
    del fulldata['points-from-3-pointers']
    del fulldata['three-pointers-made-per-game']
    del fulldata['defensive-efficiency']
    del fulldata['offensive-efficiency']
    del fulldata['possessions-per-game']
    indices = ['defensive-rebounds-per-poss',
 'defensive-rebounds-per-game',
 'personal-fouls-per-game',
 'steals-perpossession',
 'steal-pct',
 'personal-fouls-per-possession',
 'steals-per-game',
 'block-pct',
 'extra-chances-per-poss',
 'blocks-per-poss',
 'extra-chances-per-game',
 'personal-foul-pct',
 'defensive-rebounding-pct',
 'floor-percentage',
 'turnover-pct',
 'effective-possession-ratio',
 'turnovers-per-possession',
 'blocks-per-game',
 'assists-per-fgm',
 'true-shooting-percentage',
 'effective-field-goal-pct',
 'percent-of-points-from-3-pointers',
 'shooting-pct',
 'percent-of-points-from-free-throws',
 'turnovers-per-game',
 'percent-of-points-from-2-pointers',
 'assist--per--turnover-ratio',
 'offensive-rebounding-pct',
 'fta-per-fga',
 'three-point-rate',
 'two-point-rate',
 'assists-per-game',
 'offensive-rebounds-per-game',
 'free-throw-rate',
 'ftm-per-100-possessions',
 'assists-per-possession',
 'offensive-rebounds-per-poss']

    X = fulldata[indices[:n_feats]]
    Z = linkage(X.T, 'ward')
    clusts = None
    clusts=fcluster(Z, n_clusts, criterion='maxclust')
    pcadf = pd.DataFrame()
    for j in set(clusts):
        varclust = None
        varclust = ([(list(X)[v] if clusts[v] == j else None) for v in range(0, len(clusts))])
        varclust = [x for x in varclust if x != None]
        print(varclust)
        pcadf[j] = PCA(n_components = 1, random_state = 1108).fit_transform(scale.fit_transform(X[varclust])).flatten()
    iddf = fulldata[['team', 'date']]
    return pcadf, scoreresults, iddf

def scored_clust(n_feats, n_clusts, scale):
    import singlegamestats
    import pandas as pd
    from scipy.cluster.hierarchy import linkage, fcluster
    from sklearn.decomposition import PCA
    data = singlegamestats.pull_reg()
    fulldata = data.dropna(how='any')
    for gamestat in ['defensive-rebounds-per-game','extra-chances-per-game','offensive-rebounds-per-game','blocks-per-game']:
        fulldata[gamestat[:-4] + 'poss'] = fulldata[gamestat]/fulldata['possessions-per-game']
    scoreresults = fulldata['points']
    del fulldata['points'] 
    del fulldata['points-from-2-pointers']
    del fulldata['points-from-3-pointers']
    del fulldata['three-pointers-made-per-game']
    del fulldata['defensive-efficiency']
    del fulldata['offensive-efficiency']
    del fulldata['possessions-per-game']
    indices = ['floor-percentage',
     'true-shooting-percentage',
     'effective-field-goal-pct',
     'shooting-pct',
     'assists-per-game',
     'personal-fouls-per-game',
     'defensive-rebounds-per-game',
     'assists-per-possession',
     'defensive-rebounds-per-poss',
     'personal-fouls-per-possession',
     'offensive-rebounds-per-game',
     'turnovers-per-game',
     'turnover-pct',
     'turnovers-per-possession',
     'percent-of-points-from-3-pointers',
     'assists-per-fgm',
     'effective-possession-ratio',
     'offensive-rebounds-per-poss',
     'ftm-per-100-possessions',
     'personal-foul-pct',
     'percent-of-points-from-2-pointers',
     'extra-chances-per-game',
     'assist--per--turnover-ratio',
     'offensive-rebounding-pct',
     'free-throw-rate',
     'steals-per-game',
     'extra-chances-per-poss',
     'two-point-rate',
     'three-point-rate',
     'fta-per-fga',
     'percent-of-points-from-free-throws',
     'defensive-rebounding-pct',
     'steals-perpossession',
     'steal-pct',
     'blocks-per-poss',
     'blocks-per-game',
     'block-pct']
    
    X = fulldata[indices[:n_feats]]
    Z = linkage(X.T, 'ward')
    clusts = None
    clusts=fcluster(Z, n_clusts, criterion='maxclust')
    pcadf = pd.DataFrame()
    for j in set(clusts):
        varclust = None
        varclust = ([(list(X)[v] if clusts[v] == j else None) for v in range(0, len(clusts))])
        varclust = [x for x in varclust if x != None]
#        print(varclust)
        pcadf[j] = PCA(n_components = 1, random_state = 1108).fit_transform(scale.fit_transform(X[varclust])).flatten()
    return pcadf, scoreresults


def scored_clust_wteam(n_feats, n_clusts, scale):
    import singlegamestats
    import pandas as pd
    from scipy.cluster.hierarchy import linkage, fcluster
    from sklearn.decomposition import PCA
    data = singlegamestats.pull_reg_wteam()
    fulldata = data.dropna(how='any')
    for gamestat in ['defensive-rebounds-per-game','extra-chances-per-game','offensive-rebounds-per-game','blocks-per-game']:
        fulldata[gamestat[:-4] + 'poss'] = fulldata[gamestat]/fulldata['possessions-per-game']
    scoreresults = fulldata['points']
    del fulldata['points'] 
    del fulldata['points-from-2-pointers']
    del fulldata['points-from-3-pointers']
    del fulldata['three-pointers-made-per-game']
    del fulldata['defensive-efficiency']
    del fulldata['offensive-efficiency']
    del fulldata['possessions-per-game']
    indices = ['floor-percentage',
     'true-shooting-percentage',
     'effective-field-goal-pct',
     'shooting-pct',
     'assists-per-game',
     'personal-fouls-per-game',
     'defensive-rebounds-per-game',
     'assists-per-possession',
     'defensive-rebounds-per-poss',
     'personal-fouls-per-possession',
     'offensive-rebounds-per-game',
     'turnovers-per-game',
     'turnover-pct',
     'turnovers-per-possession',
     'percent-of-points-from-3-pointers',
     'assists-per-fgm',
     'effective-possession-ratio',
     'offensive-rebounds-per-poss',
     'ftm-per-100-possessions',
     'personal-foul-pct',
     'percent-of-points-from-2-pointers',
     'extra-chances-per-game',
     'assist--per--turnover-ratio',
     'offensive-rebounding-pct',
     'free-throw-rate',
     'steals-per-game',
     'extra-chances-per-poss',
     'two-point-rate',
     'three-point-rate',
     'fta-per-fga',
     'percent-of-points-from-free-throws',
     'defensive-rebounding-pct',
     'steals-perpossession',
     'steal-pct',
     'blocks-per-poss',
     'blocks-per-game',
     'block-pct']
    
    X = fulldata[indices[:n_feats]]
    Z = linkage(X.T, 'ward')
    clusts = None
    clusts=fcluster(Z, n_clusts, criterion='maxclust')
    pcadf = pd.DataFrame()
    for j in set(clusts):
        varclust = None
        varclust = ([(list(X)[v] if clusts[v] == j else None) for v in range(0, len(clusts))])
        varclust = [x for x in varclust if x != None]
        print(varclust)
        pcadf[j] = PCA(n_components = 1, random_state = 1108).fit_transform(scale.fit_transform(X[varclust])).flatten()
    iddf = fulldata[['team', 'date']]
    return pcadf, scoreresults, iddf



def both_clust(scored_feats, scored_clusts, scored_scale, allowed_feats, allowed_clusts, allowed_scale):    
#    from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
#    scored_feats = 9
#    scored_clusts = 4
#    scored_scale = StandardScaler()
#    allowed_feats = 9
#    allowed_clusts = 3
#    allowed_scale = RobustScaler() 
    import singlegamestats
    import pandas as pd
    from scipy.cluster.hierarchy import linkage, fcluster
    from sklearn.decomposition import PCA
    data = singlegamestats.pull()
    del data['line']
    del data['ou']
    fulldata = data.dropna(how='any')
    list(data)
    for gamestat in ['defensive-rebounds-per-game','extra-chances-per-game','offensive-rebounds-per-game','blocks-per-game']:
        fulldata['fav-' + gamestat[:-4] + 'poss'] = fulldata['fav-' + gamestat]/fulldata['fav-possessions-per-game']
        fulldata['dog-' + gamestat[:-4] + 'poss'] = fulldata['dog-' + gamestat]/fulldata['dog-possessions-per-game']
#    allowed_scoreresults = fulldata['favscore']
#    scored_scoreresults = fulldata['dogscore']
    allowed_indices = ['defensive-rebounds-per-poss',
     'defensive-rebounds-per-game',
     'personal-fouls-per-game',
     'steals-perpossession',
     'steal-pct',
     'personal-fouls-per-possession',
     'steals-per-game',
     'block-pct',
     'extra-chances-per-poss',
     'blocks-per-poss',
     'extra-chances-per-game',
     'personal-foul-pct',
     'defensive-rebounding-pct',
     'floor-percentage',
     'turnover-pct',
     'effective-possession-ratio',
     'turnovers-per-possession',
     'blocks-per-game',
     'assists-per-fgm',
     'true-shooting-percentage',
     'effective-field-goal-pct',
     'percent-of-points-from-3-pointers',
     'shooting-pct',
     'percent-of-points-from-free-throws',
     'turnovers-per-game',
     'percent-of-points-from-2-pointers',
     'assist--per--turnover-ratio',
     'offensive-rebounding-pct',
     'fta-per-fga',
     'three-point-rate',
     'two-point-rate',
     'assists-per-game',
     'offensive-rebounds-per-game',
     'free-throw-rate',
     'ftm-per-100-possessions',
     'assists-per-possession',
     'offensive-rebounds-per-poss']
    scored_indices = ['floor-percentage',
     'true-shooting-percentage',
     'effective-field-goal-pct',
     'shooting-pct',
     'assists-per-game',
     'personal-fouls-per-game',
     'defensive-rebounds-per-game',
     'assists-per-possession',
     'defensive-rebounds-per-poss',
     'personal-fouls-per-possession',
     'offensive-rebounds-per-game',
     'turnovers-per-game',
     'turnover-pct',
     'turnovers-per-possession',
     'percent-of-points-from-3-pointers',
     'assists-per-fgm',
     'effective-possession-ratio',
     'offensive-rebounds-per-poss',
     'ftm-per-100-possessions',
     'personal-foul-pct',
     'percent-of-points-from-2-pointers',
     'extra-chances-per-game',
     'assist--per--turnover-ratio',
     'offensive-rebounding-pct',
     'free-throw-rate',
     'steals-per-game',
     'extra-chances-per-poss',
     'two-point-rate',
     'three-point-rate',
     'fta-per-fga',
     'percent-of-points-from-free-throws',
     'defensive-rebounding-pct',
     'steals-perpossession',
     'steal-pct',
     'blocks-per-poss',
     'blocks-per-game',
     'block-pct']
       
    alldata = pd.DataFrame()
    alldata['fav-pts'] = fulldata['favscore']
    alldata['dog-pts'] = fulldata['dogscore']
    for favdog in ['fav-', 'dog-']:
        X = fulldata[[favdog + i for i in allowed_indices][:allowed_feats]]
        Z = linkage(X.T, 'ward')
        clusts = None
        clusts=fcluster(Z, allowed_clusts, criterion='maxclust')
#        pcadf = pd.DataFrame()
        for j in set(clusts):
            varclust = None
            varclust = ([(list(X)[v] if clusts[v] == j else None) for v in range(0, len(clusts))])
            varclust = [x for x in varclust if x != None]
    #        print(varclust)
#            pcadf[j] = PCA(n_components = 1, random_state = 1108).fit_transform(allowed_scale.fit_transform(X[varclust])).flatten()
            alldata[favdog+'allowed'+str(j)] = PCA(n_components = 1, random_state = 1108).fit_transform(allowed_scale.fit_transform(X[varclust])).flatten()

    for favdog in ['fav-', 'dog-']:
        X = fulldata[[favdog + i for i in scored_indices][:scored_feats]]
        Z = linkage(X.T, 'ward')
        clusts = None
        clusts=fcluster(Z, scored_clusts, criterion='maxclust')
#        pcadf = pd.DataFrame()
        for j in set(clusts):
            varclust = None
            varclust = ([(list(X)[v] if clusts[v] == j else None) for v in range(0, len(clusts))])
            varclust = [x for x in varclust if x != None]
    #        print(varclust)
#            pcadf[j] = PCA(n_components = 1, random_state = 1108).fit_transform(scored_scale.fit_transform(X[varclust])).flatten()
            alldata[favdog+'scored'+str(j)] = PCA(n_components = 1, random_state = 1108).fit_transform(scored_scale.fit_transform(X[varclust])).flatten()
    
    alldata=alldata.dropna(how='any')
    return alldata