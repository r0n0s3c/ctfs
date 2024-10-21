import requests
from Crypto.Util.number import long_to_bytes

def chinese_remainder(n, a):
    """
    Solves a system of linear congruences using the Chinese Remainder Theorem.

    Parameters:
    n (list): Moduli (pairwise coprime)
    a (list): Residues

    Returns:
    x (int): Solution to the system of congruences
    """
    prod = 1
    for p in n:
        prod *= p

    sum = 0
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p

    return sum % prod

def mul_inv(a, b):
    """
    Computes the modular inverse of a modulo b using the Extended Euclidean Algorithm.

    Parameters:
    a (int): Number
    b (int): Modulus

    Returns:
    x (int): Modular inverse of a modulo b
    """
    if b == 1:
        return 1
    x0, x1 = 0, 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b
    return x1


url = "https://cyberhacktics.sfo2.digitaloceanspaces.com/DEADFACECTF2024/challenges/crypto/crypto13/ecdh_crack_20241013.log"
PRIMES = []
LOGS = []
resp = requests.get(url)
data = resp.text

for line in data.split('\n'):
    if 'computing' in line:
        PRIMES.append(int(line.replace('computing discrete log for prime: ', '')))
    else:
        LOGS.append(int(line.replace('discrete log found: ', '')))



#nis = [191, 1621, 61, 2447, 991, 1297, 47, 1049, 347, 283, 2617, 1429, 167, 307, 431, 683, 1627, 17, 827, 97, 523, 151, 37, 2269, 1733, 3, 19, 439]
#cis = [25, 293, 49, 2105, 564, 50, 13, 21, 229, 257, 307, 511, 124, 7, 63, 476, 1054, 2, 793, 60, 270, 145, 32, 796, 1041, 1, 9, 60]
print(long_to_bytes(chinese_remainder(PRIMES, LOGS)))