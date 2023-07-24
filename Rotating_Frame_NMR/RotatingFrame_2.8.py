import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import numpy as np

# Set parameters
key, init = 0, 0
B0 = 1
B1 = 0.5
w0 = 250
w0 = w0/1000
w1 = w0
x, y, z = 1, 1, 1

# Create the figure and subplots
fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
ax.set_xlabel('z')
ax.set_ylabel('x')
ax.set_zlabel('y')
ax.set_xlim([-max(1,1), max(1, 1)])
ax.set_ylim([-max(1.3, 1), max(1.3, 1)])
ax.set_zlim([-max(1, 1), max(1, 1)])
plt.xticks([])
plt.yticks([])
ax.zaxis.set_tick_params(labelsize=0, labelcolor='w')
plt.gca().invert_yaxis()

# Define the arrow properties
arrow_start = (0, 0, 0)
arrow_length = 1  # Adjust the length of the arrow

# Initialize the quiver plot
magnetization_vector = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
               0, 0, 0, length=arrow_length, arrow_length_ratio=0.3, color='r')
B0_vector = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
               1, 0, 0, length=B0, arrow_length_ratio=0.2, color='g')
#B1_vector = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
#               0, 1, 0, length=2*B1, arrow_length_ratio=0.2, color='b')
B1_vector_var = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
               0, 0, 0, length=2*B1, arrow_length_ratio=0.2, color='b')
B1_vector_L = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
               0, 0, 0, length=B1, arrow_length_ratio=0.2, color='teal')
B1_vector_R = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
               0, 0, 0, length=B1, arrow_length_ratio=0.2, color='aqua')

# Line plot for the arrow positions
line_plot, = ax.plot([], [], [], linestyle='dotted', color='gray')

# Initialize the arrow positions
arrow_positions = []

