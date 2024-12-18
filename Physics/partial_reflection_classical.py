##########################################################################################################################################
# Reflection and transmission of a wave packet
print("###############################################################################")
print("Welcome!")
print("This code simulates a Gaussian wavepacket traveling towards a new medium.")
print("The goal is to illustrate reflection and transmission across an interface.")
print("The output is a video.")
print("###############################################################################")
##########################################################################################################################################

##########################################################################################################################################
# Imports
import numpy as np
import matplotlib.pyplot as plt
import cv2 # video output
import os  # open video after creation

##########################################################################################################################################
# Parameters
## Step sizes and total range/duration
L       = 150                  # string length
dx      = 0.1                  # spatial step size
dt      = 0.01                 # temporal step size
t_max   = 100                  # simulation time
x       = np.arange(0, L, dx)  # spatial domain: array([0, dx, 2*2x, ..., L])

## Wave speed in each medium
c1      = 1.0                  # incident/reflected
c2      = 0.5                  # transmitted
c_array = np.ones(len(x)) * c1 # [c1, c1, ..., c1, c1, c1, ..., c1]
c_array[len(x)//2:] = c2       # [c1, c1, ..., c1, c2, c2, ..., c2]

# Initial wave packet
x0      = 30                   # initial position
σ       = 2                    # standard deviation
ψ       = np.exp(-((x - x0) ** 2) / (2 * σ ** 2))
ψ_prev  = np.exp(-((x - x0 + c1 * dt) ** 2) / (2 * σ ** 2))

# Video details
frame_width  = 640
frame_height = 480
out = cv2.VideoWriter('partial_reflection_classical.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (frame_width, frame_height))

##########################################################################################################################################
# Definitions
def main():
    """ Calculates evolution through wave equation.
        np.roll(ψ, n) yields the wavefunction centered on the nth spatial step. """
    
    global ψ, ψ_prev
    
    # Define some parameters for convenience
    t_steps = int(t_max / dt)
    
    # Utilize finite difference method
    for t in range(t_steps):
    
        # Calculate second spatial derivative at current time
        derivative = np.roll(ψ, -1) - 2 * ψ + np.roll(ψ, 1)
        ψ_next = 2*ψ - ψ_prev + (c_array * dt / dx)**2 * derivative
        
        ψ_prev = ψ.copy() # prevents recursive definition
        ψ = ψ_next.copy() # prevents recursive definition

        if t % (t_steps // 100) == 0:
            plot_and_save_frame(ψ, t)

    # Release the video writer
    out.release()
    cv2.destroyAllWindows()
    os.system(f'start partial_reflection_classical.avi')

def plot_and_save_frame(ψ, t):
    """ Plots function at current time and inserts plot as a frame in a video. """
    
    # Plot function
    plt.figure(figsize=(8, 6))
    plt.plot(x, ψ, label=f'Time={t*dt:.2f}')
    plt.xlabel('x')
    plt.ylabel('Displacement')
    plt.ylim([-2, 2])
    plt.legend()
    plt.grid(True)
    plt.title('Wave Packet Simulation')

    # Save plot as image
    plt.savefig('frame.png')
    plt.close()

    # Read the image and write to video
    frame = cv2.imread('frame.png')
    frame = cv2.resize(frame, (frame_width, frame_height))
    out.write(frame)

##########################################################################################################################################
# Global scripts
main()

##########################################################################################################################################