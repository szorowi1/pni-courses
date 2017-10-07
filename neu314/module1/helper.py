import numpy as np

def LIF_spike(V0 =-60e-3, dt =  1e-3, t_max = 400e-3, 
              tau= 20e-3, el =-60e-3, i_mean=  25e-3, 
              vr =-70e-3, vth=-50e-3):
    """
    Implements the Leaky Integrate-and-Fire neuron model
    
    Requires no input, but can optionally receive any of
    the model parameters as input to change form the default.
    
    Returns 3 outputs: an array with the time course of the 
    simulation, an array with the voltage over that time 
    course, and a list with the spike times.
    """
    time = np.arange(0.0,t_max,dt)
    v = np.zeros_like(time)
    v[0] = V0
    spike_times = []
    for j in range(1,len(time)):
        if v[j-1] >= vth:
            v[j] = vr
            spike_times += [time[j]]
        else:
            i=i_mean*np.random.random()
            v[j] = v[j-1] + (el - v[j-1] + i)*dt/tau

    return time, v, spike_times