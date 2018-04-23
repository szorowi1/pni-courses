import numpy as np
from collections import OrderedDict
from mne import spatial_tris_connectivity as tris_to_adj
from pystan.misc import _calc_starts
from scipy.sparse import coo_matrix

def adj_to_ugl(A):
    
    ## Extract metadata.
    row, col, data = A.row, A.col, A.data
    
    ## Compute vertex degree.
    D = np.asarray(A.sum(axis=0)).squeeze()
    
    ## Construct new matrix.
    row = np.concatenate([row, np.arange(D.size)])
    col = np.concatenate([col, np.arange(D.size)])
    data = np.concatenate([data * -1, D])
    
    UGL = coo_matrix((data, (row, col)), shape=A.shape)
    return UGL

def assemble_advi_params(samples, params, dims):
    
    ## Calculate dimensions.
    starts = _calc_starts(dims)
    
    ## Avengers, assemble!
    d = OrderedDict()
    for i in range(len(starts) - 1):

        ## Define start and stop.
        start, stop = starts[i], starts[i+1]

        ## Extract samples.
        s = np.array(samples[start:stop])

        ## Reshape.
        s = s.reshape(*dims[i], s.shape[-1], order='F')

        ## Store.
        d[params[i]] = s

    ## Extract final element.
    s = np.array(samples[starts[-1]:-1])

    ## Reshape.
    s = s.reshape(*dims[-1], s.shape[-1], order='F')

    ## Store.
    d[params[-1]] = s
    
    return d