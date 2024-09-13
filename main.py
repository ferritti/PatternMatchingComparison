import numpy as np
import random as rd
import string as str
import timeit

from matplotlib import pyplot as plt


def naive_string_matcher(T, P):
    n = len(T)
    m = len(P)

    for s in range(n - m + 1):
        if T[s:s + m] == P:
            print(f"Occorrenza del pattern con spostamento {s}")


def kmp_matcher(T, P):
    n = len(T)
    m = len(P)
    pi = compute_prefix_function(P, m)
    q = 0

    for i in range(n):
        while q > 0 and P[q] != T[i]:
            q = pi[q]
        if P[q] == T[i]:
            q += 1
        if q == m:
            print(f"Occorrenza del pattern con spostamento {i - m + 1}")
            q = pi[q - 1]

def compute_prefix_function(P, m):
    pi = np.zeros(m,dtype=int)
    k = 0

    for q in range(1, m):
        while k > 0 and P[k] != P[q]:
            k = pi[k - 1]
        if P[k] == P[q]:
            k += 1
        pi[q] = k

    return pi


def generate_random_string(length):
    return ''.join(rd.choice(str.ascii_lowercase) for _ in range(length))

#test per ottenere i tempi di esecuzione di naive e kmp con text e pattern stringe casuali di lunghezza rispettivamente n e m.
def test_execution_time(n, m):
    text = generate_random_string(n)
    pattern = generate_random_string(m)

    naive_time = timeit.timeit(lambda: naive_string_matcher(text, pattern), number=1)
    kmp_time = timeit.timeit(lambda: kmp_matcher(text, pattern), number=1)

    return naive_time, kmp_time