import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the Kuramoto model parameters
N = 20  # Number of oscillators
K = 1.0  # Coupling strength
w0 = 1.0  # Natural frequency

# Generate random initial phases between 0 and 2*pi
theta = np.random.uniform(low=0.0, high=2*np.pi, size=N)

# Define the Kuramoto model function
def kuramoto(theta, t):
    dtheta = w0 + K/N * np.sum(np.sin(theta - theta[:, np.newaxis]), axis=1)
    return dtheta

# Define the simulation time
t_start = 0.0
t_end = 10.0
dt = 0.1
t = np.arange(t_start, t_end, dt)

# Integrate the Kuramoto model
from scipy.integrate import odeint
theta_sol = odeint(kuramoto, theta, t)
theta_sol_list, theta_sol_sublist = [], []
biglist = []
for i in range(len(theta_sol)):
    for j in range(len(theta_sol[i])):
        entry = theta_sol[i][j] % (2*np.pi)
        theta_sol_sublist.append(entry)
        if len(theta_sol_sublist) == N:
            theta_sol_list.append(theta_sol_sublist.copy())
            theta_sol_sublist = []  # create a new list here
theta_sol = np.array(theta_sol_list)

# Set up the plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 2*np.pi)
ax.set_xlabel('Time')
ax.set_ylabel('Phase')
ax.set_title('Kuramoto model')

# Initialize the line objects
lines = [ax.plot([], [], lw=2)[0] for i in range(N)]

# Define the update function for the animation
def update(frame):
    for i in range(N):
        lines[i].set_data(t[:frame], theta_sol[:frame, i])
    return lines

# Create the animation object
ani = animation.FuncAnimation(fig, update, frames=len(t), blit=True, interval=16)

# Show the animation
plt.show()
