import random as rd
import string as str
import timeit
import os

from matplotlib import pyplot as plt

def naive_string_matcher(T, P):
    n = len(T)
    m = len(P)

    for s in range(n - m + 1):
        if T[s:s + m] == P:
            pass#print(f"Occorrenza del pattern con spostamento {s}")


def kmp_matcher(T, P):
    n = len(T)
    m = len(P)
    lpc = compute_prefix_function(P, m)
    q = 0

    for i in range(n):
        while q > 0 and P[q] != T[i]:
            q = lpc[q]
        if P[q] == T[i]:
            q += 1
        if q == m:
            #print(f"Occorrenza del pattern con spostamento {i - m + 1}")
            q = lpc[q - 1]


def compute_prefix_function(P, m):
    pi = [0] * m
    k = 0

    for q in range(1, m):
        while k > 0 and P[k] != P[q]:
            k = pi[k - 1]
        if P[k] == P[q]:
            k += 1
        pi[q] = k

    return pi

#Genera una stringa casuale di lunghezza specificata
def generate_random_string(length):
    return ''.join(rd.choice(str.ascii_lowercase) for _ in range(length))

#Genera un pattern ripetuto frequentemente
def generate_repeated_pattern(length):
   return 'abc' * (length // 3) + 'abc'[:length % 3]


#tempo di esecuzione medio per una serie di ripetizioni di naive e kmp con text e pattern stringe casuali di lunghezza rispettivamente n e m.
def test_execution_time(n,m,repetitions):
    text = generate_random_string(n)
    pattern = generate_random_string(m)

    naive_time = timeit.timeit(lambda: naive_string_matcher(text, pattern), number=repetitions) / repetitions
    kmp_time = timeit.timeit(lambda: kmp_matcher(text, pattern), number=repetitions) / repetitions

    return naive_time, kmp_time

#confronta i tempi di esecuzione degli algoritmi Naive e KMP su più testi e pattern di lunghezza variabile.
def execution_time_comparison(text_lengths, pattern_lengths,repetitions=10):
    naive_tuples = []
    kmp_tuples = []

    for text_length in text_lengths:
        for pattern_length in pattern_lengths:
            naive_time, kmp_time = test_execution_time(text_length, pattern_length,repetitions)
            naive_tuples.append((text_length, pattern_length, naive_time))
            kmp_tuples.append((text_length, pattern_length, kmp_time))

    return naive_tuples, kmp_tuples

#per ogni lunghezza di pattern, crea un grafico con i tempi di esecuzione per entrambi gli algoritmi e lo salva.
def plot_execution_time(naive_tuples, kmp_tuples):
    text_lengths = sorted(set(t[0] for t in naive_tuples))
    pattern_lengths = sorted(set(t[1] for t in naive_tuples))

    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Latex images', 'Tempo esecuzione')

    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)

    for pattern_length in pattern_lengths:
        naive_times = [t[2] for t in naive_tuples if t[1] == pattern_length]
        kmp_times = [t[2] for t in kmp_tuples if t[1] == pattern_length]

        plt.figure(figsize=(10, 5))
        plt.plot(text_lengths, naive_times, label='Naive', marker='o')
        plt.plot(text_lengths, kmp_times, label='KMP', marker='o')
        plt.xlabel('Lunghezza testo')
        plt.ylabel('Tempo di esecuzione (secondi)')
        plt.title(f'Confronto tempi di esecuzione con Pattern di lunghezza {pattern_length}')
        plt.legend()
        plt.grid(True)

        #Salva il grafico nella cartella
        filename = f'grafico lunghezza pattern {pattern_length}.png'
        file_path = os.path.join(desktop_path, filename)
        plt.savefig(file_path)






if __name__ == "__main__":
    text_lengths_sets = {
        "small": [50, 100, 200],
        "medium": [500, 1000, 2000],
        "large": [5000, 10000, 20000]
    }

    pattern_lengths_sets = {
        "small": [20, 30],
        "medium": [200, 500],
        "large": [3000, 5000]
    }

for size in text_lengths_sets:
        naive_tuples, kmp_tuples = execution_time_comparison(text_lengths_sets[size], pattern_lengths_sets[size])
        plot_execution_time(naive_tuples, kmp_tuples)