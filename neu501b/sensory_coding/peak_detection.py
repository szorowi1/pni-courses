import numpy as np
from scipy.ndimage import measurements

def find_threshold(arr, k):
    return k * np.median( np.abs(arr) ) / 0.6745

def peak_finder(x0, thresh):
    '''Simple peak finding algorithm.'''
    assert x0.ndim == 1
    clusters, ix = measurements.label(x0 > thresh)
    peak_loc = np.concatenate(measurements.maximum_position(x0, labels=clusters, index=np.arange(ix)+1))
    peak_mag = measurements.maximum(x0, labels=clusters, index=np.arange(ix)+1)
    return peak_loc, peak_mag

def peak_censor(times, loc, mag, min_dist=2e-3):

    while True:
        
        ## Compute differences.
        td = np.diff(times[loc])
        
        ## Identify violations.
        violations, = np.where(td < min_dist)   
        if not np.any(violations): break
            
        ## Identify smallest difference.
        i = violations[td[violations].argmin()] 
        
        ## Remove smaller peak.
        if mag[i] > mag[i+1]: 
            loc = np.delete(loc, i+1)
            mag = np.delete(mag, i+1)
        else:
            loc = np.delete(loc, i)
            mag = np.delete(mag, i)
        
    return loc, mag    
