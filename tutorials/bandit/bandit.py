import numpy as np

def softmax(arr, beta=1):
    '''Softmax function.
    
    Parameters
    ----------
    arr : 1-d array
      array of values.
    beta : scalar
      inverse temperature parameter.
    
    Returns
    -------
    p : 1-d array
      normalized values (sum to 1).
    '''
    return np.exp(beta * arr) / np.sum( np.exp( beta * arr ) )

class Bandit(object):
    '''Class for simulated agent playing N-arm bandit task.
    
    Parameters
    ----------
    alpha : scalar
      learning parameter in the range of [0, 1].
    beta : scalar
      inverse temperature parameter.
    epsilon : scalar, string
      exploration/exploitation parameter. Either scalar in range of [0, 1], 
      determining fraction of times random action is selected; or "softmax",
      where softmax plus multinomial probability functions selects action. 
    '''
    
    def __init__(self, alpha=0.1, beta=5, epsilon='softmax'):
        
        ## Error-catching.
        if not (alpha >= 0 and alpha <= 1):
            raise ValueError('Alpha must be within [0,1].')
        elif not (epsilon == 'softmax' or (epsilon >= 0 and epsilon <= 1)):
            raise ValueError('Epsilon must be within [0,1] or equal to "softmax".')
        
        ## Set values.
        self._alpha = np.copy(alpha)
        self._beta = np.copy(beta)
        self._epsilon = np.copy(epsilon)
        self.info = dict(alpha = self._alpha, beta = self._beta, epsilon=self._epsilon)
        
    def _init_q(self, Q, R):
        '''Convenience function to initialize Q-table.
        
        Parameters
        ----------
        Q : scalar, array shape=(n_arms,)
          Initial values for Q-table.
        R : array, shape=(n_trials, n_arms)
          Predetermined reward values for bandit task.
        
        Returns
        -------
        Q : array, shape=(n_arms,)
          Initial values for Q-table.
        R : array, shape=(n_trials, n_arms)
          Predetermined reward values for bandit task.
        '''
        
        ## Force to NumPy array.
        Q, R = np.copy(Q).astype(float), np.copy(R).astype(float)
        
        ## Initialize Q-table.
        if not np.ndim(Q):
            Q = np.ones(R.shape[1]) * Q
        elif np.ndim(Q) > 1:
            raise ValueError('Initial values for Q-table must be scalar or 1d array.')
            
        return Q, R
    
    def _init_score(self, Q, R, C):
        '''Convenience function to initialize values in scoring function.'''
        
        ## Force to NumPy arrays.
        Q, R, C = np.copy(Q).astype(float), np.copy(R).astype(float), np.copy(C).astype(int)
        
        ## Force to shape=(n_blocks, n_trials, n_arms).
        if np.ndim(R) < 3:
            R, C = np.expand_dims(R,0), np.expand_dims(C,0)
            
        ## Initialize Q-table.
        if not np.ndim(Q):
            Q = np.ones(R.shape[-1]) * Q
        elif np.ndim(Q) > 1:
            raise ValueError('Initial values for Q-table must be scalar or 1d array.')
            
        return Q, R, C
        
    def _select_action(self, q):
        '''Action selection function. See simulate function for details.
        
        Parameters
        ----------
        q : 1-d array
          Q-values on a particular trial.
          
        Returns
        -------
        c : int
          integer, corresponding to index of action selected.
        '''
        
        if self._epsilon == 'softmax':
            p = softmax(q, self._beta)
            c = np.argmax(np.random.multinomial(1, p, 1))
        elif np.any(np.random.binomial(1, 1 - self._epsilon, 1)):
            c = np.argmax(q)
        else:
            c = np.random.choice(np.arange(q.size), 1)
        return c      
        
    def simulate(self, R, Q=False):
        '''Simulate bandit task for agent. 
        
        Parameters
        ----------
        R : array, shape=(n_trials, n_arms)
          Predetermined reward values for bandit task.
        Q : scalar, array shape=(n_arms,)
          Initial values for Q-table. If scalar, Q initialized as
          1-d array with all the same value.
        
        Returns
        -------
        Q : array, shape=(n_trials, n_arms)
          Final values in Q-table.
        C : array, shape=(n_trials)
          Choices (i.e. selected arm) on each trial.
          
        Notes
        -----
        The strategy for action selection is contingent on the epsilon parameter.
        If epsilon is a scalar (in the range of [0, 1]), then the agent will 
        perform greedy selection, selecting the most valuable option 1 - epsilon
        fraction of times. If epsilon is set to "softmax", then the agent will
        select an action probabilistically with each action probability scaled
        by the softmax function.
        '''
        
        ## Initialize Q-table.
        Q, R = self._init_q(Q, R)
            
        ## Preallocate space for choices.
        C = np.zeros(R.shape[0], dtype=int)
        
        ## Run bandit task.
        for i in np.arange(R.shape[0]):
            
            ## Select action.
            C[i] = self._select_action(Q)
            
            ## Take action / update values.                
            Q[C[i]] += self._alpha * ( R[i,C[i]] - Q[C[i]] )
            
        return Q, C
    
    def score(self, R, C, Q=False):
        '''Estimate likelihood of observing choice behavior, C,
        conditioned on rewards, R, and agent parameters.
        
        Parameters
        ----------
        R : array, shape=(n_blocks, n_trials, n_arms)
          Reward values for bandit task.
        C : array, shape=(n_blocks, n_trials)
          Choices observed during bandit task. 
        
        Returns
        -------
        log_lik : scalar
          Log-likelihood of model.
          
        Notes
        -----
        Assumes epsilon = "softmax". 
        '''
        
        ## Initialize values.
        Q, R, C = self._init_score(Q, R, C)
        n_blocks, n_trials, n_arms = R.shape
        
        ## Compute log-likelihood.
        log_lik = 0
        for i in np.arange(n_blocks):

            q = np.copy(Q)

            for j in np.arange(n_trials):

                ## Compute likelihood.
                theta = softmax(q, beta=self._beta)
                log_lik += np.log(theta[C[i,j]])

                ## Update Q-value.
                q[C[i,j]] += self._alpha * ( R[i,j,C[i,j]] - q[C[i,j]] )
                
        return log_lik