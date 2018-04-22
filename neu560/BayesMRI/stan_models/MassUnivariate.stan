data {
    
    // Metadata
    int T;                  // Number of time points
    int V;                  // Number of voxels
    int K;                  // Number of task regressors
    int M;                  // Number of nuisance regressors
    
    // Data
    matrix[T, V] Y;         // Observed data
    matrix[T, K] X;         // Task regressors
    matrix[T, M] Z;         // Nuisance regressors
    
}
parameters {

    matrix[V, K] B;         // Weights on task regressors
    matrix[V, M] G;         // Weights on nuisance regressors
    real<lower=0> sigma;    // Residual error

}
model {

    // Priors
    for (i in 1:K){
        B[:,i] ~ normal(0, 1);
    }
    for (i in 1:M){
        G[:,i] ~ normal(0, 1);
    }
    sigma ~ normal(0, 2.5);
    
    // Likelihood
    to_vector(Y) ~ normal(to_vector(X * B' + Z * G'), sigma);

}