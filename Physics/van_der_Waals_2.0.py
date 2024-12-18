###########################################################################################################################################################
# Phase Transitions for a van der Waals gas
print("\n###############################################################################")
print("Welcome!")
print("This code simulates a van der Waals gas.")
print("The goal is to predict the coexistence curve for phase transitions.")
print("###############################################################################\n")
###########################################################################################################################################################

###########################################################################################################################################################
# Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.signal import find_peaks

###########################################################################################################################################################
# Parameters and data containers
## Particle parameters
R = 8.314     # Gas constant in J/(mol*K)
a = 1.355e-1  # van der Waals constant 'a' in (m^6 * Pa) / mol^2 for argon
b = 3.201e-5  # van der Waals constant 'b' in m^3 / mol for argon
Tc = 8 * a / (27 * b * R)  # critical temperature
Tc = Tc - Tc/255 # slightly below critical temperature

# Data containers
V_values = np.linspace(1.5*b, 119.65*b, 10000)  # range of volumes in m^3
PV_min_list, PV_max_list, PV_intersect_list, PT_list = [], [], [], [] # notable datapoints
curves = [] # [i, T, P list, V list, P_max, V(P_max), P_min, V(P_min)]
sample_size_T = 10 # number of curves
Tc_range = Tc * 16 / 100 # critical range for positive pressure
T_values = [Tc - Tc_range*i/10 for i in range(sample_size_T)] # temperature of each curve

###########################################################################################################################################################
# Definitions
def calculate_pressure(V, T):
    """ Returns pressure using the van der Waals equation for a given volume and temperature. """
    return (R * T) / (V - b) - a / (V ** 2)

def piecewise_function(P_values, V_values, V_1, V_2):
    """ Chops P(V) curves into monotonically increasing and decreasing intervals. """
    pieces = [[[], []], [[], []], [[], []]]
    for i in range(len(V_values)):
        if V_values[i] < V_2:
            pieces[0][1].append(V_values[i])
            pieces[0][0].append(P_values[i])
        elif V_values[i] == V_2:
            pieces[0][1].append(V_values[i])
            pieces[0][0].append(P_values[i])
            pieces[1][1].append(V_values[i])
            pieces[1][0].append(P_values[i])
        elif V_values[i] < V_1:
            pieces[1][1].append(V_values[i])
            pieces[1][0].append(P_values[i])
        elif V_values[i] == V_1:
            pieces[1][1].append(V_values[i])
            pieces[1][0].append(P_values[i])
            pieces[2][1].append(V_values[i])
            pieces[2][0].append(P_values[i])
        else:
            pieces[2][1].append(V_values[i])
            pieces[2][0].append(P_values[i])
    return pieces

def integrate_with_numpy(x_values, y_values):
    """ Integrates a curve with a strictly positive result. """
    dx = abs(np.diff(x_values))
    dy = abs((np.array(y_values[:-1]) + np.array(y_values[1:])) / 2)
    integral = np.cumsum(dx * dy)
    return x_values[1:], list(integral)

def intersections(T, P):
    """ Finds points on the van der Waals equation corresponding to a given temperature and pressure. """
    coefficients = [P, -(P*b+R*T), a, -a*b] # 0=PV^3-(Pb+RT)V^2+aV-b
    roots = np.roots(coefficients)
    return [P, list(roots)]

###########################################################################################################################################################
# Initialize plots
fig = plt.figure(figsize=(15, 5))
gs = GridSpec(2, 5, figure=fig, wspace=0.5)
axes = [fig.add_subplot(gs[0, 0:2]), fig.add_subplot(gs[1, 0:2]), fig.add_subplot(gs[:, 2]), fig.add_subplot(gs[:, 3]), fig.add_subplot(gs[:, 4])]
colors = [(i/sample_size_T, i/sample_size_T, i/sample_size_T) for i in range(sample_size_T)]

## P(V) full view
axes[0].set_ylabel(r'$Pressure$ [MPa]')
axes[0].set_title(r'$P$($v$)')
axes[0].grid(True)
axes[0].set_xlim(0, 1400)  # Set explicit limits for the x-axis
axes[0].set_ylim(0, 6)   # Set explicit limits for the y-axis
axes[0].tick_params(axis='both', labelsize=8)

## P(V) small view
axes[1].set_xlabel(r'$Volume$ [cm$^3$/mol]')
axes[1].set_ylabel(r'$Pressure$ [MPa]')
axes[1].grid(True)
axes[1].set_xlim(50, 300)  # Set explicit limits for the x-axis
axes[1].set_ylim(0, 5.5)   # Set explicit limits for the y-axis
axes[1].tick_params(axis='both', labelsize=8)

