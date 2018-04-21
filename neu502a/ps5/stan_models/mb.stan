data {

    int N;             // Total trials
    int  Y[N,2];       // Choice data
    real R[N];         // Rewards

}
parameters {

    real eta_pr;       // Learning rate
    real beta_pr;      // Inverse temperature

}
transformed parameters {

    real<lower=0,upper=1> eta;
    real<lower=0,upper=10> beta;

    eta = Phi_approx(eta_pr);
    beta = Phi_approx(beta_pr) * 10;

}
model{

    // Generated quantities
    vector[2] Q[3];
    real delta;
    int s_prime;

    for (i in 1:3){Q[i] = rep_vector(0,2);}

    // Priors
    eta_pr ~ normal(0,1);
    beta_pr ~ normal(0,1);

    // Likelihood
    for (i in 1:N){

        // Likelihood of choice in first state.
        Y[i,1] ~ categorical_logit( beta * Q[1,:] );

        // Likelihood of choice in second state.
        s_prime = Y[i,1]+1;
        Y[i,2] ~ categorical_logit( beta * Q[s_prime,:] );

        // Compute reward prediction error.
        delta = R[i] - Q[s_prime, Y[i,2]]; 

        // Update Q-values.
        Q[s_prime, Y[i,2]] += eta * delta;
        Q[1, 1] = 0.7 * max(Q[2]) + 0.3 * max(Q[3]);
        Q[1, 2] = 0.3 * max(Q[2]) + 0.7 * max(Q[3]);
        
    }

}