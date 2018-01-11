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
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import pandas as pd
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.cm as cm
from sklearn.svm import SVR
from sklearn.model_selection import cross_validate, KFold
from sklearn.utils import resample
from sklearn.ensemble import ExtraTreesRegressor

#data = singlegamestats.pull_margin()
#data = singlegamestats.pull_share()
data = singlegamestats.pull_pointsallowed()
#data = singlegamestats.pull_reg()
fulldata = data.dropna(how='any')
for gamestat in ['defensive-rebounds-per-game','extra-chances-per-game','offensive-rebounds-per-game','blocks-per-game']:
    fulldata[gamestat[:-4] + 'poss'] = fulldata[gamestat]/fulldata['possessions-per-game']

#scoreresults = resample(fulldata['points'], n_samples = int(len(fulldata)/3), random_state = 46)
#scoreresults = resample(fulldata['margin'], n_samples = int(len(fulldata)/3), random_state = 46)
#scoreresults = resample(fulldata['share'], n_samples = int(len(fulldata)/3), random_state = 46)
#scoreresults = resample(fulldata['allowed'], n_samples = int(len(fulldata)/3), random_state = 46)
scoreresults = fulldata['allowed']



del fulldata['allowed'] ### either margin, points, allowed or share!!!!!!!!!!!!!!!
del fulldata['points-from-2-pointers']
del fulldata['points-from-3-pointers']
del fulldata['three-pointers-made-per-game']

del fulldata['defensive-efficiency']
del fulldata['offensive-efficiency']
del fulldata['possessions-per-game']
#X = resample(fulldata[list(fulldata)[7:]], n_samples = int(len(fulldata)/3), random_state = 46)
#X = resample(fulldata, n_samples = int(len(fulldata)/3), random_state = 46)
X = fulldata

#forest = ExtraTreesRegressor(n_estimators=500,
#                              random_state=86)
#forest.fit(X, scoreresults)
#importances = forest.feature_importances_
#std = np.std([tree.feature_importances_ for tree in forest.estimators_],
#             axis=0)
#indicesnum = np.argsort(importances)[::-1]
#indices = [list(fulldata)[i] for i in indicesnum]
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
#clist.index(max(clist[16:]))
#
#
#
#
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

Z = linkage(X[indices[:9]].T, 'ward')
plt.figure(figsize=(15, 7))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
    labels = indices[:9]
)
plt.show()

#
for i in [9, 12]:
    Z = linkage(X[indices[:i]].T, 'ward')
    c, coph_dists = cophenet(Z, pdist(X[indices[:i]].T))
    print(c)    
    last = Z[-10:, 2]
    last_rev = last[::-1]
    idxs = np.arange(1, len(last) + 1)
    plt.plot(idxs, last_rev)
    
    acceleration = np.diff(last, 2)  # 2nd derivative of the distances
    acceleration_rev = acceleration[::-1]
    plt.plot(idxs[:-2] + 1, acceleration_rev)
    plt.show()
#Z = linkage(X.T, 'ward')
#c, coph_dists = cophenet(Z, pdist(X.T))
#print(c)
## .760420393083, .8/.82
## .792615540271


mselist = []
r2list = []
sillist = []
scoreresults = resample(scoreresults, n_samples = int(len(fulldata)/10), random_state = 46)
loopX = resample(fulldata, n_samples = int(len(fulldata)/10), random_state = 46)
clustsizes = range(2, 8)
numfeats = [2, 4, 9, 12, 15, 18, -1]
progress = 0
for i in clustsizes:
    for k in numfeats:
        for scale in [StandardScaler(), RobustScaler(), MinMaxScaler()]:
            progress += 1
            print('%s percent complete' % ((float(progress) / float(len(numfeats) * len(clustsizes) * 3))*100))
            X = loopX[indices[:k]]
            Z = linkage(X.T, 'ward')
            clusts = None
            clusts=fcluster(Z, i, criterion='maxclust')
            pcadf = pd.DataFrame()
            for j in set(clusts):
                varclust = None
                varclust = ([(list(X)[v] if clusts[v] == j else None) for v in range(0, len(clusts))])
                varclust = [x for x in varclust if x != None]
                pcadf[j] = PCA(n_components = 1, random_state = 1108).fit_transform(scale.fit_transform(X[varclust])).flatten()
            try:
                sillist.append(silhouette_score(X.T, clusts))
            except ValueError:
                sillist.append(0)
            cvscores = cross_validate(SVR(kernel='rbf'), pcadf, scoreresults, scoring =('neg_mean_absolute_error', 'r2'), cv = KFold(n_splits = 10, random_state = 86))
            mselist.append(np.mean(cvscores['test_neg_mean_absolute_error']))
            r2list.append(np.mean(cvscores['test_r2']))
            
