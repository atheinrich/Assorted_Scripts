##################################################################################
#
# Spherical harmonics
# Expands products of spherical harmonics in the basis of spherical harmonics.
#
##################################################################################

##################################################################################
# Imports
import numpy as np # np.math.factorial(n)
from scipy.special import sph_harm # sph_harm(j, m, ϕ, θ, out=array)

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, colors
from matplotlib.colors import Normalize

##################################################################################
# Parameters and data containers
## Set indices of spherical harmonics to be multiplied
j1, m1 = 1, -1
j2, m2 = 1, -1

## Set domain in spherical coordinates
theta = np.linspace(0, np.pi, 100)
phi = np.linspace(0, 2*np.pi, 100)
theta, phi = np.meshgrid(theta, phi)

## Convert domain to Cartesian coordinates
x = np.sin(theta) * np.cos(phi)
y = np.sin(theta) * np.sin(phi)
z = np.cos(theta)

##################################################################################
# Definitions
def main():
    # Calculate the product of two spherical harmonics using scipy
    product_direct = scipy_product()
    
    # Calculate coefficients in the expansion equation
    jm_list = Wigner_3j_search() # looks for nonzero Wigner 3j symbols; [[j3, m3], ...]
    coefficients_list = expansion_coefficients(jm_list) # calculates expansion coefficient for each nonzero Wigner 3j symbol
    
    # Calculate full spherical harmonic expansion
    product_expansion = Wigner_expansion(coefficients_list) # returns linear combination of spherical harmonics
    
    # Calculate difference between scipy result and Wigner expansion result for fidelity check
    product_difference =  difference_harmonic(coefficients_list)
    
    # Calculate each term in the expansion individually
    expansion_term_list = expansion_terms(coefficients_list)
    
    # Plot the results
    plot_results(product_direct, product_expansion, product_difference, expansion_term_list)

def scipy_product():
    global product_direct
    
    product_direct = sph_harm(m1, j1, phi, theta) * sph_harm(m2, j2, phi, theta)
    product_direct = product_direct.real
    norm = Normalize(vmin=product_direct.min(), vmax=product_direct.max()) # normalize for plotting
    return norm(product_direct)

def Wigner_3j_search():
    """ Looks for nonzero Wigner 3j symbols and returns a list of the respective j3 and m3 values. """
    
    jm_list_cache = []
    for j3 in range(abs(j1-j2), j1+j2+1): # verifies that |j1-j2| ≤ j3 ≤ |j1+j2|
        for m3 in range(-j3, j3+1):       # verifies that -j3 ≤ m3 ≤ j3
            if m1+m2+m3 == 0:             # verifies that m3 = -(m1+m2)
                if type(j1+j2+j3) == int: # verifies that j1+j2+j2 is an integer
                    jm_list_cache.append([j3, m3])
    return jm_list_cache

def Wigner_3j_calc(j1, j2, j3, m1, m2, m3):
    """ Calculates a single, nonzero Wigner 3j symbol and returns the result. """
    
    # Calculate some parameters for convenience
    j          = j1+j2+j3
    a1, a2, a3 = j1-m1, j2-m2, j3-m3
    b1, b2, b3 = j1+m1, j2+m2, j3+m3
    c1, c2, c3 = j-2*j1, j-2*j2, j-2*j3
    d1, d2, d3 = j1-j2-m3, j2-j3-m1, j3-j1-m2
    k = max(-d3, 0, d2)
    l = min(a1, b2, c3)

    # Calculate the coefficient outside of the products and summations
    term_1 = (-1)**d1 / np.math.factorial(j+1)**(1/2)
    
    # Calculate the products
    term_2 = (np.math.factorial(a1) * np.math.factorial(b1) * np.math.factorial(c1))**(1/2)
    term_3 = (np.math.factorial(a2) * np.math.factorial(b2) * np.math.factorial(c2))**(1/2)
    term_4 = (np.math.factorial(a3) * np.math.factorial(b3) * np.math.factorial(c3))**(1/2)
    
    # Calculate the summations
    term_5 = 0
    for u in range(k, l+1):
        term_5_i  = (-1)**u / np.math.factorial(u)
        term_5_i /= np.math.factorial(a1-u) * np.math.factorial(b2-u) * np.math.factorial(c3-u)
        term_5_i /= np.math.factorial(u-d2) * np.math.factorial(u+d3)
        term_5   += term_5_i
    
    # Exports result
    return term_1 * term_2 * term_3 * term_4 * term_5

