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
from sklearn.ensemble import ExtraTreesClassifier

data = singlegamestats.pull()

del data['fav-points-per-game']
del data['fav-points-from-2-pointers']
del data['fav-points-from-3-pointers']
del data['fav-three-pointers-made-per-game']
del data['dog-points-per-game']
del data['dog-points-from-2-pointers']
del data['dog-points-from-3-pointers']
del data['dog-three-pointers-made-per-game']

fulldata = data.dropna(how='any')
fulldata = fulldata[(fulldata.favscore + fulldata.line) - fulldata.dogscore != 0]
lineresults = (fulldata.favscore + fulldata.line) - fulldata.dogscore
lineresults=lineresults.apply(lambda x: 1 if x>0 else -1)
X = fulldata[list(fulldata)[7:]]

forest = ExtraTreesClassifier(n_estimators=500,
                              random_state=86)
forest.fit(X, lineresults)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indicesnum = np.argsort(importances)[::-1]
indices = [list(fulldata)[7:][i] for i in indicesnum]
#clist = []
#clist.append(0)
#for i in range(2, len(indices)+1):
#    Z = linkage(X[indices[:i]].T, 'ward')
#    c, coph_dists = cophenet(Z, pdist(X[indices[:i]].T))
#    clist.append(c)
#    
## Print the feature ranking
#print("Feature ranking:")
#
#for f in range(X.shape[1]):
#    print("%d. feature %d (%f)" % (f + 1, indicesnum[f], importances[indicesnum[f]]))
#
## Plot the feature importances of the forest
#fig, ax1 = plt.subplots()
#ax1.bar(range(X[indices].shape[1]), importances[indicesnum],
#       color="r", yerr=std[indicesnum], align="center")
#ax2 = ax1.twinx()
#ax2.plot(clist)
#fig.tight_layout()
#plt.show()
##
#clist.index(max(clist[40:45]))
#
#for i in [4, 6, 8, 11, 14, 21, 44, 64, -1]:
#    Z = linkage(X[indices[:i]].T, 'ward')
#    c, coph_dists = cophenet(Z, pdist(X[indices[:i]].T))
#    print(c)    
#    last = Z[-10:, 2]
#    last_rev = last[::-1]
#    idxs = np.arange(1, len(last) + 1)
#    plt.plot(idxs, last_rev)
#    
#    acceleration = np.diff(last, 2)  # 2nd derivative of the distances
#    acceleration_rev = acceleration[::-1]
#    plt.plot(idxs[:-2] + 1, acceleration_rev)
#    plt.show()
#
#Z = linkage(X.T, 'ward')
#c, coph_dists = cophenet(Z, pdist(X.T))
#print(c)
## .760420393083, .8/.82
## .792615540271
#
#plt.figure(figsize=(15, 7))
#plt.title('Hierarchical Clustering Dendrogram')
#plt.xlabel('sample index')
#plt.ylabel('distance')
#dendrogram(
#    Z,
#    leaf_rotation=90.,  # rotates the x axis labels
#    leaf_font_size=8.,  # font size for the x axis labels
#    labels = list(X)
#)
#plt.show()
#
#
#last = Z[-10:, 2]
#last_rev = last[::-1]
#idxs = np.arange(1, len(last) + 1)
#plt.plot(idxs, last_rev)
#
#acceleration = np.diff(last, 2)  # 2nd derivative of the distances
#acceleration_rev = acceleration[::-1]
#plt.plot(idxs[:-2] + 1, acceleration_rev)
#plt.show()



acclist = []
f1list = []
rocauclist = []
sillist = []
loopX = fulldata[list(fulldata)[7:]]
for i in range(2, 6):
    for k in [4, 6, 8, 11, 14, 21, 44, 64, -1]:
        X = loopX[indices[:k]]
        Z = linkage(X.T, 'ward')
        clusts = None
        clusts=fcluster(Z, i, criterion='maxclust')
        pcadf = pd.DataFrame()
        for j in set(clusts):
            varclust = None
            varclust = ([(list(X)[v] if clusts[v] == j else None) for v in range(0, len(clusts))])
            varclust = [x for x in varclust if x != None]
            pcadf[j] = PCA(n_components = 1, random_state = 1108).fit_transform(MinMaxScaler().fit_transform(X[varclust])).flatten()
        sillist.append(silhouette_score(X.T, clusts))
        cvscores = cross_validate(SVC(kernel='rbf'), pcadf, lineresults, scoring =('f1', 'accuracy', 'roc_auc'), cv = StratifiedKFold(n_splits = 10, random_state = 86))
        acclist.append(np.mean(cvscores['test_accuracy']))
        f1list.append(np.mean(cvscores['test_f1']))
        rocauclist.append(np.mean(cvscores['test_roc_auc']))
combination = [np.mean([acclist[i], f1list[i], rocauclist[i]]) for i in range(0, len(acclist))]
clustsizes = range(2, 6)
numfeats = [4, 6, 8, 11, 14, 21, 44, 64, -1]
combination = np.reshape(combination, (len(clustsizes), -1))
sillist = np.reshape(sillist, (len(clustsizes), -1))
comb_offsets = [0 + 2*i for i in range(0, len(acclist))]
sil_offsets = [1 + 2*i for i in range(0, len(acclist))]
comb_offsets = np.reshape(comb_offsets, (len(clustsizes), -1))
sil_offsets = np.reshape(sil_offsets, (len(clustsizes), -1))
accurlist = np.reshape(acclist, (len(clustsizes), -1))
combi = [np.mean([acclist[i], f1list[i]]) for i in range(0, len(acclist))]
combi = np.reshape(combi, (len(clustsizes), -1))

plt.figure()
COLORS = 'bgrcmyk'
for i, (label, comb, combin, sil, acc, coff, soff) in enumerate(zip(clustsizes, combination, combi, sillist, accurlist, comb_offsets, sil_offsets)):
#    plt.bar(coff, comb, label=label, color=COLORS[i])
#    plt.bar(soff, sil, label=label, color=COLORS[i])
#    plt.bar(soff, acc, label=label, color=COLORS[i])
    plt.bar(soff, combin, label=label, color=COLORS[i])

    
plt.title("Comparing feature reduction techniques")
plt.xlabel('Reduced number of features')
#plt.xticks(bar_offsets + len(reducer_labels) / 2, N_FEATURES_OPTIONS)
plt.ylim((0, 1))
#plt.legend(loc='upper left')

acclist.index(max(acclist))

Z = linkage(loopX[indices[:6]].T, 'ward')
c, coph_dists = cophenet(Z, pdist(loopX[indices[:6]].T))
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




for i in range(2, 6):        
        clusts = None
        clusts=fcluster(Z, i, criterion='maxclust')
        pcadf = pd.DataFrame()
        for j in set(clusts):
            varclust = None
            varclust = ([(list(X)[v] if clusts[v] == j else None) for v in range(0, len(clusts))])
            varclust = [x for x in varclust if x != None]
            pcadf[j] = PCA(n_components = 1, random_state = 1108).fit_transform(MinMaxScaler().fit_transform(X[varclust])).flatten()
            
            
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        fig.set_size_inches(10, 5)
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
            pca_2D = PCA(n_components = 2, random_state = 1108).fit_transform(MinMaxScaler().fit_transform(pcadf))
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
        ax3.set_xticks(range(0,4), ['Accuracy', 'Roc/Auc', 'F1', 'Silhouette'])
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
        