mselistpd = pd.DataFrame(mselist)
r2listpd = pd.DataFrame(r2list)    
sillistpd = pd.DataFrame(sillist)    
mselistpd.to_csv("mse_allowed.csv")       
r2listpd.to_csv("r2_allowed.csv")       
sillistpd.to_csv("sil_allowed.csv")       
            
            
            
            
combination = [np.mean([acclist[i], f1list[i], rocauclist[i]]) for i in range(0, len(acclist))]
combination = np.reshape(combination, (len(clustsizes), -1))
sillist = np.reshape(sillist, (len(clustsizes), -1))








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






Z = linkage(X.T, 'ward')
c, coph_dists = cophenet(Z, pdist(X.T))
print(c)


# all feats, points
# .791529705044
# 2 clust sil = 0.641513468584, mms mae = -.557664, r2 = .650016
# 5 clust sil = .496467, rbs mae = -.401439, r2 = .821759

# all feats, margin
# .790873301857
# 2 clust sil = .4998232, ss mae = .739024, r2 = .575518

# all feats, share
# .790811367072
# mm 3 and 4

plt.figure(figsize=(25, 10))
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

for scale in [StandardScaler(), RobustScaler(), MinMaxScaler()]:
    for i in range(2, 6):
        clusts = None
        clusts=fcluster(Z, i, criterion='maxclust')
        pcadf = pd.DataFrame()
        for j in set(clusts):
            varclust = None
            varclust = ([(list(X)[v] if clusts[v] == j else None) for v in range(0, len(clusts))])
            varclust = [x for x in varclust if x != None]
            pcadf[j] = PCA(n_components = 1, random_state = 1108).fit_transform(scale.fit_transform(X[varclust])).flatten()
            
            
#        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        fig, (ax1, ax3) = plt.subplots(1, 2)

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
#        if i > 2:
#            pca_2D = PCA(n_components = 2, random_state = 1108).fit_transform(scale.fit_transform(pcadf))
#        else:
#            pca_2D = np.array(pcadf)
#        
#        x_min, x_max = pca_2D[:, 0].min() - 1, pca_2D[:, 0].max() + 1
#        y_min, y_max = pca_2D[:, 1].min() - 1, pca_2D[:, 1].max() + 1
#        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
#                         np.arange(y_min, y_max, 0.1))
#        clf2d = SVR(kernel='rbf')
#        clf2d.fit(pca_2D, scoreresults)
#        preds2D = clf2d.predict(np.c_[xx.ravel(), yy.ravel()])
#        preds2D = preds2D.reshape(xx.shape)
#    
#        ax2.contourf(xx, yy, preds2D, alpha=0.4)
#        ax2.scatter(pca_2D[:, 0][::20], pca_2D[:, 1][::20], c=scoreresults[::20],
#                                      s=20, edgecolor='k')
#        ax2.set_title("The visualization of the clustered data.")
#        ax2.set_xlabel("Feature space for the 1st feature")
#        ax2.set_ylabel("Feature space for the 2nd feature")    
        cvscores = cross_validate(SVR(kernel='rbf'), pcadf, scoreresults, scoring =('neg_mean_absolute_error', 'r2'), cv = KFold(n_splits = 10, random_state = 86), n_jobs = -1)
    
        ax3.set_title("Classification Report")
        ax3.bar(range(0,3), [(np.mean(cvscores['test_neg_mean_absolute_error']) * -1)/10, np.mean(cvscores['test_r2']), silhouette_avg],
               color='rbygc',  align="center")
        ax3.set_ylabel('Score')
        ax3.set_xlabel('Metric')
        ax3.set_ylim([.3,.9])
    
        plt.suptitle(("Silhouette analysis for feature clustering on sample data "
                      "with n_clusters = %d, mae of %f, r2 of %f, and silhouette of %f" % (i, np.mean(cvscores['test_neg_mean_absolute_error'])/10, np.mean(cvscores['test_r2']), silhouette_avg)),
                     fontsize=14, fontweight='bold')
        plt.show()    
        
#useclust=fcluster(Z, 4, criterion='maxclust')
#for j in set(useclust):
#    thisclust = ([(list(X)[v] if useclust[v] == j else None) for v in range(0, len(useclust))])
#    thisclust = [x for x in thisclust if x != None]
#    print(thisclust)
        
