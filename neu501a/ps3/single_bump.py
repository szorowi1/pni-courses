import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
%load_ext autoreload
%matplotlib qt5

def firing_rate(u, theta=0.5, beta=0.3):
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
    
    def _compute_weights(self):
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
        
    def _update_drive(self):
        '''convenience function: update drive dynamics'''
        
        ## Update drive position.
        self.muD += self.dV * self.dt
        if self.muD > self.N - 2 * self.sigmaE: self.dV = -self.dV
        elif self.muD < 2 * self.sigmaE: self.dV = -self.dV

        ## Update external drive.
        return self.wD * np.exp( -( np.arange(1,self.N+1) - self.muD)**2 / (2*self.sigmaD ** 2) )
        
    def _compute_dudt(self, u, r, leak, eD):
        '''convenience function: compute du/dt'''
        return -leak * u - self.gI*np.sum(r) + self.wE*self.weights.dot(r) - \
                self.sigmaN * np.random.normal(size=u.size)*np.sqrt(self.dt) + self.gD + eD 
        
    def _submit_gD(self, text):
        self.gD = float(text)
        
    def _submit_gI(self, text):
        self.gI = float(text)
        
    def _submit_wD(self, text):
        self.wD = float(text)
        
    def _submit_wE(self, text):
        self.wE = float(text)
        
    def _submit_dV(self, text):
        self.dV = float(text)
        
    def _submit_muD(self, text):
        self.muD = float(text)
        
    def _submit_leakN(self, text):
        self.leakN = float(text)
    
    def _submit_sigmaN(self, text):
        self.sigmaN = float(text)
        
    def _initialize_canvas(self):
        
        ## Initialize canvas.
        fig = plt.figure(figsize=(8,4))
        
        ## Initialize axes.
        ax1 = plt.subplot2grid((4,1),(0,0),rowspan=3)
        ax2 = plt.subplot2grid((4,1),(3,0))
        plt.subplots_adjust(left=0.05, right=0.75, top=0.925, bottom=0.075, hspace=0.35)
        
        ## Define buttons.
        x, xw, yw = 0.90, 0.08, 0.04
        
        sigmaN_text = TextBox(plt.axes([x,0.35,xw,yw]), r'$\sigma$ Noise', initial=str(self.sigmaN))
        sigmaN_text.on_submit(self._submit_sigmaN)
        
        gI_text = TextBox(plt.axes([x,0.40,xw,yw]), 'gI', initial=str(self.gI))
        gI_text.on_submit(self._submit_gI)
        
        wE_text = TextBox(plt.axes([x,0.45,xw,yw]), 'wE', initial=str(self.wE))
        wE_text.on_submit(self._submit_wE)
        
        gD_text = TextBox(plt.axes([x,0.55,xw,yw]), 'Global Drive', initial=str(self.gD))
        gD_text.on_submit(self._submit_gD)
        
        leakN_text = TextBox(plt.axes([x,0.65,xw,yw]), 'Leak Noise', initial=str(self.leakN))
        leakN_text.on_submit(self._submit_leakN)
        
        muD_text = TextBox(plt.axes([x,0.75,xw,yw]), 'Drive Position', initial=str(self.muD))
        muD_text.on_submit(self._submit_muD)
        
        dV_text = TextBox(plt.axes([x,0.80,xw,yw]), 'Drive Speed', initial=str(self.dV))
        dV_text.on_submit(self._submit_dV)
        
        wD_text = TextBox(plt.axes([x,0.85,xw,yw]), 'Drive Strength', initial=str(self.wD))
        wD_text.on_submit(self._submit_wD)
        
        return [fig, ax1, ax2, sigmaN_text, gI_text, wE_text, gD_text, leakN_text, 
                muD_text, dV_text, wD_text]
        
    def run_simulation(self, plot=False, sleep=0.01):
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Define parameters.
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
        self._compute_weights()
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Initialize figure.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
        if plot:
            
            ## Initialize canvas. 
            ## Unfortunately we need to pass all of the text boxes
            ## or else they fail to work. Sorry for the clunky code.
            fig, ax1, ax2, t1, t2, t3, t4, t5, t6, t7, t8 = self._initialize_canvas()
            
            ## Plot initial firing rates.
            r_line, = ax1.plot(r)
            ax1.set(xlim=(0,r.size), ylim=(-0.05,1.05))
            
            ## Plot initial driving dynamics.
            eD = self._update_drive()
            eD_line, = ax2.plot(eD)
            ax2.set(xlim=(0,eD.size))
            
            fig.canvas.draw()
            fig.canvas.flush_events()
            
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Main loop.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        while t < self.T:

            ## Update time.
            t += self.dt

            ## Update driving dynamics.
            eD = self._update_drive()
            
            ## Compute du/dt.
            dudt = self._compute_dudt(u, r, leak, eD)

            ## Estimate u with Euler's method.
            u += dudt * self.dt

            ## Update firing rate.
            r = firing_rate(u)

            ## Update time.
            t += self.dt
            
            ## Update plot.
            if plot:
                
                ## Update time.
                ax1.set_title('t = %0.2f' %t)
                
                ## Update firing rate.
                r_line.set_ydata(r)
                
                ## Update driving dynamics.
                eD_line.set_ydata(eD)
                ax2.set(ylim=(eD.min()-0.05, eD.max()+0.05))
                
                fig.canvas.draw()
                fig.canvas.flush_events()
                time.sleep(sleep)
                
        return r