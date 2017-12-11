import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from scipy.ndimage import measurements
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
#
# The functions below are used in the spike sorting pipeline 
# for the crayfish experiments as part of the 501b independent
# project. Virtually all of these functions draw from external 
# references in some way or another. The most useful references
# were:
#
# Spike detection and preprocessing
#   Quian-Quiroga et al. (2004): Unsupervised Spike Detection and Sorting with Wavelets and Superparamagnetic Clustering
#   Gonzalo-Rey et al. (2015): Past, present and future of spike sorting techniques
#   https://dragly.org/2013/03/25/working-with-percolation-clusters-in-python.html
#
# Gap statistic
#   Tibshirani et al. (2001): Estimating the number of clusters in a data set via the gap statistic
#   https://datasciencelab.wordpress.com/2013/12/27/finding-the-k-in-k-means-clustering/
#   https://anaconda.org/milesgranger/gap-statistic/notebook

def find_threshold(arr, k):
    '''Empirical determination of amplitude threshold.
    
    Parameters
    ----------
    arr : array, shape=(n_samples,)
      1-d timeseries of extracellular recording.
    k : scalar
      scaling constant. Higher values return more 
      conservative values for threshold.
      
    Returns
    -------
    threshold : scalar
      recommended amplitude threshold.
      
    Notes
    -----
    Typical values of k in range of [3, 5]. See
    Quian-Quiroga et al. (2004) for details.
    '''
    return k * np.median( np.abs(arr) ) / 0.6745

def peak_finder(arr, thresh):
    '''Absolute amplitude-based peak finding algorithm.
    
    Parameters
    ----------
    arr : array, shape=(n_samples,)
      1-d timeseries of extracellular recording.
    thresh : scalar
      amplitude threshold. Only samples above this
      value will be included in clusters.
      
    Returns
    -------
    peak_loc : array
      indices of cluster peaks.
    peak_mag : array
      magnitude of cluster peaks.
    '''
    assert arr.ndim == 1
    clusters, ix = measurements.label(arr > thresh)
    peak_loc = np.concatenate(measurements.maximum_position(arr, labels=clusters, index=np.arange(ix)+1))
    peak_mag = measurements.maximum(arr, labels=clusters, index=np.arange(ix)+1)
    return peak_loc, peak_mag

def gap_statistic(X, n_clusters=10, n_ref=10):
    '''Calculate the gap statistic of a dataset with different
    numbers of clusters, k
    
    Parameters
    ----------
    X : array, shape=(n_samples, n_features)
      dataset for clustering.
    n_clusters : int
      max number of cluster levels to test.
    n_ref : int
      number of reference distributions to generate.
      
    Returns
    -------
    gap : array, shape=(n_clusters,)
      gap statistic at each level of clustering.
      
    Notes
    -----
    Estimates the optimal number of clusters, k, 
    for a dataset, X, using K-means clustering. 
    See Tibshirani et al. (2001) for details.
    '''
    
    ## Normalize data [0, 1].
    X = MinMaxScaler().fit_transform(X)
    
    ## Preallocate space.
    gap = np.zeros(n_clusters)
    
    ## Main loop.
    D = lambda arr: np.linalg.norm(arr - arr.mean(axis=0)) ** 2
    for i in np.arange(n_clusters):
        
        ## Initialize K-means.
        km = KMeans(n_clusters=i+1)
        
        ## Calculate observed dispersion.
        fit = km.fit(X)
        clusters = fit.predict(X)
        Wk = np.sum([ D(X[clusters==c]) / (2 * X[clusters==c].shape[0]) for c in np.unique(clusters) ])
        
        ## Calculate reference dispersion.
        Wkb = np.zeros(n_ref)
        for j in np.arange(n_ref):
            
            ## Generate random sample.
            null = np.random.random_sample(size=X.shape)
            
            ## Calculate null dispersion.
            fit = km.fit(null)
            clusters = fit.predict(null)
            Wkb[j] = np.sum([ D(null[clusters==c]) / (2 * null[clusters==c].shape[0]) for c in np.unique(clusters) ])

        ## Calculate gap statistic.
        gap[i] = np.mean(np.log(Wkb)) - np.log(Wk)
    
    return gap

def seconds_to_timeindex(t,decimals=4):
    '''Junky convenience function for resampling.'''
    m = int(t // 60)
    s = int(np.floor(t % 60))
    ms = np.round(t - m * 60 - s, decimals)
    stringtime = '%0.2d:%0.2d.%s' %(m,s,str(ms)[2:])
    return datetime.strptime(stringtime, '%M:%S.%f')

def timeindex_to_seconds(index, decimals=4):
    '''Junky convenience function for resampling.'''
    m = index.minute * 60
    s = index.second
    ms = index.microsecond * 1e-6
    return np.round(m + s + ms, decimals)

def plot_spikes(times, data, peak_loc, tmin=-5e-4, tmax=5e-4, clusters=False, 
                threshold=False, colors=False, null_color='#34495e', ax=False):

    ## Initialize parameters.
    if not ax: fig, ax = plt.subplots(1,1)
    if not np.any(colors): colors = sns.color_palette(n_colors=np.max(clusters)+1)
    if not np.any(clusters): clusters = np.zeros_like(peak_loc, dtype=int)

    ## Plot data.
    ax.plot(times, data, lw=0.5, color=null_color, alpha=0.4)
    
    ## Plot spikes.
    for loc, cluster in zip(peak_loc, clusters):
        ix = np.logical_and(times >= loc + tmin, times <= loc + tmax)
        ax.plot(times[ix], data[ix], color=colors[cluster])

    ## Plot threshold.
    if threshold: 
        x1, x2 = ax.get_xlim()
        ax.hlines(threshold, x1, x2, color='k', lw=0.5, linestyle='--')
        ax.set_xlim(x1,x2)
        
    return ax