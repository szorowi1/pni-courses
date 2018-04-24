functions {

    real sparse_iar_lpdf(vector b, real tau, vector D, vector Aw, 
                         int[] Av, int[] Au, int V) {
      real bDb;    // b' * D * b
      real bAb;    // b' * A * b
    
      bDb = b' * (D .* b);
      bAb = b' * csr_matrix_times_vector(V, V, Aw, Av, Au, b);
    
      return 0.5 * ( (V-1) * log(tau) - tau * (bDb - bAb) );
  }
    
}
data {
    
    // Metadata
    int T;                  // Number of time points
    int V;                  // Number of voxels
    int K;                  // Number of task regressors
    int M;                  // Number of nuisance regressors
    int AR;                 // Autoregressive order
    int nz;                 // Number of nonzero elements in A
    
    // Data
    vector[V] Y[T];         // Observed data
    vector[K] X[T];         // Task regressors
    vector[M] Z[T];         // Nuisance regressors 
    
    // Graph laplacian
    vector[V]  D;           // Degree vector       
    vector[nz] Aw;          // Adj mat values
    int Av[nz];             // Adj mat column indices
    int Au[V+1];            // Adj mat row indices
    
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
    matrix[V,AR] rho_pr;    // AR(n) estimates (pre-transform)    
    real<lower=0> sigma;    // Variance on residual error
    
    // Hyperparameters
    vector<lower=0>[K] tau; // Variance on weight priors
    vector<lower=0>[K] tau; // Variance on weight priors

}
model {

    // Generated quantities
    vector[V] mu;           // Estimated mean
    matrix[V,AR] epsilon;   // Residuals
    matrix[V,AR] rho_pr;    // AR(n) estimates (pre-transform)
    epsilon = rep_matrix(0, V, AR);
    
    // Priors
    for (i in 1:K){
        B[:,i] ~ sparse_iar_lpdf(tau[i], D, Aw, Av, Au, V);
    }
    for (i in 1:M){
        G[:,i] ~ normal(0, 1);
    }
    for (i in 1:AR){
        rho_pr[:,i] ~ sparse_iar_lpdf(tau[i], D, Aw, Av, Au, V);
        rho[:,i] = Phi_approx(rho_pr[:,i]);
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