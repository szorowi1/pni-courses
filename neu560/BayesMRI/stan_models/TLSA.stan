functions {
    
    /** Logistic basis function
    * Return the gradient of activation as voxels move from center
    * corresponding to a sigmoid.
    *
    * @param R Matrix containing coordinates of voxels
    * @param loc Vector containing center of activation
    * @param fwhm Scalar representing halfway point of activation
    * @param scale Scalar representing slope of gradient
    *
    * @return f Vector containing gradient
    */
    vector lbf(matrix R, row_vector loc, real fwhm, real scale) {
        vector[rows(R)] f;
        
        // Compute Euclidean norm
        f = sqrt( rows_dot_self( R - rep_matrix(loc, rows(R)) ) );
        
        // Compute logistic basis function
        f = rep_vector(1, rows(R)) ./ (1. + exp( (f - fwhm) / scale ));
        
        // Normalize values.
        f /= max(f);
        
        return f;
    }
    
}
data {
    
    // Metadata
    int T;                  // Number of time points
    int V;                  // Number of voxels
    int K;                  // Number of task regressors
    int Z;                  // Number of latent states
    int D;                  // Number of dimensions (2d vs. 3d)
    
    // Data
    row_vector[V] Y[T];     // Observed data
    row_vector[K] X[T];     // Task regressors
    matrix[V, D] R;         // Voxel coordinates
    
}
parameters {

    // Regression weights
    row_vector[K*Z] W;      // Weights on task regressors
    real<lower=0> sigma;    // Variance on residual error

    // Basis functions
    vector<lower=0>[Z] fwhm;     // Halfway point of basis functions
    vector<lower=0>[Z] scale;    // Decay slope of basis fucntions 
    
}
model {

    // Generated quantities
    matrix[V, Z] F;         // Latent basis functions
    row_vector[V] mu;       // Estimated mean
    row_vector[D] loc[Z];    
    
    loc[1] = [2.5, 2.5];
    loc[2] = [7.5, 7.5];
    
    // Priors
    W ~ normal(0, 1);
    fwhm ~ normal(0, 1);
    scale ~ normal(0, 1);
    
    for (i in 1:Z){
        F[:,i] = lbf( R, loc[i], fwhm[i], scale[i] );
    }    
    
    // Likelihood
    for (i in 1:T){
        
        // Compute estimated mean.
        mu = X[i] * to_matrix(W, K, Z) * F';
            
        // Likelihood of estimate.
        Y[i] ~ normal(mu, sigma);
        
    }
    
}