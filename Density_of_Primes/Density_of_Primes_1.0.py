import matplotlib.pyplot as plt

def is_prime(n):
    """
    Returns True if n is prime, False otherwise.
    """
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

x = range(100001)  # integer values from 0 to 10000
primes = [is_prime(n) for n in x]  # list of True/False values indicating whether each number is prime
cumulative_primes = [sum(primes[:i]) for i in range(len(primes))]  # cumulative sum of True values up to each index

plt.semilogx(x, cumulative_primes)
plt.title('Cumulative Number of Prime Numbers')
plt.xlabel('Integers')
plt.ylabel('Cumulative Number of Primes')
plt.yscale('log')  # sets the y-axis to logarithmic scale
plt.show()
