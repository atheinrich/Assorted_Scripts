###########################################################################################################################
# Plots angular momentum addition
print("###############################################################################")
print("Welcome!")
print("This code illustrates the addition of angular momentum.")
print("This goal is to find vectors whose sum satisfies quantum mechanics:")
print("\t J in {|j1 - j2|, |j1 - j2 + 1|, |j1 - j2 + 2|, ..., |j1 + j2|}")
print("The blue vector is fixed, and the red vector is rotated.")
print("Each grey vector is the sum of the blue vector and a red vector.")
print("###############################################################################\n")
###########################################################################################################################

###########################################################################################################################
# Imports
import numpy as np
import matplotlib.pyplot as plt

###########################################################################################################################
# Parameters and data containers
## Set vector lengths
fixed_vector_norm, rotated_vector_norm = 4, 3
max_norm, min_norm = abs(fixed_vector_norm + rotated_vector_norm), abs(fixed_vector_norm - rotated_vector_norm)

## Set precision
precision_index = 4
tolerance       = 10 * 10**(-precision_index)
num_vectors     = 10**(precision_index)
angle_increment = np.pi / num_vectors

## Other
int_list = []

###########################################################################################################################
# Definitions
def plot_rotated_vectors():
    global fixed_vector

    # Plot initial position
    unit_vector = np.array([rotated_vector_norm, 0])
    plt.quiver(0, 0, unit_vector[0], unit_vector[1], angles='xy', scale_units='xy', scale=1, color='r')

    # Plot rotated vectors satisfying desired criteria
    for i in range(num_vectors):
    
        # Create rotated vector
        angle = i * angle_increment
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                    [np.sin(angle), np.cos(angle)]])
        rotated_vector = np.dot(rotation_matrix, unit_vector)
        
        # Check if criteria is satisfied
        for i in range(max_norm):
            new_vector = fixed_vector + rotated_vector
            new_norm = np.linalg.norm(new_vector)
            
            # Check if new norm is related to the max norm by the subtraction of an integer
            if np.isclose(new_norm, max_norm-i, atol=tolerance): # returns True if new norm falls within tolerance
                if round(new_norm) not in int_list: # prevents plotting multiple vectors associated with the same integer
                    plt.quiver(0, 0, rotated_vector[0], rotated_vector[1], angles='xy', scale_units='xy', scale=1, color='r')
                    int_list.append(round(new_norm))
                    print(f"angle: {round(angle, 1)} rad\t{round(angle*180/np.pi)}°\t\tnorm: {round(new_norm, 3)}")
                    
                    plt.quiver(-fixed_vector_norm, 0, new_vector[0], new_vector[1], angles='xy', scale_units='xy', scale=1, alpha=0.5)

def main():
    global fixed_vector
    
    print(f"fixed vector norm:\t\t{fixed_vector_norm}\nrotated vector norm:\t\t{rotated_vector_norm}")
    print(f"expected total J:\t\t{list(range(int(abs(fixed_vector_norm - rotated_vector_norm)), int(fixed_vector_norm + rotated_vector_norm) + 1))}\n")
    
    fixed_vector = np.array([fixed_vector_norm, 0]) # sets coordinates for non-rotated vector
    plt.quiver(-fixed_vector_norm, 0, fixed_vector[0], fixed_vector[1], angles='xy', scale_units='xy', scale=1, color='b') #-fixed_vector_norm
    plot_rotated_vectors()

###########################################################################################################################
# Global scripts
main()

plt.xlim(-max_norm, max_norm)
plt.ylim(-max_norm, max_norm)
plt.xlabel('X')
plt.ylabel('Y')
plt.gca().set_aspect('equal', adjustable='box')
plt.title('Unit Vector and Rotated Vectors')
plt.grid()
plt.show()

###########################################################################################################################