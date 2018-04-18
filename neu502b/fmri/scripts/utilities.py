import numpy as np
import nibabel as nib

def read_gifti(f):
    '''Convenience function for reading gifti (gii) files'''
    
    ## Load file.
    obj = nib.load(f)
    
    ## Iteratively extract and return data.
    data = []
    for arr in obj.darrays: data.append(arr.data)
    return np.array(data)

def mask_insert(arr, mask):
    full = np.zeros((arr.shape[0], mask.size))
    full[:,mask] = arr
    return full