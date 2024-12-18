###########################################################################################################################
# Poisson distribution and Fisher information
print("\n###############################################################################")
print("Welcome!")
print("This code examines the Fisher information of the Poisson distribution.")
print("The goal is to relate Fisher information and the convergence of samples.")
print("###############################################################################\n")
###########################################################################################################################

###########################################################################################################################
# Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.stats import poisson

###########################################################################################################################
# Parameters
parameters = [25, 20, 30, 144, 132, 156]
sample_size = 10000

x1 = np.arange(0, 200, 1)
x2 = np.arange(0, sample_size, 1)
μ_nonzero = np.arange(1, 200, 1)

###########################################################################################################################
# Definitions
def poisson_pmf1(k, lamb):
    """ Calculates Poisson distribution for a fixed average and variable observations. """
    
    log_factorial = np.cumsum(np.log(np.arange(1, k.max() + 1)))
    log_factorial = np.insert(log_factorial, 0, 0)  # Insert log(0!) = 0 at the start
    log_pmf = -lamb + k * np.log(lamb) - log_factorial[k]
    pmf = np.exp(log_pmf)
    return pmf

def poisson_pmf2(lamb, k):
    """ Calculates Poisson distribution for a fixed observation and variable averages. """
    
    log_factorial = np.sum(np.log(np.arange(1, k + 1)))    
    log_pmf = -lamb + k * np.log(lamb) - log_factorial
    pmf = np.exp(log_pmf)
    return pmf
    
def calculate_MSE(lambda_param):
    """ Calculates mean-squared error of a randomly generated set that satisfies the given distribution. """
    
    random_values = poisson.rvs(mu=lambda_param, size=sample_size)
    running_avg = np.cumsum(random_values) / np.arange(1, sample_size + 1)
    mse = np.cumsum((running_avg - lambda_param) ** 2) / np.arange(1, sample_size + 1)
    return mse

def Fisher_information():
    """ Calculates Fisher information. """
    
    return -μ_nonzero * np.log(1-1/μ_nonzero**2)

###########################################################################################################################
# Global scripts
## Initialize plots
fig = plt.figure(figsize=(14, 7))
gs = GridSpec(3, 2, figure=fig)

## Plot Poisson distribution for the values set in parameters
ax1 = fig.add_subplot(gs[0, 0])
ax1.stem(x1, poisson_pmf1(x1, parameters[1]), basefmt=" ", linefmt='C1:') # poisson.pmf()
ax1.stem(x1, poisson_pmf1(x1, parameters[2]), basefmt=" ", linefmt='C1:')
ax1.stem(x1, poisson_pmf1(x1, parameters[0]), basefmt=" ", linefmt='C0-')
ax1.set_title('Poisson Distribution (λ = {})'.format(parameters[0]))
ax1.set_ylabel('Probability')
ax1.grid(True)
ax1.text(0.95, 0.95, 'A', transform=ax1.transAxes, fontsize=16, verticalalignment='top', horizontalalignment='right')

ax2 = fig.add_subplot(gs[0, 1])
ax2.stem(x1, poisson_pmf1(x1, parameters[4]), basefmt=" ", linefmt='C1:')
ax2.stem(x1, poisson_pmf1(x1, parameters[5]), basefmt=" ", linefmt='C1:')
ax2.stem(x1, poisson_pmf1(x1, parameters[3]), basefmt=" ", linefmt='C0-')
ax2.set_title('Poisson Distribution (λ = {})'.format(parameters[3]))
ax2.grid(True)
ax2.text(0.95, 0.95, 'C', transform=ax2.transAxes, fontsize=16, verticalalignment='top', horizontalalignment='right')

## Plot the probability of obtaining 25 and 144 for a range of averages
#ax3 = fig.add_subplot(gs[1, 0])
#ax3.stem(x1, poisson_pmf2(x1, 25), basefmt=" ", linefmt='C0-')
#ax3.stem(x1, poisson_pmf1(x1, parameters[0])-poisson_pmf2(x1, 25), basefmt=" ", linefmt='C1-')
#ax3.set_ylabel('Relative Probability')
#ax3.grid(True)
#ax3.text(0.95, 0.95, 'B', transform=ax3.transAxes, fontsize=16, verticalalignment='top', horizontalalignment='right')

#ax4 = fig.add_subplot(gs[1, 1])
#ax4.stem(x1, poisson_pmf2(x1, 144), basefmt=" ", linefmt='C0-')
#ax4.stem(x1, poisson_pmf1(x1, parameters[3])-poisson_pmf2(x1, 144), basefmt=" ", linefmt='C1-')
#ax4.grid(True)
#ax4.text(0.95, 0.95, 'E', transform=ax4.transAxes, fontsize=16, verticalalignment='top', horizontalalignment='right')

## Plot mean-squared error for sets of randomly generated values according to each distribution
ax5 = fig.add_subplot(gs[1, 0])
ax5.plot(x2, calculate_MSE(parameters[0]))
ax5.plot(x2, calculate_MSE(parameters[0]))
ax5.plot(x2, calculate_MSE(parameters[0]))
ax5.plot(x2, calculate_MSE(parameters[0]))
ax5.plot(x2, calculate_MSE(parameters[0]))
ax5.set_ylabel('MSE')
ax5.set_ylim(0, 0.5)
ax5.grid(True)
ax5.text(0.95, 0.95, 'B', transform=ax5.transAxes, fontsize=16, verticalalignment='top', horizontalalignment='right')

ax6 = fig.add_subplot(gs[1, 1])
ax6.plot(x2, calculate_MSE(parameters[3]))
ax6.plot(x2, calculate_MSE(parameters[3]))
ax6.plot(x2, calculate_MSE(parameters[3]))
ax6.plot(x2, calculate_MSE(parameters[3]))
ax6.plot(x2, calculate_MSE(parameters[3]))
ax6.set_ylim(0, 0.5)
ax6.grid(True)
ax6.text(0.95, 0.95, 'D', transform=ax6.transAxes, fontsize=16, verticalalignment='top', horizontalalignment='right')

## Plot Fisher information
ax5 = fig.add_subplot(gs[2, :])
ax5.plot(μ_nonzero, Fisher_information())
ax5.axvline(parameters[0], linestyle=':')
ax5.axvline(parameters[3], linestyle=':')
ax5.set_ylabel('Fisher Information')
ax5.set_ylim(0, 0.5)
ax5.grid(True)
ax5.text(0.95, 0.95, 'E', transform=ax5.transAxes, fontsize=16, verticalalignment='top', horizontalalignment='right')

## Finalize and plot
plt.tight_layout()
plt.show()

###########################################################################################################################