import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage import measurements

# Spike detection and preprocessing
#   Quian-Quiroga et al. (2004): Unsupervised Spike Detection and Sorting with Wavelets and Superparamagnetic Clustering
#   Gonzalo-Rey et al. (2015): Past, present and future of spike sorting techniques
#   https://dragly.org/2013/03/25/working-with-percolation-clusters-in-python.html

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
    if not ix: return np.array([]), np.array([])
    peak_loc = np.concatenate(measurements.maximum_position(arr, labels=clusters, index=np.arange(ix)+1))
    peak_mag = measurements.maximum(arr, labels=clusters, index=np.arange(ix)+1)
    return peak_loc, peak_mag