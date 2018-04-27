import numpy as np
from tqdm import tqdm

def permutation_testing(WY, WX, n_task, n_perm=5000):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Precompute matrices.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    ## Preallocate space.
    T, K, V = WX.shape
    WZ = WX[:,n_task:,:]
    ZtZ = np.zeros((K-n_task,K-n_task,V))    # Nuisance projection matrices.
    XtX = np.zeros((K, K, V))                # Design projection matrices

    for i in np.arange(V):

        ## Precompute regressor projection matrix.
        XtX[...,i] = np.linalg.inv(WX[...,i].T @ WX[...,i])
        ZtZ[...,i] = np.linalg.inv(WZ[...,i].T @ WZ[...,i])

    ## Precompute full regressor matices.
    XXX = np.einsum('ijk,ljk->ilk', XtX, WX)
    ZZZ = np.einsum('ijk,ljk->ilk', ZtZ, WZ)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Observed statistics.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    ## Compute regression coefficients.
    B = np.einsum('ijk,jk->ik', XXX, WY)

    ## Compute residual error.
    epsilon = WY - np.einsum('ijk,jk->ik',WX,B)

    ## Compute standard error.
    se = np.zeros_like(B)
    for i in np.arange(V):
        sigma_sq = epsilon[:,i] @ epsilon[:,i] / (T - K)
        se[:,i] = np.sqrt(sigma_sq * np.diag(XtX[...,i]))

    ## Compute test statistic.
    F = B / se

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Permuted statistics.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    ## Preallocate space.
    p = np.ones_like(F)

    ## Compute nuisance-only regression coefficients.
    G = np.einsum('ijk,jk->ik', ZZZ, WY)
    ZG = np.einsum('ijk,jk->ik',WZ,G)

    ## Compute nuisance-only residual error.
    Ez = WY - ZG

    for _ in tqdm(np.arange(n_perm)):

        ## Create permuted dataset.
        np.random.shuffle(Ez)
        WY_star = Ez + ZG

        ## Preallocate space.
        B_star = np.einsum('ijk,jk->ik', XXX, WY_star)

        ## Compute residual error.
        epsilon = WY - np.einsum('ijk,jk->ik', WX, B_star)

        ## Compute standard error.
        se = np.zeros_like(B)
        for i in np.arange(V):
            sigma_sq = epsilon[:,i] @ epsilon[:,i] / (T - K)
            se[:,i] = np.sqrt(sigma_sq * np.diag(XtX[...,i]))

        ## Compute test statistic.
        F_star = B_star / se

        ## Compare to observed statistic (two-tailed).
        p += (np.abs(F_star).max(axis=-1).reshape(-1,1) > np.abs(F)).astype(int)

    ## Convert to p-values.
    p /= n_perm + 1
    p = -np.log10(p) * np.sign(F)

    return B, F, p