# Animation update function for the 3D plot
def update(time):
    global magnetization_vector, B1_vector, B1_vector_var, B1_vector_L, B1_vector_R, line_plot, arrow_positions, key, init
    
    t, Bt = time*w0, time*w0  # Scaling factor for animation
    magnetization_offset = 0
    B1_offset = -1.25
    
    if t <= 4*np.pi: # Fixed B0; no B1. Magnetization precesses B0.
        x, Bx = np.sin(t+magnetization_offset), 0
        y, By = np.cos(t+magnetization_offset), 0
        z, Bz = 1, 0
        arrow_direction, B_arrow_direction = (z, y, x), (Bz, By, Bx)
        magnetization_vector.remove()
        magnetization_vector = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
                               arrow_direction[0], arrow_direction[1], arrow_direction[2],
                               length=arrow_length, arrow_length_ratio=0.3, color='r')
        B0_vector = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
               1, 0, 0, length=B0, arrow_length_ratio=0.2, color='g')

    elif t <= 8*np.pi: # Fixed B0; fixed B1. Magnetization precesses B0 and B1.
        x, Bx = np.sin(t+magnetization_offset), 0
        y, By = np.cos(t+magnetization_offset), 0
        z, Bz = np.sin(t+magnetization_offset) + np.cos(t+magnetization_offset), 0
        arrow_direction, B_arrow_direction = (z, y, x), (Bz, By, Bx)
        magnetization_vector.remove()
        magnetization_vector = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
                               arrow_direction[0], arrow_direction[1], arrow_direction[2],
                               length=arrow_length, arrow_length_ratio=0.3, color='r')
        try:
            B1_vector.remove()
        except:
            pass
        B1_vector = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
               0, 1, 0, length=2*B1, arrow_length_ratio=0.2, color='b')

    elif t <= 12*np.pi: # Fixed B0; oscillating B1.
        if init == 0:
            B1_vector.remove()
            init += 1
        x, Bx = np.sin(t+magnetization_offset), 0
        y, By = np.cos(t+magnetization_offset), np.cos(Bt+B1_offset)
        z, Bz = np.sin(t+magnetization_offset) + np.cos(t), 0
        arrow_direction, B_arrow_direction = (z, y, x), (Bz, By, Bx)
        magnetization_vector.remove()
        try:
            B1_vector_var.remove()
        except:
            pass
        B1_vector_var = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
               0, B_arrow_direction[1], 0, length=2*B1, arrow_length_ratio=0.2, color='b')
        magnetization_vector = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
                               arrow_direction[0], arrow_direction[1], arrow_direction[2],
                               length=arrow_length, arrow_length_ratio=0.3, color='r')

    elif t <= 16*np.pi: # Fixed B0; oscillating B1 components with B1.
        x, Bx = np.sin(t+magnetization_offset), np.sin(Bt+B1_offset)
        y, By = np.cos(t+magnetization_offset), np.cos(Bt+B1_offset)
        z, Bz = np.sin(t+magnetization_offset) + np.cos(t+magnetization_offset), 0
        arrow_direction, B_arrow_direction = (z, y, x), (Bz, By, Bx)
        magnetization_vector.remove()
        try:
            B1_vector_var.remove()
            B1_vector_L.remove()
            B1_vector_R.remove()
        except:
            pass
        magnetization_vector = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
                               arrow_direction[0], arrow_direction[1], arrow_direction[2],
                               length=arrow_length, arrow_length_ratio=0.3, color='r')
        B1_vector_var = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
               0, B_arrow_direction[1], 0, length=2*B1, arrow_length_ratio=0.2, color='b')
        B1_vector_L = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
               0, B_arrow_direction[1], B_arrow_direction[2], length=B1, arrow_length_ratio=0.2, color='teal')
        B1_vector_R = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
               0, B_arrow_direction[1], -B_arrow_direction[2], length=B1, arrow_length_ratio=0.2, color='aqua')
    
    else: # Fixed B0; oscillating B1 components with B1.
        if key == 0:
            key += 1
        x, Bx = np.sin(t+magnetization_offset), np.sin(Bt+B1_offset)
        y, By = np.cos(t+magnetization_offset), np.cos(Bt+B1_offset)
        z, Bz = np.sin(t+magnetization_offset) + np.cos(t+magnetization_offset), 0
        arrow_direction, B_arrow_direction = (z, y, x), (Bz, By, Bx)
        magnetization_vector.remove()
        try:
            B1_vector_var.remove()
        except:
            pass
        try:
            B1_vector_L.remove()
            B1_vector_R.remove()
        except:
            pass
        magnetization_vector = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
                               arrow_direction[0], arrow_direction[1], arrow_direction[2],
                               length=arrow_length, arrow_length_ratio=0.3, color='r')
        B1_vector_L = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
               0, B_arrow_direction[1], B_arrow_direction[2], length=B1, arrow_length_ratio=0.2, color='teal')
        B1_vector_R = ax.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
               0, B_arrow_direction[1], -B_arrow_direction[2], length=B1, arrow_length_ratio=0.2, color='aqua')
       
    # Update the arrow positions
    arrow_positions.append(arrow_direction)
    
    # Update the line plot with arrow positions
    arrow_positions_x = [pos[0] for pos in arrow_positions]
    arrow_positions_y = [pos[1] for pos in arrow_positions]
    arrow_positions_z = [pos[2] for pos in arrow_positions]
    
    line_plot.set_data(arrow_positions_x, arrow_positions_y)
    line_plot.set_3d_properties(arrow_positions_z)
    
    #ax.view_init(elev=20, azim=120, roll=0)
    
    return magnetization_vector, line_plot

# Rotate the axes and update function for the rotation animation
def rotate(angle):
    global key, init
    elev = azim = roll = 0
    angle = angle*w0*57.2975
    if key == 0:
        angle = angle
        ax.view_init(elev=20, azim=60)
        plt.title('Azimuth: %d°' % angle)
    elif key == 1:
        angle = angle
        ax.view_init(elev=-angle, azim=90, roll=0)
        plt.title('Azimuth: %d°' % angle)
    #else:
    #    if angle < 1:
    #        ax.view_init(elev=0, azim=angle)
    #        plt.title('Azimuth: %d°' % angle)

# Create the animation for the 3D plot
animation = FuncAnimation(fig, update, frames=360, interval=10)

# Subplot for the rotation animation
ax_rot = fig.add_subplot(122)

# Create the rotation animation
rotation_animation = FuncAnimation(fig, rotate, frames=360, interval=10)
plt.pause(1)

# Show the plot
plt.show()
