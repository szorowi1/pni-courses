import numpy as np
from scipy.special import gammaln
from scipy.special import gamma as fgamma
# https://github.com/nipy/nipype/blob/master/nipype/algorithms/modelgen.py
# https://github.com/PyMVPA/PyMVPA/blob/master/mvpa2/misc/fx.py

def spm_hrf(RT, P=None, fMRI_T=16):
    """ python implementation of spm_hrf
    see spm_hrf for implementation details
    % RT   - scan repeat time
    % p    - parameters of the response function (two gamma
    % functions)
    % defaults  (seconds)
    %   p(0) - delay of response (relative to onset)6
    %   p(1) - delay of undershoot (relative to onset)    16
    %   p(2) - dispersion of response 1
    %   p(3) - dispersion of undershoot 1
    %   p(4) - ratio of response to undershoot  6
    %   p(5) - onset (seconds) 0
    %   p(6) - length of kernel (seconds)		  32
    %
    % hrf  - hemodynamic response function
    % p    - parameters of the response function
    the following code using scipy.stats.distributions.gamma
    doesn't return the same result as the spm_Gpdf function ::
        hrf = gamma.pdf(u, p[0]/p[2], scale=dt/p[2]) -
              gamma.pdf(u, p[1]/p[3], scale=dt/p[3])/p[4]
    """
    p = np.array([6, 16, 1, 1, 6, 0, 32], dtype=float)
    if P is not None:
        p[0:len(P)] = P

    _spm_Gpdf = lambda x, h, l: np.exp(h * np.log(l) + (h - 1) * np.log(x) - (l * x) - gammaln(h))
    # modelled hemodynamic response function - {mixture of Gammas}
    dt = RT / float(fMRI_T)
    u = np.arange(0, int(p[6] / dt + 1)) - p[5] / dt
    with np.errstate(divide='ignore'):  # Known division-by-zero
        hrf = _spm_Gpdf(u, p[0] / p[2], dt / p[2]) - _spm_Gpdf(u, p[1] / p[3],
                                                               dt / p[3]) / p[4]
    idx = np.arange(0, int((p[6] / RT) + 1)) * fMRI_T
    hrf = hrf[idx]
    hrf = hrf / np.sum(hrf)
    return hrf

def gamma(x, a, b):
    '''pdf of gamma(shape, rate)'''
    return b ** a / fgamma(a) * x ** (a - 1) * np.exp(-b * x)

def to_sr(mode, sd):
    '''convenience function: gamma(mode,sd) --> gamma(shape,rate)'''
    rate = ( mode + np.sqrt( mode**2 + 4*sd**2 ) ) / ( 2 * sd**2 )
    shape = 1 + mode * rate
    return shape, rate

def from_sr(a, b):
    '''convenience function: gamma(shape,rate) --> gamma(mode,sd)'''
    mode = (a - 1) / b
    sd = np.sqrt(a) / b
    return mode, sd

def empirical_fwhm(t,y):  
    '''for best results, vector of times (t) should have reasonable resolution'''
    tpeak = t[y.argmax()]
    t1 = t[t < tpeak][ np.argmin( np.power(y[t < tpeak] - y.max() / 2, 2) ) ]
    t2 = t[t > tpeak][ np.argmin( np.power(y[t > tpeak] - y.max() / 2, 2) ) ]
    return t1, t2, t2 - t1