import numpy as np
from mne.filter import filter_data
from mne.preprocessing.peak_finder import peak_finder
from scipy.ndimage import measurements

def find_step_events(arr, direction, sfreq, h_freq=5.0, min_duration=0.5, tol=1e-5):
    '''
    Idiosyncratic function designed to detect motion/null events in
    botfly stepwise-motion recordings. Roughly, works by:
        1. Filter: lowpass filters stimulus (drum) recording to smooth input signal.
        2. Delta: compute the difference between sequential timepoints. Periods of 
           no motion should be close to zero.
        3. Clustering: identify contiguous near-zero data points (i.e. no-motion epochs).
           Clusters can be filtered by a specified minimum duration.
        4. Events: identify the start and stop points of clusters. Reorganize info
           as an [Nx3] array of [start, stop, condition], where {stationary = 0, CCW = 1, CW = 2}.
           
   INPUTS
   -- arr: stimulus (drum) signal
   -- direction: CCW or CW
   -- sfreq: sampling frequency
   -- h_freq: lowpass frequency. If set to False, no lowpass applied.
   -- min_duration: minimum length of cluster (in seconds)
   -- tol: non-zero tolerance. Datapoints beneath this value are considered stationary.
    '''
    assert direction == 'CCW' or direction == 'CW'
    
    ## Filter data.
    if h_freq: arr = filter_data(arr, sfreq, l_freq=None, h_freq=h_freq, phase='zero', verbose=False)

    ## Compute differences.
    delta = np.insert( np.diff(arr), 0, 0 )

    ## Identify clusters.
    bool_arr = np.abs(delta) < tol
    clusters, n_cluster = measurements.label(bool_arr)

    ## Filter clusters by duration.
    durations = measurements.sum(bool_arr, labels=clusters, index=np.arange(n_cluster+1)) / sfreq
    for i, duration in enumerate(durations):
        if duration < min_duration: clusters[clusters == i] = 0

    ## Find indices of cluster onsets/offsets. 
    indices = np.unique(clusters)[np.unique(clusters) > 0]
    onsets = [ np.where(clusters == i)[0][0] for i in indices ]
    offsets= [ np.where(clusters == i)[0][-1] for i in indices ]

    ## Re-organize into events. Demarcate null/motion events.
    events = np.sort(np.concatenate([onsets,offsets]))
    events = np.array([events[i:i+2] for i in range(events.size-1)])
    if not events.size: raise ValueError('No events detected. Check paramaters.')
    events = np.concatenate([events, np.arange(events.shape[0]).reshape(-1,1) % 2], axis=-1)
    if direction == 'CW': events[:,-1] *= 2
    
    return events

def find_oscillation_events(arr, direction, sfreq, h_freq=5, thresh=None):
    '''
    Idiosyncratic function designed to detect motion/null events in
    botfly oscillation-motion recordings. Roughly, works by:
        1. Filter: lowpass filters stimulus (drum) recording to smooth input signal.
        2. Peak finding: identify minima and maxima of drum signal.
        3. Events: Reorganize info as an [Nx3] array of [start, stop, condition], 
        where {CCW = 1, CW = 2}
           
   INPUTS
   -- arr: stimulus (drum) signal
   -- direction: CCW or CW
   -- sfreq: sampling frequency
   -- h_freq: lowpass frequency. If set to False, no lowpass applied.
    '''
    assert direction == 'CCW' or direction == 'CW'
    
    ## Filter data.
    if h_freq: arr = filter_data(arr, sfreq, l_freq=None, h_freq=h_freq, phase='zero', verbose=False)

    ## Identify extrema.
    maxima, _ = peak_finder(arr, thresh=thresh, extrema=1)
    minima, _ = peak_finder(arr, thresh=thresh, extrema=-1)

    ## Re-organize into events.
    events = np.sort(np.concatenate([maxima,minima]))
    events = np.array([events[i:i+2] for i in range(events.size-1)])
    if not events.size: raise ValueError('No events detected. Check paramaters.')

    ## Demarcate null/motion events.
    events = np.concatenate([events, np.zeros(events.shape[0], dtype=int).reshape(-1,1)], axis=-1)
    if direction == 'CCW':
        events[np.in1d(events[:,0], maxima), -1] = 1
        events[np.in1d(events[:,0], minima), -1] = 2
    else:
        events[np.in1d(events[:,0], maxima), -1] = 2
        events[np.in1d(events[:,0], minima), -1] = 1
        
    return events

def find_threshold(arr, k):
    return k * np.median( np.abs(arr) ) / 0.6745

def amplitude_thresholding(x0, thresh):
    '''Simple peak finding algorithm.'''
    assert x0.ndim == 1
    clusters, ix = measurements.label(x0 > thresh)
    peak_loc = np.concatenate(measurements.maximum_position(x0, labels=clusters, index=np.arange(ix)+1))
    peak_mag = measurements.maximum(x0, labels=clusters, index=np.arange(ix)+1)
    return peak_loc, peak_mag