###########################################################################################################################
# Density of primes
print("\n###############################################################################")
print("Welcome!")
print("This code counts prime numbers and compares the result to a linear function.")
print("The goal is to illustrate the distribution of prime numbers.")
print("The ratios illustrate a maximum deviation from linearity.")
print("###############################################################################\n")
###########################################################################################################################

###########################################################################################################################
# Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

###########################################################################################################################
# Definitions
def sieve_of_eratosthenes(limit):
    """Generates a list of booleans where True means the number is prime."""
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[:2] = False  # 0 and 1 are not prime
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i*i:limit+1:i] = False  # Mark multiples of i as non-prime
    return sieve

def main():
    global x, cumulative_primes, ratio_primes, linear_primes, linear_approx
    
    # Set order of magnitude of integers to test, generate integer list
    order = 5
    limit = 10**order
    x = np.arange(1, limit+1)

    # Generate primes using Sieve of Eratosthenes
    primes = sieve_of_eratosthenes(limit)

    # Process data
    cumulative_primes = np.cumsum(primes[1:])  # Cumulative sum of prime booleans
    ratio_primes = cumulative_primes / x  # Ratio of cumulative primes to integer
    linear_primes = cumulative_primes - (0.0937 * x)  # Linearly adjusted prime count
    linear_approx = 0.0937 * x  # Linear approximation line based on prime density

###########################################################################################################################
# Global
main()

# Additional plots
canvas = plt.figure(figsize=(12, 5))
grid = GridSpec(nrows=1, ncols=3, wspace=0.5)

graph_1 = canvas.add_subplot(grid[0,0])
graph_1.set_title("Cumulative number of primes")
graph_1.set(xlabel=r"$n$", ylabel=r"$N$")
graph_1.plot(x, cumulative_primes)
graph_1.plot(x, linear_approx, linestyle=':', color='r', label='Linear Approximation')  # Added dotted line
graph_1.legend()
graph_1.grid()

graph_2 = canvas.add_subplot(grid[0,1])
graph_2.set_title("Ratio of cumulative to integers")
graph_2.set(xlabel=r"$n$", ylabel=r"$N$")
graph_2.plot(x, ratio_primes)
graph_2.grid()

graph_3 = canvas.add_subplot(grid[0,2])
graph_3.set_title("Linearly adjusted ratio")
graph_3.set(xlabel=r"$n$", ylabel=r"$N$")
graph_3.plot(x, linear_primes)
graph_3.grid()

plt.show()
