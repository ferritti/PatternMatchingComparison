import numpy as np

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