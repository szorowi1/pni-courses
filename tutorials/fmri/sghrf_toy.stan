functions {
    
    real rate(real mode, real sd){
        // Compute the rate of a gamma distribution from gamma(mode,sd)
        real rate;
        rate = ( mode + sqrt( mode^2 + 4*sd^2 ) ) / ( 2 * sd^2 );
        return rate;
    }
    
    real shape(real mode, real rate){
        // Compute the shape of a gamma distribution from gamma(mode,rate)
        real shape;
        shape = 1 + mode * rate;
        return shape;
    }

    vector single_gamma_hrf(vector t, real a, real b, real h){
        vector[rows(t)] yhat;
        for (n in 1:rows(t)){ 
            yhat[n] = (b^a) / tgamma(a) * t[n]^(a-1) * e()^(-b*t[n]); 
        }
        yhat = yhat / max(yhat); // Normalize gamma curve       
        yhat = h * yhat;         // Multiply by amplitude
        return yhat;
    }
    
}
data {

    // Metadata
    int n_subj;
    int n_bins;
    
    // Observed
    vector[n_bins] t;
    vector[n_bins] y[n_subj];

}
parameters {

    real<lower=0> M;
    real<lower=0> S;
    real<lower=-1, upper=1> A;
    
}
transformed parameters{

    real<lower=0> alpha;
    real<lower=0> beta;

    beta = rate(M, S);
    alpha = shape(M, beta);

}
model {
    
    M ~ gamma(5, 2);
    S ~ gamma(2.33, 2);
    A ~ normal(0, 0.2);
    
    // Likelihood
    for (n in 1:n_subj){
        y[n] ~ normal(single_gamma_hrf(t, alpha, beta, A), 0.1);
    }

}
generated quantities {
    vector[n_bins] yhat;
    yhat = single_gamma_hrf(t, alpha, beta, A);
}