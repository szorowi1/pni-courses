import numpy as np

def firing_rate(u, theta=0.3, beta=0.5):
    return 0.5 + 0.5 * np.tanh( (u - theta) / beta )

class SingleBump(object):
    '''Recreation of single_bump.m

    INPUTS
    - dt:     timestep size
    - T:      time after which simulation stops
    - N:      number of cells in the simulation
    - wE:     local excitatory weight strength
    - gI:     global inhibition, from every cell to every cell
    - gD:     global drive, an external constant drive to every cell
    - sigmaE: width of excitatory neighborhood
    - sigmaN: sigma noise, magnitude of noise in each cell
    - leakN:  static randomness, across cells, in their "leak membrane conductance"
    - wD:     strength of external gaussian drive
    - sigmaD: external gaussian drive has same width as default exc conn width
    - muD:    drive starts at midpoint of screen.
    - dV:     drive speed, in neuron positions per unit time.
    - u0:     optional initial conditions for u.'''
    
    def __init__(self, dt=0.1, T=10000, N=250, wE=1.4, sigmaE=4, gI=0.4, gD=2.1, 
                sigmaN=0.4, leakN=0, wD=0, sigmaD=4, muD=0.5, dV=0, u0=False):
        
        ## Store all values.
        self.dt     = dt
        self.T      = T
        self.N      = N
        self.wE     = wE
        self.gI     = gI
        self.gD     = gD
        self.wD     = wD
        self.muD    = muD * N
        self.sigmaE = sigmaE
        self.sigmaN = sigmaN
        self.sigmaD = sigmaD
        self.leakN  = leakN
        self.dV     = dV
        self.u0     = u0
    
    def compute_weights(self):
        '''convenience function: compute excitatory weights'''
        ## Preallocate space.
        weights = np.zeros((self.N, self.N))
        
        ## Compute weights.
        for i in np.arange(self.N-1):
            for j in np.arange(i+1,self.N):
                delta = np.abs(i-j)
                weights[i,j] += np.exp( -delta**2 / (2*self.sigmaE**2) ) / self.sigmaE
                weights[j,i] += np.exp( -delta**2 / (2*self.sigmaE**2) ) / self.sigmaE
        
        ## Store.
        self.weights = weights
        
    def update_drive(self):
        '''convenience function: update drive dynamics'''
        ## Update drive position.
        self.muD += self.dV * self.dt
        if self.muD > self.N - 2 * self.sigmaE: self.dV = -self.dV
        elif self.muD < 2 * self.sigmaE: self.dV = -self.dV

        ## Update external drive.
        return self.wD * np.exp( -( np.arange(1,self.N+1) - self.muD)**2 / (2*self.sigmaD ** 2) )
        
    def compute_dudt(self, u, r, leak, eD):
        '''convenience function: compute du/dt'''
        return -leak * u - self.gI*np.sum(r) + self.wE*self.weights.dot(r) - \
                self.sigmaN * np.random.normal(size=u.size)*np.sqrt(self.dt) + self.gD + eD 
        
    def run_simulation(self):
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Preparations.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
        ## Store first time.
        t = 0 
        
        ## Preallocate space.
        u = np.zeros(self.N)        # Membrane potential
        r = np.zeros(self.N)        # Firing rate.
        if self.u0: u[0] = self.u0  
        
        ## Compute leaks.
        leak = np.ones_like(r) + self.leakN * np.random.normal(size=r.size); 
        leak[leak<0] = 0
        
        ## Compute weights.
        self.compute_weights()
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Main loop.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        while t < self.T:

            ## Update time.
            t += self.dt

            ## Update driving dynamics.
            eD = self.update_drive()
            
            ## Compute du/dt.
            dudt = self.compute_dudt(u, r, leak, eD)

            ## Estimate u with Euler's method.
            u += dudt * self.dt

            ## Update firing rate.
            r = firing_rate(u)

            ## Update time.
            t += self.dt
        