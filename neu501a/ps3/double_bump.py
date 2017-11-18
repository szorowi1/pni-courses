import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

## NOTE: The following code *requires* Matplotlib v2.1.0. TextBox widgets 
## were not added to Matplotlib before this version: 
## https://github.com/matplotlib/matplotlib/issues/7724/

def firing_rate(u, theta=0.5, beta=0.3):
    return 0.5 + 0.5 * np.tanh( (u - theta) / beta )

class DoubleBump(object):
    '''Recreation of single_bump.m

    INPUTS
    - dt:      timestep size
    - T:       time after which simulation stops
    - N:       number of cells in the simulation
    - wE:      local excitatory weight strength
    - gI:      global inhibition, from every cell to every cell
    - gD:      global drive, an external constant drive to every cell
    - sigmaE:  width of excitatory neighborhood
    - sigmaN:  sigma noise, magnitude of noise in each cell
    - leakN:   static randomness, across cells, in their "leak membrane conductance"
    - sigmaD:  external gaussian drive has same width as default exc conn width
    - wD1:     strength of external gaussian drive
    - muD1:    drive starts at midpoint of screen.
    - dV1:     drive speed, in neuron positions per unit time.
    - wD2:     strength of external gaussian drive
    - muD2:    drive starts at midpoint of screen.
    - dV2:     drive speed, in neuron positions per unit time.
    - u0:      optional initial conditions for u.
    - mapping: Can pass in the permutation that goes from one space to the other.'''
    
    def __init__(self, dt=0.1, T=10000, N=250, wE=1.4, gI=0.4, gD=2.1, sigmaE=4,
                 sigmaN=0.4, leakN=0, sigmaD=4, wD1=0,  muD1=0.5, dV1=0, 
                 wD2=0,  muD2=0.5, dV2=0, u0=False, mapping=False):
        
        ## Store all values.
        self.dt      = dt
        self.T       = T
        self.N       = N
        self.wE      = wE
        self.gI      = gI
        self.gD      = gD
        self.sigmaE  = sigmaE
        self.sigmaN  = sigmaN
        self.leakN   = leakN
        self.sigmaD  = sigmaD
        self.wD1     = wD1
        self.muD1    = muD1 * N
        self.dV1     = dV1
        self.wD2     = wD2
        self.muD2    = muD1 * N
        self.dV2     = dV2
        self.u0      = np.copy(u0)
        self.mapping = np.copy(mapping)
    
    def _compute_weights(self):
        '''convenience function: compute excitatory weights'''
        ## Preallocate space.
        weights = np.zeros((self.N, self.N))
        
        ## Compute weights along first track.
        for i in np.arange(self.N-1):
            for j in np.arange(i+1,self.N):
                delta = np.abs(i-j)
                weights[i,j] += np.exp( -delta**2 / (2*self.sigmaE**2) ) / self.sigmaE
                weights[j,i] += np.exp( -delta**2 / (2*self.sigmaE**2) ) / self.sigmaE
                
        ## Compute weights along second track.
        ix = np.argsort(self.mapping)
        for i in np.arange(self.N-1):
            for j in np.arange(i+1,self.N):
                delta = np.abs(ix[i] - ix[j])
                weights[i,j] += np.exp( -delta**2 / (2*self.sigmaE**2) ) / self.sigmaE
                weights[j,i] += np.exp( -delta**2 / (2*self.sigmaE**2) ) / self.sigmaE
        
        ## Store.
        self.weights = weights
        
    def _update_drive(self):
        '''convenience function: update drive dynamics'''
        
        ## Update drive position along track 1.
        self.muD1 += self.dV1 * self.dt
        if self.muD1 > self.N - 2 * self.sigmaE: self.dV1 = -self.dV1
        elif self.muD1 < 2 * self.sigmaE: self.dV1 = -self.dV1
            
        ## Update external drive along track 1.
        eD1 = self.wD1 * np.exp( -( np.arange(1,self.N+1) - self.muD1)**2 / (2*self.sigmaD ** 2) )
            
        ## Update drive position along track 2.
        self.muD2 += self.dV2 * self.dt
        if self.muD2 > self.N - 2 * self.sigmaE: self.dV2 = -self.dV2
        elif self.muD2 < 2 * self.sigmaE: self.dV2 = -self.dV2
            
        ## Update external drive along track 2.
        eD2 = self.wD2 * np.exp( -( np.arange(1,self.N+1) - self.muD2)**2 / (2*self.sigmaD ** 2) )
        eD2 = eD2[np.argsort(self.mapping)] # Re-sort.
        
        return eD1, eD2
        
    def _compute_dudt(self, u, r, leak, eD1, eD2):
        '''convenience function: compute du/dt'''
        return -leak * u - self.gI*np.sum(r) + self.wE*self.weights.dot(r) - \
                self.sigmaN * np.random.normal(size=u.size)*np.sqrt(self.dt) + self.gD + eD1 + eD2 
        
    def _submit_gD(self, text):
        self.gD = float(text)
        
    def _submit_gI(self, text):
        self.gI = float(text)
        
    def _submit_wE(self, text):
        self.wE = float(text)
        
    def _submit_leakN(self, text):
        self.leakN = float(text)
    
    def _submit_sigmaN(self, text):
        self.sigmaN = float(text)
            
    def _submit_muD1(self, text):
        self.muD1 = float(text)
                
    def _submit_dV1(self, text):
        self.dV1 = float(text)
        
    def _submit_wD1(self, text):
        self.wD1 = float(text)
        
    def _submit_muD2(self, text):
        self.muD2 = float(text)
                
    def _submit_dV2(self, text):
        self.dV2 = float(text)
        
    def _submit_wD2(self, text):
        self.wD2 = float(text)
        
    def _initialize_canvas(self):
        
        ## Initialize canvas.
        fig = plt.figure(figsize=(16,8))
        
        ## Initialize axes.
        ax1 = plt.subplot2grid((4,2),(0,0),rowspan=3)
        ax2 = plt.subplot2grid((4,2),(3,0))
        ax3 = plt.subplot2grid((4,2),(0,1),rowspan=3)
        ax4 = plt.subplot2grid((4,2),(3,1))
        plt.subplots_adjust(left=0.05, right=0.80, top=0.925, bottom=0.075, hspace=0.35, wspace=0.2)
        
        ## Define buttons.
        x, xw, yw = 0.90, 0.08, 0.04
        
        sigmaN_text = TextBox(plt.axes([x,0.20,xw,yw]), r'$\sigma$ Noise', initial=str(self.sigmaN))
        sigmaN_text.on_submit(self._submit_sigmaN)
        
        gI_text = TextBox(plt.axes([x,0.25,xw,yw]), 'gI', initial=str(self.gI))
        gI_text.on_submit(self._submit_gI)
        
        wE_text = TextBox(plt.axes([x,0.30,xw,yw]), 'wE', initial=str(self.wE))
        wE_text.on_submit(self._submit_wE)
        
        gD_text = TextBox(plt.axes([x,0.35,xw,yw]), 'Global Drive', initial=str(self.gD))
        gD_text.on_submit(self._submit_gD)
        
        leakN_text = TextBox(plt.axes([x,0.40,xw,yw]), 'Leak Noise', initial=str(self.leakN))
        leakN_text.on_submit(self._submit_leakN)
        
        muD2_text = TextBox(plt.axes([x,0.50,xw,yw]), 'Drive Position', initial=str(self.muD2))
        muD2_text.on_submit(self._submit_muD2)
        
        dV2_text = TextBox(plt.axes([x,0.55,xw,yw]), 'Drive Speed', initial=str(self.dV2))
        dV2_text.on_submit(self._submit_dV2)
        
        wD2_text = TextBox(plt.axes([x,0.60,xw,yw]), 'Drive Strength', initial=str(self.wD2))
        wD2_text.on_submit(self._submit_wD2)
        
        muD1_text = TextBox(plt.axes([x,0.70,xw,yw]), 'Drive Position', initial=str(self.muD1))
        muD1_text.on_submit(self._submit_muD1)
        
        dV1_text = TextBox(plt.axes([x,0.75,xw,yw]), 'Drive Speed', initial=str(self.dV1))
        dV1_text.on_submit(self._submit_dV1)
        
        wD1_text = TextBox(plt.axes([x,0.80,xw,yw]), 'Drive Strength', initial=str(self.wD1))
        wD1_text.on_submit(self._submit_wD1)
        
        return [fig, ax1, ax2, ax3, ax4, sigmaN_text, gI_text, wE_text, gD_text, leakN_text, 
                muD1_text, dV1_text, wD1_text, muD2_text, dV2_text, wD2_text]
        
    def run_simulation(self, plot=False, sleep=0.01):
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Define parameters.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
        ## Store first time.
        t = 0 
        
        ## Preallocate space.
        r = np.zeros(self.N)                     # Firing rate.
        if np.any(self.u0): u = self.u0.copy()   # Membrane potential.
        else: u = np.zeros_like(r)
        assert u.size == r.size
        
        ## Compute leaks.
        leak = np.ones_like(r) + self.leakN * np.random.normal(size=r.size); 
        leak[leak<0] = 0
        
        ## Re-map neurons of track 2 with respect to track 1.
        if not np.any(self.mapping): self.mapping = np.random.choice(np.arange(self.N), self.N, replace=False)
        assert self.mapping.size == self.N
        sort_ix = np.argsort(self.mapping)
        
        ## Compute weights.
        self._compute_weights()
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Initialize figure.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
        if plot:
            
            ## Initialize canvas. 
            ## Unfortunately we need to pass all of the text boxes
            ## or else they fail to work. Sorry for the clunky code.
            figure_elements = self._initialize_canvas()
            fig, ax1, ax2, ax3, ax4 = figure_elements[:5] 
            
            ## Plot initial firing rates.
            r1_line, = ax1.plot(r, color='#1f77b4')
            r2_line, = ax3.plot(r[sort_ix], color='#2ca02c')
            ax1.set(xlim=(0,r.size), ylim=(-0.05,1.05))
            ax3.set(xlim=(0,r.size), ylim=(-0.05,1.05))
            
            ## Plot initial driving dynamics.
            eD1, eD2 = self._update_drive()
            eD1_line, = ax2.plot(eD1, color='#1f77b4')
            eD2_line, = ax4.plot(eD2, color='#2ca02c')
            ax2.set(xlim=(0,eD1.size))
            ax4.set(xlim=(0,eD2.size))
            
            fig.canvas.draw()
            fig.canvas.flush_events()
            
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Main loop.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        while t < self.T:
            
            ## Break loop if figure closed.
            if plot and not plt.fignum_exists(fig.number): 
                plt.close('all')
                break

            ## Update time.
            t += self.dt

            ## Update driving dynamics.
            eD1, eD2 = self._update_drive()
            
            ## Compute du/dt.
            dudt = self._compute_dudt(u, r, leak, eD1, eD2)

            ## Estimate u with Euler's method.
            u += dudt * self.dt

            ## Update firing rate.
            r = firing_rate(u)

            ## Update time.
            t += self.dt
            
            ## Update plot.
            if plot:                
                
                ## Update time.
                plt.title('t = %0.2f' %t, x=0.5, y=0.95, fontsize=18)
                
                ## Update firing rate.
                r1_line.set_ydata(r)
                r2_line.set_ydata(r[self.mapping])
                
                ## Update driving dynamics.
                eD = eD1 + eD2
                eD1_line.set_ydata(eD)
                eD2_line.set_ydata(eD[self.mapping])
                ax2.set(ylim=(eD.min()-0.05, eD.max()+0.05))
                ax4.set(ylim=(eD.min()-0.05, eD.max()+0.05))
                
                fig.canvas.draw()
                fig.canvas.flush_events()
                time.sleep(sleep)
                
        return r, r[self.mapping]