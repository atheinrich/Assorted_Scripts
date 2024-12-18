##############################################################################################################################################################################
##############################################################################################################################################################################
###
### Kuramoto model
###
##############################################################################################################################################################################
##############################################################################################################################################################################

##############################################################################################################################################################################
# Imports
import numpy as np # Generates intervals of numbers and random numbers, calculates sums and trigonometries, constructs and analyzes arrays
import matplotlib.pyplot as plt # Plots numerical results on a graph
import matplotlib.animation as animation # Animates the plot over time
from scipy.integrate import odeint # Solves differential equations
import time # Uses time.sleep(t) for troubleshooting

##############################################################################################################################################################################
# Parameters and initial conditions
N_oscillators = 20  # Number of oscillators in positive integers
K_strength = 1.0  # Coupling strength in g⸱s⁻²
ω0_freq = 1.0  # Natural frequency in radians

θ_initial = np.random.uniform(low=0.0, high=2*np.pi, size=N_oscillators) # Generates random initial phases between 0 and 2π
r_initial = np.random.uniform(low=0.1, high=1.0, size=N_oscillators) # Generate random initial magnitudes between 0.1 and 1.0

t_initial = 0.0 # Sets the simulation time
t_final = 100.0
dt = 0.1
t = np.arange(t_initial, t_final, dt)

##############################################################################################################################################################################
# Definitions
def kuramoto(z, t):
    """ Models coupling with the form [dr,dθ]=[k∙Σ(rₒ∙sin(θₒ-θ))/n,ωₒ+k∙Σ(rₒ∙sin(θₒ-θ))/n]. """
    θ_initial = z[:N_oscillators] # Extracts phases from state vector as arrays with N_oscillators elements
    r_initial = z[N_oscillators:] # Extracts magnitudes from state vector as arrays with N_oscillators elements
    dθ = ω0_freq + K_strength/N_oscillators * np.sum(r_initial[:, np.newaxis] * np.sin(θ_initial - θ_initial[:, np.newaxis]), axis=1) # Calculates the change in phase
    dr = K_strength/N_oscillators * np.sum(r_initial[:, np.newaxis] * np.sin(θ_initial - θ_initial[:, np.newaxis]), axis=1) # Calculates the change in magnitude
    return np.concatenate((dθ, dr)) # Returns the change in phase and magnitude as a single array

def update(frame):
    """ Updates the graph over time. """
    for i in range(N_oscillators):
        x = np.cos(kuramoto_θ[frame, i]) * kuramoto_r[frame, i]
        y = np.sin(kuramoto_θ[frame, i]) * kuramoto_r[frame, i]
        lines[i].set_data([0, x], [0, y]) # Update the line endpoints
        points[i].set_data(x, y) # Update the point position
    
    # Update the sum of magnitudes line
    sum_magnitudes = np.sum(kuramoto_r[frame])
    sum_line.set_data(np.arange(frame + 1), np.full(frame + 1, sum_magnitudes))
    
    # Check if the x and y limits need to be adjusted
    x = np.cos(kuramoto_θ[frame]) * kuramoto_r[frame]
    y = np.sin(kuramoto_θ[frame]) * kuramoto_r[frame]
    xlim = graph[0].get_xlim()
    ylim = graph[0].get_ylim()
    x_min = np.min(x)
    x_max = np.max(x)
    y_min = np.min(y)
    y_max = np.max(y)
    x_expand = False
    y_expand = False
    if x_min < xlim[0]:
        graph[0].set_xlim(x_min * 2, xlim[1] * 2)
        x_expand = True
    elif x_max > xlim[1]:
        graph[0].set_xlim(xlim[0] * 2, x_max * 2)
        x_expand = True
        
    if y_min < ylim[0]:
        graph[0].set_ylim(y_min * 2, ylim[1] * 2)
        y_expand = True
    elif y_max > ylim[1]:
        graph[0].set_ylim(ylim[0] * 2, y_max * 2)
        y_expand = True
        
    # Redraw the plot if the x or y limits were adjusted
    if x_expand or y_expand:
        main_canvas.canvas.draw()
    return lines + points + [sum_line]

##############################################################################################################################################################################
# Evaluation and plot initialization
initial_θ_r_array = np.concatenate((θ_initial, r_initial)) # Sets the phase and magnitude as a single array
kuramoto_θ_r_array = odeint(kuramoto, initial_θ_r_array, t) # Runs Kuramoto model for phases and amplitudes then outputs a solution array
kuramoto_θ, kuramoto_r = kuramoto_θ_r_array[:, :N_oscillators], kuramoto_θ_r_array[:, N_oscillators:] # Extract phases and magnitudes from the solution array

main_canvas, graph = plt.subplots(figsize=(12, 6), ncols=2, gridspec_kw={'width_ratios': [3, 1]}) # Initializes the canvas and graph structure
graph[0].set_xlim(-5, 5) # Initializes the x-axis for the primary graph
graph[0].set_ylim(-5, 5) # Initializes the y-axis for the primary graph
graph[0].set_aspect('equal') # Sets the aspect ratio for the primary graph
graph[0].set_title('Kuramoto model')
graph[1].set_xlim(0, 1) # Initializes the x-axis for the secondary graph
graph[1].set_ylim(0, 100) # Initializes the y-axis for the secondary graph
graph[1].set_title('Total magnitude')

lines = [graph[0].plot([], [], lw=2)[0] for i in range(N_oscillators)]
points = [graph[0].plot([], [], 'o', markersize=5)[0] for i in range(N_oscillators)]
sum_line, = graph[1].plot([], [], lw=2)

##############################################################################################################################################################################
# Main
ani = animation.FuncAnimation(main_canvas, update, frames=len(t), blit=True, interval=16) # Creates the animation object
plt.show() # Plots the data

##############################################################################################################################################################################
