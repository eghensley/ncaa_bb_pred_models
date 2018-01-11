#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 11:33:29 2017

@author: eric.hensleyibm.com
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import singlegamestats
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster, cophenet
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, silhouette_samples
from scipy.spatial.distance import pdist
import matplotlib.cm as cm
from sklearn.svm import SVR
from sklearn.model_selection import cross_validate, KFold

scores = pd.DataFrame()
mse = pd.read_csv('mse_scored.csv')
r2 = pd.read_csv('r2_scored.csv')
sil = pd.read_csv('sil_scored.csv')

clustsizes = [2,3,4,5,6,7]
numfeats = [7, 9, 18, 27, -1]
scales = ['Standard', 'Robust', 'MinMax']

c = []
n = []
s = []
for clust in clustsizes:
    for num in numfeats:
        for scale in scales:
            c.append(clust)
            n.append(num)
            s.append(scale)
mse = np.array(mse['0'])
r2 = np.array(r2['0'])
sil = np.array(sil['0'])

scores['mse'] = mse
scores['r2'] = r2
scores['sil'] = sil
scores['clusters'] = np.array(c)
scores['features'] = np.array(n)
scores['scaler'] = np.array(s)

9 = 3,4
18 = 4
27 = 2, 4, 5
7,9,robust
5, 9 robust
4,9 standard
7, 18 robust
2, 27 minmax
3, 27 minmax



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

#for coord in [(4, 18, MinMaxScaler()), (2, 27, MinMaxScaler()), (3, 27, MinMaxScaler())]:
for coord in [(5, 18, MinMaxScaler()), (4, 27, MinMaxScaler()), (6, 27, MinMaxScaler())]:
    cluster, feature, scale = coord
    X = fulldata[indices[:feature]]
    Z = linkage(X.T, 'ward')
    dendscore, coph_dists = cophenet(Z, pdist(X.T))
    last = Z[-10:, 2]
    last_rev = last[::-1]
    idxs = np.arange(1, len(last) + 1)
    clusts = None
    clusts=fcluster(Z, cluster, criterion='maxclust')
    pcadf = pd.DataFrame()
    for j in set(clusts):
        varclust = None
        varclust = ([(list(X)[v] if clusts[v] == j else None) for v in range(0, len(clusts))])
        varclust = [x for x in varclust if x != None]
        pcadf[j] = PCA(n_components = 1, random_state = 1108).fit_transform(scale.fit_transform(X[varclust])).flatten()
    silhouette_score(X.T, clusts)

    plt.figure(figsize=(18, 4))
    plt.title('Hierarchical Clustering Dendrogram, Proposed Clusters = %s, Score = %s' % (cluster, dendscore))
    plt.xlabel('sample index')
    plt.ylabel('ward distance')
    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
        labels = list(X)
    )
    plt.show()
    
    fig, (ax2, ax3, ax1, ax4) = plt.subplots(1, 4)
    fig.set_size_inches(18, 7)

    ax2.plot(idxs, last_rev)
    acceleration = np.diff(last, 2)  # 2nd derivative of the distances
    acceleration_rev = acceleration[::-1]
    ax2.plot(idxs[:-2] + 1, acceleration_rev)
    ax2.set_title('First and Second Derivative Elbow Plot')
    ax2.set_xlabel('Clusters')

    
    ax3.set_xlim([-0.1, 1])
    ax3.set_ylim([0, len(X.T) + (cluster + 1) * 10])
    cluster_labels = clusts
    
    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    silhouette_avg = silhouette_score(X.T, cluster_labels)
    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(X.T, cluster_labels)
    
    y_lower = 10
    for seti in set(clusts):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[cluster_labels == seti]
    
        ith_cluster_silhouette_values.sort()
    
        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i
    
        color = cm.spectral(float(seti) / cluster)
        ax3.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)
    
        # Label the silhouette plots with their cluster numbers at the middle
        ax3.text(-0.05, y_lower + 0.5 * size_cluster_i, str(seti))
    
        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples
    
    ax3.set_title("Silhouette plot. Average = %s" % (silhouette_avg))
    ax3.set_xlabel("The silhouette coefficient values")
    ax3.set_ylabel("Cluster label")
    
    # The vertical line for average silhouette score of all the values
    ax3.axvline(x=silhouette_avg, color="red", linestyle="--")
    
    ax3.set_yticks([])  # Clear the yaxis labels / ticks
    ax3.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    if cluster > 2:
        pca_2D = PCA(n_components = 2, random_state = 1108).fit_transform(scale.fit_transform(pcadf))
    else:
        pca_2D = np.array(pcadf)
    
    x_min, x_max = pca_2D[:, 0].min() - 1, pca_2D[:, 0].max() + 1
    y_min, y_max = pca_2D[:, 1].min() - 1, pca_2D[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                     np.arange(y_min, y_max, 0.1))
    clf2d = SVR(kernel='rbf')
    clf2d.fit(pca_2D, scoreresults)
    preds2D = clf2d.predict(np.c_[xx.ravel(), yy.ravel()])
    preds2D = preds2D.reshape(xx.shape)

    ax1.contourf(xx, yy, preds2D, alpha=0.4)
    ax1.scatter(pca_2D[:, 0][::100], pca_2D[:, 1][::100], c=scoreresults[::100],
                                  s=20, edgecolor='k')
    ax1.set_title("2D visualization of the clustered data.")
    ax1.set_xlabel("Feature space for the 1st feature")
    ax1.set_ylabel("Feature space for the 2nd feature") 

    cvscores = cross_validate(SVR(kernel='rbf'), pcadf, scoreresults, scoring =('neg_mean_absolute_error', 'r2'), cv = KFold(n_splits = 10, random_state = 86), n_jobs = -1)
    ax4.set_title("Cross Validated Performance")
    ax4.bar(range(0,3), [(np.mean(cvscores['test_neg_mean_absolute_error']) * -1)/10, np.mean(cvscores['test_r2']), silhouette_avg],
           color='rbygc',  align="center")
    ax4.set_ylabel('Score')
    ax4.set_xlabel('Metric')
    ax4.set_ylim([.3,.9])

    plt.suptitle(("Analysis for %s clusters of top %s features.  MAE = %s, R2 = %s, Silhouette = %s" % (cluster, feature, np.mean(cvscores['test_neg_mean_absolute_error']), np.mean(cvscores['test_r2']), silhouette_avg)),
                 fontsize=14, fontweight='bold')
    plt.show()    