## V(P)
axes[2].set_xlabel(r'$Pressure$ [MPa]')
axes[2].set_ylabel(r'$Volume$ [cm$^3$/mol]')
axes[2].set_title('$v$($P$)')
axes[2].grid(True)
axes[2].set_xlim(0, 6)   # Set explicit limits for the x-axis
axes[2].set_ylim(0, 400)  # Set explicit limits for the y-axis
axes[2].tick_params(axis='both', labelsize=8)

## μ(P)
axes[3].set_xlabel(r'$Pressure$ [MPa]')
axes[3].set_ylabel(r'$Chemical$ $potential$ [kJ/mol]')
axes[3].set_title('$μ$($P$)')
axes[3].grid(True)
axes[3].set_xlim(0, 6)   # Set explicit limits for the x-axis
axes[3].set_ylim(1.8, 3.2)   # Set explicit limits for the x-axis
axes[3].tick_params(axis='both', labelsize=8)

## P(T)
axes[4].set_xlabel(r'$Temperature$ [K]')
axes[4].set_ylabel(r'$Pressure$ [MPa]')
axes[4].set_title('$P$($T$)')
axes[4].grid(True)
axes[4].set_xlim(125, 155)   # Set explicit limits for the x-axis
axes[4].set_ylim(1.5, 5)   # Set explicit limits for the x-axis
axes[4].tick_params(axis='both', labelsize=8)

###########################################################################################################################################################
# Main
## Plot each P(V) curve for different temperatures
for i in range(len(T_values)):
    
    # Calculate pressures and plot results for each temperature
    P_values = calculate_pressure(V_values, T_values[i])
    axes[0].plot([x*1e6 for x in V_values], [x/1e6 for x in P_values], color=colors[i], label=f"{int(T_values[i])} K")
    axes[1].plot([x*1e6 for x in V_values], [x/1e6 for x in P_values], color=colors[i])

    # Find local maxima and minima
    peaks_max, _ = find_peaks(-P_values)  # Negative of pressure to find maxima
    peaks_min, _ = find_peaks(P_values)   # Positive pressure to find minima

    # Find extrema in the desired range
    peaks_max = peaks_max[(V_values[peaks_max] > b) & (V_values[peaks_max] < b * 12)]
    peaks_min = peaks_min[(V_values[peaks_min] > b) & (V_values[peaks_min] < b * 12)]

    # Save curve and local extrema
    curves.append([i, T_values[i], list(P_values), list(V_values), list(P_values[peaks_min]), list(V_values[peaks_min]), list(P_values[peaks_max]), list(V_values[peaks_max])])

    # Plot local extrema
    PV_min_list.append([list(P_values[peaks_max])[0], list(V_values[peaks_max])[0]])
    PV_max_list.append([list(P_values[peaks_min])[0], list(V_values[peaks_min])[0]])

