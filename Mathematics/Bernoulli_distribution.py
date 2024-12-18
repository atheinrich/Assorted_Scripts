###########################################################################################################################
# Bernoulli distribution and Fisher information
print("\n###############################################################################")
print("Welcome!")
print("This code examines the Fisher information of the Bernoulli distribution.")
print("The goal is to relate Fisher information and the convergence of samples.")
print("###############################################################################\n")
###########################################################################################################################

###########################################################################################################################
# Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.stats import bernoulli

###########################################################################################################################
# Parameters
parameters = [0.05, 0.5] # holds fixed probabilities (fixed averages)
sample_size = 10000 # used for MSE

x1 = np.arange(0, 2, 1) # sets possible observations
x2 = np.arange(0, sample_size, 1) # used for MSE
p_nonzero = np.linspace(0.001, 0.999, 1000)

###########################################################################################################################
# Definitions'
def bernoulli_pmf(x, p):
    """ Calculates Bernoulli distribution for a fixed average and variable observations.
        The result is identical to a fixed observation and variable averages. """
    
    return [1 - p, p]

def calculate_MSE(p):
    """ Calculates mean-squared error of a randomly generated set that satisfies the given distribution. """

    random_values = bernoulli.rvs(p, size=sample_size)
    running_avg = np.cumsum(random_values) / np.arange(1, sample_size + 1)
    mse = np.cumsum((running_avg - p) ** 2) / np.arange(1, sample_size + 1)
    return mse

def Fisher_information():
    """ Calculates Fisher information. """
    
    return 1/(p_nonzero * (1 - p_nonzero))

###########################################################################################################################
# Global scripts
## Initialize plots
fig = plt.figure(figsize=(14, 7))
gs = GridSpec(3, 2, figure=fig)

## Plot Bernoulli distribution for the values set in parameters
ax1 = fig.add_subplot(gs[0, 0])
ax1.bar(x1, bernoulli_pmf(x1, parameters[0]), width=0.4, color='blue', alpha=0.7)
ax1.set_xticks(x1)
ax1.set_xticklabels(['0', '1'])
ax1.set_ylabel('Probability')
ax1.set_title('Bernoulli Distribution (p = {})'.format(parameters[0]))
ax1.text(0.95, 0.95, 'A', transform=ax1.transAxes, fontsize=16, verticalalignment='top', horizontalalignment='right')

ax2 = fig.add_subplot(gs[0, 1])
ax2.bar(x1, bernoulli_pmf(x1, parameters[1]), width=0.4, color='green', alpha=0.7)
ax2.set_xticks(x1)
ax2.set_xticklabels(['0', '1'])
ax2.set_title('Bernoulli Distribution (p = {})'.format(parameters[1]))
ax2.text(0.95, 0.95, 'C', transform=ax2.transAxes, fontsize=16, verticalalignment='top', horizontalalignment='right')

## Plot mean-squared error for sets of randomly generated values according to each distribution
ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(x2, calculate_MSE(parameters[0]))
ax3.plot(x2, calculate_MSE(parameters[0]))
ax3.plot(x2, calculate_MSE(parameters[0]))
ax3.plot(x2, calculate_MSE(parameters[0]))
ax3.plot(x2, calculate_MSE(parameters[0]))
ax3.set_ylabel('MSE')
ax3.set_ylim(0, 0.005)
ax3.grid(True)
ax3.text(0.95, 0.95, 'B', transform=ax3.transAxes, fontsize=16, verticalalignment='top', horizontalalignment='right')

ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(x2, calculate_MSE(parameters[1]))
ax4.plot(x2, calculate_MSE(parameters[1]))
ax4.plot(x2, calculate_MSE(parameters[1]))
ax4.plot(x2, calculate_MSE(parameters[1]))
ax4.plot(x2, calculate_MSE(parameters[1]))
ax4.set_ylim(0, 0.005)
ax4.grid(True)
ax4.text(0.95, 0.95, 'D', transform=ax4.transAxes, fontsize=16, verticalalignment='top', horizontalalignment='right')

## Plot Fisher information
ax5 = fig.add_subplot(gs[2, :])
ax5.plot(p_nonzero, Fisher_information())
ax5.axvline(parameters[0], linestyle=':')
ax5.axvline(parameters[1], linestyle=':')
ax5.set_ylabel('Fisher Information')
ax5.set_ylim(0, 100)
ax5.grid(True)
ax5.text(0.95, 0.95, 'E', transform=ax5.transAxes, fontsize=16, verticalalignment='top', horizontalalignment='right')

## Finalize and plot
plt.tight_layout()
plt.show()

###########################################################################################################################