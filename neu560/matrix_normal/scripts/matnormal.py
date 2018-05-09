import numpy as np
import scipy.sparse as sp
from scipy.optimize import minimize
from scipy.spatial.distance import cdist
from sksparse.cholmod import cholesky

class MatrixNormalCAR(object):
    
    def __init__(self, IAR=True, method='L-BFGS-B'):
        
        ## Store optimization method.
        self.method = method
        
        ## Initialize model.
        if IAR:
            self.model = 'IAR'
            self._offset = 1e-3
        else: 
            self.model = 'CAR'
            self._offset = 0
        
    def compute_graph_laplacian(self, rr):
        '''Compute degree matrix (D) and adjacency matrix (A).
        
        Parameters
        ----------
        rr : nd array.
          Points in N-dimensional space.
          
        Returns
        -------
        D : csc_sparse matrix
          Degree matrix
        A : csc_sparse matrix
          Adjacency matrix
        '''
        
        ## Compute distances.
        rr = cdist(rr,rr)

        ## Identify adjacent points.
        rows, cols = np.where(rr==1)
        data = np.ones_like(rows)
        
        ## Construct sparse matrices.
        A = sp.coo_matrix((data, (rows,cols)), shape=rr.shape)
        D = sp.coo_matrix(np.diag(np.asarray(np.sum(A, axis=0)).squeeze()))

        return D.tocsc(), A.tocsc()
    
    def _omega_v(self, tau, alpha, D, A):
        '''Returns spatial precision matrix'''
        return tau**-1 * (D - alpha * A + self._offset * sp.eye(D.shape[0]))
    
    def _precompute_matrices(self, Y, X, Omega_v, sigma, V, K):
        '''Convenience function'''
        
        Yvec = Y.flatten(order='F')           # Vectorize Y ("order" must be F!)
        Xblck = sp.kron(sp.eye(V), X)         # Block-diagonal of design matrix.
        invC = sp.kron(Omega_v, sp.eye(K))    # Inverse prior covariance.
        XtX = sp.kron(sp.eye(V), X.T @ X)     # Block-diagonal of design covariance.
        XtY = Xblck.T @ Yvec                  # Stimulus filter.
        M = XtX / sigma**2 + invC             # Inverse posterior covariance.
    
        return Yvec, Xblck, invC, XtX, XtY, M
    
    def log_lik(self, params, Y, X, D, A):
        '''Matrix-normal negative log-likelihood'''
        
        ## Define hyperparameters.
        alpha = 1
        if len(params) == 2: tau, sigma = params
        else: tau, alpha, sigma = params
        
        ## Define metadata.
        T, V = Y.shape
        T, K = X.shape        
        
        ## Precompute matrices.
        Omega_v = self._omega_v(tau, alpha, D, A)
        Yvec, _, invC, _, XtY, M = self._precompute_matrices(Y, X, Omega_v, 
                                                             sigma, V, K)
        
        ## Log quadratic term.
        log_quad = (-0.5 * (Yvec @ Yvec) / sigma**2 +
                    0.5 * XtY.T @ cholesky(M.tocsc())(XtY) / sigma**4)

        ## Log determinant.
        log_det = -0.5 * (cholesky(M.tocsc()).logdet() -
                          cholesky(invC.tocsc()).logdet() +
                          T*V*np.log(sigma**2))

        ## Additive constant.
        const = -0.5 * Yvec.size * np.log(2 * np.pi)

        return -(const + log_det + log_quad)
        
    def fit(self, Y, X, D, A, x0=None, lb=1e-3):
        '''Fit matrix-normal IAR/CAR model.'''
        
        ## Define initial parameters
        if self.model == 'IAR' and x0 is None: 
            x0 = [1, 5]
        elif self.model == 'CAR' and x0 is None:
            x0 = [1, 0.5, 5]
            
        ## Define bounds.
        if self.model == 'IAR':
            bounds = [(lb, None), (lb, None)]
        elif self.model == 'CAR':
            bounds = [(lb, None), (lb, 1-lb), (lb, None)]
        
        ## Fit model.
        fit = minimize(self.log_lik, x0, args=(Y, X, D, A), method=self.method, bounds=bounds)
        
        ## Store results.
        self.success = fit.success
        self.params = fit.x
        
        ## Solve for W.
        return self.solve(self.params, Y, X, D, A)
        
    def solve(self, params, Y, X, D, A):
        '''Solve for W'''
        
        ## Define hyperparameters.
        alpha = 1
        if len(params) == 2: tau, sigma = params
        else: tau, alpha, sigma = params
        
        ## Define metadata.
        T, V = Y.shape
        T, K = X.shape        
        
        ## Precompute matrices.
        Omega_v = self._omega_v(tau, alpha, D, A)
        Yvec, Xblck, _, _, _, M = self._precompute_matrices(Y, X, Omega_v, 
                                                            sigma, V, K)
        
        ## Solve for W.
        W = cholesky(M.tocsc())(Xblck.T @ Yvec / sigma ** 2)
        
        return W