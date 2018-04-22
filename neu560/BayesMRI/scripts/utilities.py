import numpy as np
from mne import spatial_tris_connectivity as tris_to_adj
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