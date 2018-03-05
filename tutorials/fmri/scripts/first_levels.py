import numpy as np
from scipy.linalg import cholesky, svd, LinAlgError

def dot_self(arr):
    return np.inner(arr,arr)

def correlate(x,y):
    '''Product moment Pearson correlation'''
    x -= x.mean()
    y -= y.mean()
    return np.inner(x, y) / (np.sqrt(dot_self(x)) * np.sqrt(dot_self(y)))

def autocorrelate(arr, order):
    '''Returns autocorrelation matrix of order N'''
    V = np.diag(np.ones_like(arr))
    for n in np.arange(order)+1:
        v = np.diag(np.ones(arr.size - n) * correlate(arr[n:], arr[:-n]), -n)
        V += v + v.T
    return(V)

def cholesky_whitening(V):
    '''Returns whitening matrix from Cholesky decomposition'''
    U = cholesky(V, lower=False)
    return np.linalg.inv(U)

def svd_whitening(V):
    '''Returns whitening matrix from SVD (i.e. matrix inverse square root)'''
    U, S, Vh = svd(V)
    return U.dot(np.diag(1/np.sqrt(S))).dot(Vh)

def ols(Ys, Xs):
    return np.linalg.inv(Xs.T.dot(Xs)).dot(Xs.T.dot(Ys))

def OLS(Y, X, W, n_drop=0):
    '''Wrapper function
    - y: dependent variable, [N, 1]
    - X: independent variable, [N, M]
    - W: whitening matrix, [N, N]
    - n_drop: drop the first n rows.'''
    
    ## Drop frames.
    Y = Y[n_drop:]
    X = X[n_drop:]
    W = W[n_drop:,n_drop:]
    
    ## Premultiply.
    Ys = W.dot(Y)
    Xs = W.dot(X)
    
    ## Perform OLS.
    ces = ols(Ys,Xs)
        
    ## Compute standard error of coefficients.
    residuals = Ys - Xs.dot(ces)
    sigma_sq = dot_self(residuals) / np.subtract(*Xs.shape)
    cesvar = np.sqrt(sigma_sq * np.diag(np.linalg.inv(Xs.T.dot(Xs))))
    return ces, cesvar

def first_level_OLS(Y, X, ac_order=1, n_drop=4):
    '''NOTE: We do not smooth residuals as we assume first levels already smoothed.
    We trade off between Cholesky and singular value decomposition for autocorrelation
    matrices that are not positive semi-definite (PSD). Cholesky decomposition is substantially
    faster, and a large majority of autocorrelation matrices from empirical testing were PSD, 
    so this code should run reasonably fast. Expect slowdowns with more violations of PSD.'''
    ## Initial computation of residuals.
    ces, _, _,_ = np.linalg.lstsq(X,Y)
    residuals = Y - X.dot(ces)

    ## Preallocate space.
    ces *= np.nan
    cesvar = ces.copy()
    ac_coef = ces[:ac_order].copy()

    ## Main loop.
    for n, resid in enumerate(residuals.T):

        ## Skip missing data.
        if np.any(np.isnan(resid)): 
            continue
            
        ## Compute whitening matrix.
        V = autocorrelate(resid, ac_order)
        try:
            W = cholesky_whitening(V) # Cholesky decompostion (fast)
        except LinAlgError:
            W = svd_whitening(V)      # Singular value decomposition (slow)
        ac_coef[:,n] = [np.diag(V, i+1)[0] for i in range(ac_order)]
        
        ## Perform OLS.
        ces[:,n], cesvar[:,n] = OLS(Y[:,n], X, W, n_drop=n_drop)
        
    return ces, cesvar, ac_coef