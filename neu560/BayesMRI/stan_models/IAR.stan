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
    int nz;                 // Number of nonzero elements in A
    
    // Data
    matrix[T, V] Y;         // Observed data
    matrix[T, K] X;         // Task regressors
    matrix[T, M] Z;         // Nuisance regressors
    
    // Graph laplacian
    vector[V]  D;           // Degree vector       
    vector[nz] Aw;          // Adj mat values
    int Av[nz];             // Adj mat column indices
    int Au[V+1];            // Adj mat row indices
    
}
parameters {

    matrix[V, K] B;         // Weights on task regressors
    matrix[V, M] G;         // Weights on nuisance regressors
    vector<lower=0>[K] tau; // Variance on weight priors
    real<lower=0> sigma;    // Residual error

}
model {

    // Priors
    for (i in 1:K){
        B[:,i] ~ sparse_iar_lpdf(tau[i], D, Aw, Av, Au, V);
    }
    for (i in 1:M){
        G[:,i] ~ normal(0, 1);
    }
    tau ~ normal(0, 2.5);
    sigma ~ normal(0, 2.5);
    
    // Likelihood
    to_vector(Y) ~ normal(to_vector(X * B' + Z * G'), sigma);

}