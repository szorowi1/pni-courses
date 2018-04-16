import numpy as np
from numpy.fft import fft, ifft
## NOTE: I owe Michael Waskom a beer.
    
def default_tukey_window(n):
    """The default rule for choosing the Tukey taper window used by FSL."""
    return int(np.floor(np.sqrt(n)))

def estimate_residual_autocorrelation(Y, X, tukey_m=None):
    """Fit OLS model and estimate residual autocorrelation with regularization.
    
    Parameters
    ----------
    Y : n_tp x n_vox array
        Array of time series data for multiple voxels.
    X : n_tp x n_ev array
        Design matrix for the model.
    tukey_m: int or None
        Size of tukey taper window or None to use default rule.
   
   Returns
    -------
    acf : tukey_m x n_vox array
        Regularized autocorrelation function estimate for each voxel.
    """
    
    # Fit initial iteration OLS model in one step
    B_ols, _, _, _ = np.linalg.lstsq(X, Y)
    Yhat_ols = X.dot(B_ols)
    resid_ols = Y - Yhat_ols

    # Compute empircal residual autocorrelation function
    n_tp = Y.shape[0]
    if tukey_m is None:
        tukey_m = default_tukey_window(n_tp)
    acf_pad = n_tp * 2 - 1
    resid_fft = fft(resid_ols, n=acf_pad, axis=0)
    acf_fft = resid_fft * resid_fft.conjugate()
    acf = ifft(acf_fft, axis=0).real[:tukey_m]
    acf /= acf[[0]]

    # Regularize the autocorrelation estimate with a tukey taper
    lag = np.expand_dims(np.arange(tukey_m), 1)
    window = .5 * (1 + np.cos(np.pi * lag / tukey_m))
    acf *= window

    return acf

def prewhiten_data(Y, X):
    """Estimate autocorrelation and transform data and design for OLS.
    
    Parameters
    ----------
    Y : n_tp x n_vox array
        Array of time series data for multiple voxels.
    X : n_tp x n_ev array
        Design matrix array. Should have zero mean and no constant.
    smooth_fwhm : float
        Size (in mm) of the smoothing kernel for smoothing the autocorrelation
        estimates. Requires that the time series image affine has correct
        information about voxel size.
   
    Returns
    -------
    WY : n_tp x n_vox array
        Prewhitened time series data for voxels in mask.
    WX : n_tp x n_ev x n_vox array
        Prewhitened design matrix for voxels in mask.
    """
    
    n_tp, n_vox = Y.shape
    n_ev = X.shape[1]
    assert X.shape[0] == n_tp

    # Estimate the autocorrelation function of the model residuals
    acf_smooth = estimate_residual_autocorrelation(Y, X)
    tukey_m, _ = acf_smooth.shape

    # Compute the autocorrelation kernel
    w_pad = n_tp + tukey_m
    acf_kernel = np.zeros((w_pad, n_vox))
    acf_kernel[:tukey_m] = acf_smooth
    acf_kernel[-tukey_m + 1:] = acf_smooth[:0:-1]
    assert (acf_kernel != 0).sum() == (n_vox * (tukey_m * 2 - 1))

    # Compute the prewhitening kernel in the spectral domain
    acf_fft = fft(acf_kernel, axis=0).real
    W_fft = np.zeros((w_pad, n_vox))
    W_fft[1:] = 1 / np.sqrt(np.abs(acf_fft[1:]))
    W_fft /= np.sqrt(np.sum(W_fft[1:] ** 2, axis=0, keepdims=True) / w_pad)

    # Prewhiten the data
    Y_fft = fft(Y, axis=0, n=w_pad)
    WY = ifft(W_fft * Y_fft, axis=0).real[:n_tp].astype(np.float32)
    assert WY.shape == (n_tp, n_vox)

    # Prewhiten the design
    WX = np.empty((n_tp, n_ev, n_vox), np.float32)
    for i in range(n_ev):
        X_i = X[:, [i]]
        X_fft_i = fft(X_i, axis=0, n=w_pad)
        WX_i = ifft(W_fft * X_fft_i, axis=0).real[:n_tp]
        WX[:, i, :] = WX_i.astype(np.float32)

    return WY, WX