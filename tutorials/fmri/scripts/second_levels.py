import numpy as np
from scipy.sparse import coo_matrix

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### I/O functions.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def load_sparse_coo(filename):
    npz = np.load(filename)
    M,N = npz['shape']
    return coo_matrix( (npz['data'], (npz['row'],npz['col'])), (M,N) )

def prepare_image(arr, space):
    npz = np.load('first_levels/%s_connectivity.npz' %space)
    image = np.zeros_like(npz['mapping'], dtype=float)
    
    if not space == 'mni305': 
        image[npz['vertices']] += arr
    else:
        x,y,z = npz['vertices'].T
        image[x,y,z] += arr
    
    for _ in range(4 - len(image.shape)): image = np.expand_dims(image,-1)
    return image

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Permutation functions.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def choice(arr):
    return np.random.choice(arr, arr.size, replace=False)

def shuffle_within_rows(X):
    return np.apply_along_axis(choice, 1, X)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Statistics functions.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def anova1rm(data):
    '''Assumes [JxK] matrix, where 
    J = number of subjects
    K = number of variables'''
    J, K = data.shape
    grand_mean = data.mean()

    ## Compute SS_between.
    f = lambda arr: len(arr) * (arr.mean() - grand_mean) ** 2
    SS_b = np.apply_along_axis(f, 0, data).sum()

    ## Compute SS_within.
    f = lambda arr: (arr - arr.mean())**2
    SS_w = np.apply_along_axis(f, 0, data).sum()

    ## Compute SS_subjects.
    SS_subj = K * np.power(data.mean(axis=1) - grand_mean,2).sum()

    ## Compute SS_error.
    SS_err = SS_w - SS_subj

    ## Compute MS_between, MS_error.
    df_b = (K - 1)
    MS_b = SS_b / df_b

    df_err = (J-1)*(K-1)
    MS_err = SS_err / df_err

    ## Compute F.
    F = MS_b / MS_err
    return F