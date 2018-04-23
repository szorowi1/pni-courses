data {
    
    // Metadata
    int T;                  // Number of time points
    int V;                  // Number of voxels
    int K;                  // Number of task regressors
    int M;                  // Number of nuisance regressors
    int AR;                 // Autoregressive order
    
    // Data
    vector[V] Y[T];         // Observed data
    vector[K] X[T];         // Task regressors
    vector[M] Z[T];         // Nuisance regressors    
    
}
transformed data {
    
    matrix[AR,AR] P;        // Permutation matrix
    
    P = rep_matrix(0, AR, AR);
    P[AR, 1] = 1;
    for (i in 1:AR-1){
        P[i, i+1] = 1;
    }
    
}
parameters {

    matrix[V, K] B;         // Weights on task regressors
    matrix[V, M] G;         // Weights on nuisance regressors
    real<lower=0> sigma;    // Variance on residual error
    
    matrix<lower=0,upper=1>[V,AR] rho; // Autocorrelation

}
model {

    // Generated quantities
    vector[V] mu;           // Estimated mean
    matrix[V,AR] epsilon;   // Residuals
    epsilon = rep_matrix(0, V, AR);
    
    // Priors
    for (i in 1:K){
        B[:,i] ~ normal(0, 1);
    }
    for (i in 1:M){
        G[:,i] ~ normal(0, 1);
    }
    for (i in 1:AR){
        rho[:,i] ~ beta(1,1);
    }
    sigma ~ normal(0, 2.5);
    
    for (i in 1:T){
        
        // Compute estimated mean.
        mu = B * X[i] + G * Z[i] + (epsilon .* rho) * rep_vector(1,AR);
            
        // Likelihood of estimate.
        Y[i] ~ normal(mu, sigma);
        
        // Update residuals.
        epsilon = epsilon * P;
        epsilon[:,1] = Y[i] - mu; 
        
    }
    
}