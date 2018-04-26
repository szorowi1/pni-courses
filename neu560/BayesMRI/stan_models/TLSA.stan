functions {
    
    vector rbf(matrix R, row_vector mu, real lambda) {
        vector[rows(R)] f;
        
        // Compute Euclidean norm
        f = sqrt( rows_dot_self( R - rep_matrix(mu, rows(R)) ) );
        
        // Compute radial basis function
        f = exp( -f / lambda^2 );
            
        return f;
    }
    
}
data {
    
    // Metadata
    int T;                  // Number of time points
    int V;                  // Number of voxels
    int K;                  // Number of task regressors
    int S;                  // Number of latent states
    int D;                  // Number of dimensions (2d vs. 3d)
    
    // Data
    row_vector[V] Y[T];     // Observed data
    row_vector[K] X[T];     // Task regressors
    matrix[V, D] R;         // Voxel coordinates
    
}
parameters {

    // Regression weights
    row_vector[K*S] W;          // Weights on task regressors
    row_vector 
    real<lower=0> sigma;    // Variance on residual error

    // Basis functions
    vector[S] lambda;    // Decay of basis fucntions 

}
model {

    // Generated quantities
    matrix[V, S] F;         // Latent basis functions
    row_vector[V] mu;     // Estimated mean
    row_vector[D] loc[S];    
    
    loc[1] = [2.5, 2.5];
    loc[2] = [7.5, 7.5];
    
    // Priors
    W ~ normal(0, 1);
    sigma ~ normal(0, 1);
    lambda ~ normal(0, 1);
    
    for (i in 1:S){
        F[:,i] = rbf( R, loc[i], exp(lambda[i]) );
    }    
    
    // Likelihood
    for (i in 1:T){
        
        // Compute estimated mean.
        mu = X[i] * to_matrix(W, K, S) * F';
            
        // Likelihood of estimate.
        Y[i] ~ normal(mu, sigma);
        
    }
    
}