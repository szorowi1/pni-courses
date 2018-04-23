import numpy as np

def excursion_mc(X, u, tail=0, alpha=0.05):
    '''Pythonic implementation of `excursion.mc` from the 
    `excursions` package in R (Bolin & Lindgren, 2016).
    
    Parameters
    ----------
    X : 2d array
      Samples for MCMC, [n_param, n_samples].
    u : float
      Activity threshold. 
    tail : -1 or 0 or 1 (default = 0)
      Hypothesis test. See notes.
    alpha : float, [0,1].
      Confidence level.
    
    Returns
    -------
    E : 1d array
      Indices of excursion set.
      
    Notes
    -----
    If tail is 1, the alternative hypothesis is that the 
    mean of the data is greater than 0 (upper tailed test). 
    If tail is 0, the alternative hypothesis is that the mean 
    of the data is different than 0 (two tailed test). If tail 
    is -1, the alternative hypothesis is that the mean of the 
    data is less than 0 (lower tailed test).
    '''
    
    ## Calculate marginal probabilities.
    if tail == 0:
        rho = (np.abs(B) > u).mean(axis=-1)
    elif tail == 1:
        rho = (B > u).mean(axis=-1)
    elif tail == -1:
        rho = (B < u).mean(axis=-1)
    else:
        raise ValueError('tail must be -1 or 0 or 1')
    
    ## Sort (descending).
    indices = np.arange(rho.size)
    indices = indices[np.argsort(rho)[::-1]]
    rho = rho[np.argsort(rho)[::-1]]

    ## Compute joint probability sets.
    cumprod = np.cumprod(rho)
    
    ## Find excursion set.
    E = indices[cumprod >= 1 - alpha]
    return np.sort(E)