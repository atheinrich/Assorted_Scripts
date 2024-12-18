###############################################################################################
## Numerical analysis of harmonic oscillator potential
print("\n###############################################################################")
print("Welcome!")
print("This code plots orbits for an effective central potential.")
print("The goal is to illustrate how the orbit changes with energy.")
print("###############################################################################\n")
###############################################################################################

###############################################################################################
## Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cmath as cm
from time import sleep

###############################################################################################
## Initialization
# Parameters
L = 1
m = 1
k = 1

ω = np.sqrt(k/m)
r_min = L/(k*m)**(1/2)
E_min = L*(k/m)**(1/2)

# Variables
θ0 = 0
θ = 2*np.pi
dθ = 0.001

E0 = E_min/2
E = E_min*2+0.1
dE = 2
E_list = [E0]

r0 = 0.01
dr = 0.001

# Graphs
canvas = plt.figure(figsize=(14, 7))
grid = GridSpec(nrows=1, ncols=2)
colors, color_trigger = ['red', 'blue', 'green'], 0

graph_1 = canvas.add_subplot(grid[0,0], projection='polar')
graph_1.set_title("Orbit")

graph_2 = canvas.add_subplot(grid[0,1])
graph_2.set_title("Effective Potential")
graph_2.set(xlabel='$r$ [m]', ylabel="$U$ [kg∙m$^2$/s$^2$]")
graph_2.set_ylim(0, 5)
graph_2.set_xlim(0, 5)

###############################################################################################
## Main
# Analytic solution
r = lambda θ : cm.sqrt((L**2/(m*E_list[-1])) * (1-cm.sqrt(1-(ω*L/E_list[-1])**2)*cm.sin(2*(θ-θ0)))**(-1))

# Calculate orbits
while E_list[-1] < E:
    θ_list = [θ0] # Sets initial value
    r_list = [r(θ0)] # Sets initial value
    while θ_list[-1] < θ: # Calculates r(θ)
        θ_list.append(θ_list[-1]+dθ)
        r_list.append(r(θ_list[-1]+dθ))
    if (ω*L/E_list[-1])**2 <= 1: # Plots real orbits
        graph_1.plot(θ_list, r_list, label=f"$r$(θ), $E$(min)∙{E_list[-1]}", color=colors[color_trigger])
    else: # Plots complex orbits
        graph_1.plot(θ_list, r_list, label=f"$r$(θ), $E$(min)∙{E_list[-1]}", color=colors[color_trigger], linestyle='dotted')
    color_trigger += 1 # Used to specify unique colors
    E_list.append(E_list[-1]*dE)

# Calculate potential energy
r_list, U1_list, U2_list, U_list, color_trigger = [r0], [0], [0], [0], 0
while r_list[-1] < 10: # Calculates U(r) for each potential energy
    U1 = L**2/(2*m*r_list[-1]**2)
    U2 = k*r_list[-1]**2/2
    U = U1 + U2
    r_list.append(r_list[-1]+dr)
    U1_list.append(U1)
    U2_list.append(U2)
    U_list.append(U)

# Plot data
graph_1.legend()

graph_2.axvline(x=r_min, color='pink', linestyle='dashdot', label='$r$(min)')
for i in range(len(E_list)-1):
    graph_2.axhline(y=E_list[i], linestyle='dotted', color=colors[color_trigger], label=f"$E$(min)∙{E_list[i]}")
    color_trigger += 1

graph_2.plot(r_list[1:], U1_list[1:], label=f"$U_1=L^2/(2 m r^2)$", linestyle='dashed')
graph_2.plot(r_list[1:], U2_list[1:], label=f"$U_2=k r^2/2$", linestyle='dashed')
graph_2.plot(r_list[1:], U_list[1:], label=f"$U$(eff)=$U_1$+$U_2$")
graph_2.legend()

plt.show()

###############################################################################################