def expansion_coefficients(jm_list):
    """ Calculates and returns the expansion coefficients as a list of lists: [[j3, m3, coefficient], ...]. 
        Each coefficient already includes the square root normalization factor that is typically outside of the summation. 
        Does not include the spherical harmonic associated with each j3 value. 
        Note that the m3 found in Wigner_3j_search must be -γ in the expansion, so this function returns γ=-m3. """
    
    # Initialize calculation
    coefficients_cache = []
    expansion_normalization = ((2*j1+1)*(2*j2+1)/(4*np.pi))**(1/2)
    for u in range(len(jm_list)):
    
        # Calculate square root normalization factor outside of summation
        expansion_parity = (-1)**(-jm_list[u][1]) * (2*jm_list[u][0]+1)**(1/2)
        
        # Calculate each 3j symbol
        Wigner_calc_1 = Wigner_3j_calc(j1, j2, jm_list[u][0], m1, m2, jm_list[u][1]) # m3=m3
        Wigner_calc_2 = Wigner_3j_calc(j1, j2, jm_list[u][0], 0, 0, 0)               # m1=m2=m3=0
        
        # Append coefficient to list for export
        coefficient_cache = expansion_normalization * expansion_parity * Wigner_calc_1 * Wigner_calc_2
        coefficients_cache.append([jm_list[u][0], -jm_list[u][1], coefficient_cache])
    
    # Export data
    return coefficients_cache

def Wigner_expansion(coefficients_list):
    """ Takes a list [[j3, m3, coefficient], ...] and calculates the linear combination, including the spherical harmonics. """
    
    product_expansion = 0
    for i in range(len(coefficients_list)):
        product_expansion += coefficients_list[i][2] * sph_harm(coefficients_list[i][1], coefficients_list[i][0], phi, theta).real
    norm = Normalize(vmin=product_expansion.min(), vmax=product_expansion.max()) # normalize for plotting
    return norm(product_expansion)

def difference_harmonic(coefficients_list):

    product_difference = 0
    for i in range(len(coefficients_list)):
        product_difference += coefficients_list[i][2] * sph_harm(coefficients_list[i][1], coefficients_list[i][0], phi, theta)
    product_difference -= sph_harm(m1, j1, phi, theta) * sph_harm(m2, j2, phi, theta)
    product_difference = product_difference.real
    norm = Normalize(vmin=product_difference.min(), vmax=product_difference.max()) # normalize for plotting
    return norm(product_difference)

def expansion_terms(coefficients_list):

    terms_cache = []
    for u in range(len(coefficients_list)):
        single_expansion = coefficients_list[u][2] * sph_harm(coefficients_list[u][1], coefficients_list[u][0], phi, theta).real
        norm = Normalize(vmin=single_expansion.min(), vmax=single_expansion.max()) # normalize for plotting
        terms_cache.append([coefficients_list[u][0], coefficients_list[u][1], coefficients_list[u][2], norm(single_expansion)])
    return terms_cache

def plot_results(product_direct, product_expansion, product_difference, expansion_term_list):
    # Initialize plots
    canvas = plt.figure(figsize=(12, 5))
    if len(expansion_term_list) < 3: grid = GridSpec(nrows=2, ncols=3, wspace=1)
    else:                            grid = GridSpec(nrows=2, ncols=len(expansion_term_list), wspace=1)

    # Plot product directly
    graph_1 = canvas.add_subplot(grid[0,0], projection='3d')
    graph_1.plot_surface(x, y, z,  rstride=1, cstride=1, facecolors=cm.seismic(product_direct))
    graph_1.set_axis_off()
    graph_1.set_title(f"$Y_{{{j1}}}^{{{m1}}}$∙$Y_{{{j2}}}^{{{m2}}}$")
    
    # Plot product through the Wigner expansion
    graph_2 = canvas.add_subplot(grid[0,1], projection='3d')
    graph_2.plot_surface(x, y, z,  rstride=1, cstride=1, facecolors=cm.seismic(product_expansion))
    graph_2.set_axis_off()
    graph_2.set_title(f"∑$Y_j^m$")
    
    # Plot difference between direct and Wigner
    graph_3 = canvas.add_subplot(grid[0,2], projection='3d')
    graph_3.plot_surface(x, y, z,  rstride=1, cstride=1, facecolors=cm.seismic(product_difference))
    graph_3.set_axis_off()
    graph_3.set_title("Difference")
    
    # Plot each term in the expansion
    for u in range(len(expansion_term_list)):
        graph = canvas.add_subplot(grid[1,u], projection='3d')
        graph.plot_surface(x, y, z,  rstride=1, cstride=1, facecolors=cm.seismic(expansion_term_list[u][3]))
        graph.set_axis_off()
        graph.set_title(f"$Y_{{{expansion_term_list[u][0]}}}^{{{expansion_term_list[u][1]}}}$")
    
    plt.show()

##################################################################################
# Global scripts
main()

##################################################################################