import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the Kuramoto model parameters
N = 10  # Number of oscillators
K = 0.0001  # Coupling strength
w0 = 10.0  # Natural frequency

# Generate random initial phases between 0 and 2*pi
theta = np.random.uniform(low=0.0, high=2*np.pi, size=N)

def kuramoto(theta):
    dtheta = w0 + K/N * np.sum(np.sin(theta - theta[:, np.newaxis]), axis=1)
    theta = (theta + dtheta*dt) % (2*np.pi)
    return theta

# Define the simulation time and time step
t_start = 0.0
t_end = 1000.0
dt = 10
t = np.arange(t_start, t_end, dt)

# Initialize the position and velocity of the oscillators
x = np.cos(theta)
y = np.sin(theta)
vx = np.zeros_like(theta)
vy = np.zeros_like(theta)

# Define the finite difference method function
def finite_diff(x, y, vx, vy, dt):
    ax = -K/N * np.sum(np.sin(x - x[:, np.newaxis]), axis=1)
    ay = K/N * np.sum(np.cos(y - y[:, np.newaxis]), axis=1)
    vx += ax * dt
    vy += ay * dt
    x += vx * dt
    y += vy * dt
    return x, y, vx, vy

# Define the animation function
def animate(i):
    global x, y, vx, vy
    x, y, vx, vy = finite_diff(x, y, vx, vy, dt)
    line.set_data(x, y)
    ax.relim()
    ax.autoscale_view()
    return line,

# Initialize the plot
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
#ax.set_aspect('equal')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Coupled Oscillators')
line, = ax.plot(x, y, 'bo')

# Create the animation
anim = FuncAnimation(fig, animate, frames=int((t_end-t_start)/dt), interval=10, blit=True)

plt.show()
