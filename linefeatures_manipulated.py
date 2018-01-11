#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 13:11:21 2017

@author: eric.hensleyibm.com
"""

import singlegamestats
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import numpy as np
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
import pandas as pd
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.cm as cm
from sklearn.svm import SVC
from sklearn.model_selection import cross_validate, StratifiedKFold

data = singlegamestats.pull()

#del data['fav-points-per-game']
#del data['fav-points-from-2-pointers']
#del data['fav-points-from-3-pointers']
#del data['fav-three-pointers-made-per-game']
#del data['fav-blocks-per-game']
#del data['fav-steals-per-game']
#del data['fav-assists-per-game']
#del data['fav-turnovers-per-game']
#del data['fav-extra-chances-per-game']
#del data['fav-offensive-rebounds-per-game']
#del data['fav-defensive-rebounds-per-game']
#del data['dog-points-per-game']
#del data['dog-points-from-2-pointers']
#del data['dog-points-from-3-pointers']
#del data['dog-three-pointers-made-per-game']
#del data['dog-blocks-per-game']
#del data['dog-steals-per-game']
#del data['dog-assists-per-game']
#del data['dog-turnovers-per-game']
#del data['dog-extra-chances-per-game']
#del data['dog-offensive-rebounds-per-game']
#del data['dog-defensive-rebounds-per-game']
#data['fav-possessions-share'] = np.array(data['fav-possessions-per-game'])/np.array(data['dog-possessions-per-game']+data['fav-possessions-per-game'])
#del data['fav-possessions-per-game']
#del data['dog-possessions-per-game']
#data['dog-possessions-share'] = 1-data['fav-possessions-share']

fulldata = data.dropna(how='any')
fulldata = fulldata[(fulldata.favscore + fulldata.line) - fulldata.dogscore != 0]
data = pd.DataFrame()

rawstats = ['-offensive-efficiency',
 '-floor-percentage',
 '-percent-of-points-from-2-pointers',
 '-percent-of-points-from-3-pointers',
 '-percent-of-points-from-free-throws',
 '-defensive-efficiency',
 '-shooting-pct',
 '-fta-per-fga',
 '-ftm-per-100-possessions',
 '-free-throw-rate',
 '-three-point-rate',
 '-two-point-rate',
 '-effective-field-goal-pct',
 '-true-shooting-percentage',
 '-offensive-rebounding-pct',
 '-defensive-rebounding-pct',
 '-block-pct',
 '-steals-perpossession',
 '-steal-pct',
 '-turnovers-per-possession',
 '-assist--per--turnover-ratio',
 '-assists-per-fgm',
 '-assists-per-possession',
 '-turnover-pct',
 '-personal-fouls-per-possession',
 '-personal-foul-pct',
 '-effective-possession-ratio']


for stat in rawstats:
    data['diff'+stat] = (fulldata['fav'+stat] - fulldata['dog'+stat])
    data['share'+stat] = fulldata['fav'+stat]/(fulldata['fav'+stat] + fulldata['dog'+stat])

lineresults = (fulldata.favscore + fulldata.line) - fulldata.dogscore
lineresults=lineresults.apply(lambda x: 1 if x>0 else -1)
#X = fulldata[list(fulldata)[7:]]
X = data.dropna(how='any')
lineresults = lineresults[X.index]

for stat in rawstats:
    X['SSdiff'+stat] = StandardScaler().fit_transform((X['diff'+stat]).values.reshape(-1,1)).flatten()
#    X['RSdiff'+stat] = RobustScaler().fit_transform((X['diff'+stat]).values.reshape(-1,1)).flatten()
#    X['MMdiff'+stat] = MinMaxScaler().fit_transform((X['diff'+stat]).values.reshape(-1,1)).flatten()
    X['SSshare'+stat] = StandardScaler().fit_transform((X['share'+stat]).values.reshape(-1,1)).flatten()
#    X['RSshare'+stat] = RobustScaler().fit_transform((X['share'+stat]).values.reshape(-1,1)).flatten()
#    X['MMshare'+stat] = MinMaxScaler().fit_transform((X['share'+stat]).values.reshape(-1,1)).flatten()
    del X['diff'+stat]
    del X['share'+stat]
Z = linkage(X.T, 'ward')
c, coph_dists = cophenet(Z, pdist(X.T))
print(c)


plt.figure(figsize=(15, 7))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
    labels = list(X)
)
plt.show()


last = Z[-10:, 2]
last_rev = last[::-1]
idxs = np.arange(1, len(last) + 1)
plt.plot(idxs, last_rev)

acceleration = np.diff(last, 2)  # 2nd derivative of the distances
acceleration_rev = acceleration[::-1]
plt.plot(idxs[:-2] + 1, acceleration_rev)
plt.show()

for i in range(2, 10):
    clusts = None
    clusts=fcluster(Z, i, criterion='maxclust')
    pcadf = pd.DataFrame()
    for j in set(clusts):
        varclust = None
        varclust = ([(list(X)[v] if clusts[v] == j else None) for v in range(0, len(clusts))])
        varclust = [x for x in varclust if x != None]
        pcadf[j] = PCA(n_components = 1, random_state = 1108).fit_transform(StandardScaler().fit_transform(X[varclust])).flatten()
        
        
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    fig.set_size_inches(18, 7)
    ax1.set_xlim([-0.1, 1])
    ax1.set_ylim([0, len(X.T) + (i + 1) * 10])
    cluster_labels = clusts
    
    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    silhouette_avg = silhouette_score(X.T, cluster_labels)
    print("For n_clusters =", i,
          "The average silhouette_score is :", silhouette_avg)
    
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
    
        color = cm.spectral(float(seti) / i)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)
    
        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(seti))
    
        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples
    
    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")
    
    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    
    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
    
    # 2nd Plot showing the classification of 2D projection
    if i > 2:
        pca_2D = PCA(n_components = 2, random_state = 1108).fit_transform(StandardScaler().fit_transform(pcadf))
    else:
        pca_2D = np.array(pcadf)
    
    x_min, x_max = pca_2D[:, 0].min() - 1, pca_2D[:, 0].max() + 1
    y_min, y_max = pca_2D[:, 1].min() - 1, pca_2D[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                     np.arange(y_min, y_max, 0.1))
    clf2d = SVC(kernel='rbf')
    clf2d.fit(pca_2D, lineresults)
    preds2D = clf2d.predict(np.c_[xx.ravel(), yy.ravel()])
    preds2D = preds2D.reshape(xx.shape)

    ax2.contourf(xx, yy, preds2D, alpha=0.4)
    ax2.scatter(pca_2D[:, 0][::50], pca_2D[:, 1][::50], c=lineresults[::50],
                                  s=20, edgecolor='k')
    ax2.set_title("The visualization of the clustered data.")
    ax2.set_xlabel("Feature space for the 1st feature")
    ax2.set_ylabel("Feature space for the 2nd feature")    
    cvscores = cross_validate(SVC(kernel='rbf'), pcadf, lineresults, scoring =('f1', 'accuracy', 'roc_auc'), cv = StratifiedKFold(n_splits = 10, random_state = 86))

    ax3.set_title("Classification Report")
    ax3.bar(range(0,4), [np.mean(cvscores['test_accuracy']), np.mean(cvscores['test_roc_auc']), np.mean(cvscores['test_f1']), silhouette_avg],
           color='rbygc',  align="center")
    ax3.set_ylabel('Score')
    ax3.set_xlabel('Metric')
    ax3.set_xticks(np.arange(len(['Accuracy', 'Roc/Auc', 'F1', 'Silhouette'])), ['Accuracy', 'Roc/Auc', 'F1', 'Silhouette'])
    ax3.set_ylim([.3,.9])

    plt.suptitle(("Silhouette analysis for feature clustering on sample data "
                  "with n_clusters = %d, average performance score of %f, and silhouette of %f" % (i, np.mean([np.mean(cvscores['test_accuracy']), np.mean(cvscores['test_roc_auc']), np.mean(cvscores['test_f1'])]), silhouette_avg)),
                 fontsize=14, fontweight='bold')
    plt.show()    
        
#useclust=fcluster(Z, 4, criterion='maxclust')
#for j in set(useclust):
#    thisclust = ([(list(X)[v] if useclust[v] == j else None) for v in range(0, len(useclust))])
#    thisclust = [x for x in thisclust if x != None]
#    print(thisclust)
        
