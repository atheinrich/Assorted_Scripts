import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the Kuramoto model parameters
N = 20  # Number of oscillators
K = 1.0  # Coupling strength
w0 = 1.0  # Natural frequency

# Generate random initial phases and magnitudes between 0 and 2*pi and 0 and 1, respectively
theta = np.random.uniform(low=0.0, high=2*np.pi, size=N)
r = np.random.uniform(low=0.0, high=1.0, size=N)

# Define the Kuramoto model function
def kuramoto(theta_r, t):
    theta = theta_r[:N]
    r = theta_r[N:]
    dtheta = w0 + K/N * np.sum(r * np.sin(theta - theta[:, np.newaxis]), axis=1)
    dr = -K/N * np.sum(r * np.cos(theta - theta[:, np.newaxis]), axis=1)
    return np.concatenate((dtheta, dr))

# Define the simulation time
t_start = 0.0
t_end = 10.0
dt = 0.1
t = np.arange(t_start, t_end, dt)

# Integrate the Kuramoto model
from scipy.integrate import odeint
theta_r_sol = odeint(kuramoto, np.concatenate((theta, r)), t)
theta_sol_list, r_sol_list = [], []
theta_sol_sublist, r_sol_sublist = [], []
for i in range(len(theta_r_sol)):
    for j in range(len(theta_r_sol[i])):
        entry = theta_r_sol[i][j]
        if j < N:
            entry = entry % (2*np.pi)
            theta_sol_sublist.append(entry)
        else:
            r_sol_sublist.append(entry)
        if len(theta_sol_sublist) == N and len(r_sol_sublist) == N:
            theta_sol_list.append(theta_sol_sublist.copy())
            theta_sol_sublist = []  # create a new list here
            r_sol_list.append(r_sol_sublist.copy())
            r_sol_sublist = []  # create a new list here
theta_sol = np.array(theta_sol_list)
r_sol = np.array(r_sol_list)

# Convert polar coordinates to Cartesian coordinates
x_sol = r_sol * np.cos(theta_sol)
y_sol = r_sol * np.sin(theta_sol)

# Set up the plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_xlabel('Real Component')
ax.set_ylabel('Imaginary Component')
ax.set_title('Kuramoto model')

# Initialize the line objects
lines = [ax.plot([], [], lw=2)[0] for i in range(N)]

# Define the update function for the animation
def update(frame):
    for i in range(N):
        lines[i].set_data(x_sol[:frame, i], y_sol[:frame, i])
    return lines

# Create the animation object
ani = animation.FuncAnimation(fig, update, frames=len(t), blit=True, interval=16)

# Show the animation
plt.show()