## Calculate and plot V(P), μ(P), and coexistence lines
for i in range(len(curves)):
    j, T, P_values, V_values, P_max, V_max, P_min, V_min = curves[i]
    if P_max:
        
        # Chop P(V) into three monotonic intervals
        pieces = piecewise_function(P_values, V_values, V_max, V_min)
        pieces[0].reverse()
        pieces[0][0].reverse()
        pieces[0][1].reverse()
        pieces[1].reverse()

        pieces[2].reverse()
        pieces[2][0].reverse()
        pieces[2][1].reverse()
        VP_pieces = [pieces[2], pieces[1], pieces[0]] # [V, P]

        # Plot the results of V(P)
        axes[2].plot([x/1e6 for x in VP_pieces[0][1]], [x*1e6 for x in VP_pieces[0][0]], color=colors[j])
        axes[2].plot([x/1e6 for x in VP_pieces[1][1]], [x*1e6 for x in VP_pieces[1][0]], color=colors[j])
        axes[2].plot([x/1e6 for x in VP_pieces[2][1]], [x*1e6 for x in VP_pieces[2][0]], color=colors[j])
        
        pieces[1][1] = [-x for x in pieces[1][1]]
        pieces[1][0].reverse()
        pieces[1][1].reverse()
        
        # Find μ(P) and plot results
        inter_pieces = [[[], []], [[], []], [[], []]]
        for i in range(3):
            inter_pieces[i][0], inter_pieces[i][1] = integrate_with_numpy(VP_pieces[i][1], VP_pieces[i][0])
        inter_pieces[1][0] = [-x for x in inter_pieces[1][0]]
        axes[3].plot([x/1e6 for x in inter_pieces[0][0]], [x/1000 for x in inter_pieces[0][1]], color=colors[j])
        axes[3].plot([x/1e6 for x in inter_pieces[1][0]], [x/1000 for x in inter_pieces[0][1][-1]-inter_pieces[1][1]], color=colors[j])
        axes[3].plot([x/1e6 for x in inter_pieces[2][0]], [x/1000 for x in inter_pieces[0][1][-1]-inter_pieces[1][1][-1]+inter_pieces[2][1]], color=colors[j])
        
        # Find and plot coexistence line
        sample_size = 100 # sets number of pressure values to test for coexistence
        P_width = P_max[0] - P_min[0] # finds size between extrema
        P_set = [P_min[0] + ((i+0.1)/sample_size)*P_width for i in range(sample_size)]
        PV_equal_areas = [[], [], 1000, [0, 0, 0]] # holds P_coexistence, V_range, and area difference

        for i in range(sample_size): # Find intersections
            PV_intersections = intersections(T, P_set[i]) # [P_set, [V1, V2, V3]]

            # Find P(V) values in each bounded curve; max=peak, min=trough
            P_min_cache, V_min_cache, P_max_cache, V_max_cache = [], [], [], []
            P_min_fixed, V_min_fixed, P_max_fixed, V_max_fixed = [], [], [], []
            for k in range(len(V_values)):
                if PV_intersections[1][0] >= V_values[k] >= PV_intersections[1][1]:
                    P_max_cache.append(P_values[k])
                    V_max_cache.append(V_values[k])
                    P_max_fixed.append(P_set[i])
                    V_max_fixed.append(V_values[k])
                elif PV_intersections[1][1] >= V_values[k] >= PV_intersections[1][2]:
                    P_min_cache.append(P_values[k])
                    V_min_cache.append(V_values[k])
                    P_min_fixed.append(P_set[i])
                    V_min_fixed.append(V_values[k])
            x_1, area_min = integrate_with_numpy(V_min_cache, P_min_cache)
            x_2, area_max = integrate_with_numpy(V_max_cache, P_max_cache)
            area_min_fixed = P_min_fixed[0] * (V_min_fixed[-1] - V_min_fixed[0])
            area_max_fixed = P_max_fixed[0] * (V_max_fixed[-1] - V_max_fixed[0])
            area_curve_min = area_min_fixed - area_min[-1]
            area_curve_max = area_max[-1] - area_max_fixed
            area_diff = area_curve_min - area_curve_max
            if abs(area_diff) <= abs(PV_equal_areas[2]):
                PV_equal_areas[0] = P_min_fixed
                PV_equal_areas[1] = V_min_fixed
                PV_equal_areas[2] = area_diff
                PV_equal_areas[0].extend(P_max_fixed)
                PV_equal_areas[1].extend(V_max_fixed)
                PV_equal_areas[3][0] = P_set[i]
                PV_equal_areas[3][1] = PV_intersections[1][0]
                PV_equal_areas[3][2] = PV_intersections[1][2]
        axes[1].plot([x*1e6 for x in PV_equal_areas[1]], [x/1e6 for x in PV_equal_areas[0]], color=colors[j], linestyle='dotted')
        PV_intersect_list.append([PV_equal_areas[3][0], PV_equal_areas[3][1]])
        PV_intersect_list.append([PV_equal_areas[3][0], PV_equal_areas[3][2]])
        PT_list.append([PV_equal_areas[3][0], T, j])

# Plot notable datapoints
T_argon = [150.61, 150.55, 150.4, 150.0, 149.6, 149.0, 148.0, 146, 143, 140, 135, 130] # 125
P_argon = [4.84836, 4.83699, 4.80875, 4.73444, 4.66137, 4.55381, 4.37952, 4.04769, 3.58755, 3.16822, 2.55082, 2.02536] # 1.58227
for i in range(len(T_argon)):
    axes[4].scatter(T_argon, P_argon, color='black', marker='x')
for i in range(len(PT_list)):
    axes[4].scatter(PT_list[i][1], PT_list[i][0]/1e6, color=colors[PT_list[i][-1]], marker='o')

for i in range(len(PV_min_list)):
    axes[1].scatter(PV_min_list[i][1]*1e6, PV_min_list[i][0]/1e6, color='red', marker='o', s=6, zorder=3)
for i in range(len(PV_max_list)):
    axes[1].scatter(PV_max_list[i][1]*1e6, PV_max_list[i][0]/1e6, color='green', marker='o', s=6, zorder=3)
for i in range(len(PV_intersect_list)):
    axes[1].scatter(PV_intersect_list[i][1]*1e6, PV_intersect_list[i][0]/1e6, color='black', marker='o', s=6, zorder=3)

axes[0].legend(fontsize=7, loc='upper right')
plt.show()

###########################################################################################################################################################
