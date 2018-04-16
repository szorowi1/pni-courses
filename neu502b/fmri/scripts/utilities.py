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