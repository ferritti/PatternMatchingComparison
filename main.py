import random as rd
import string
import timeit
import os
from matplotlib import pyplot as plt

def naive_string_matcher(T, P):
    for s in range(len(T) - len(P) + 1):
        if T[s:s + len(P)] == P:
            print(f"Occorrenza del pattern con spostamento {s}")


def kmp_matcher(T, P):
    lpc = compute_prefix_function(P, len(P))
    q = 0
    for i in range(len(T)):
        while q > 0 and P[q] != T[i]:
            q = lpc[q - 1]
        if P[q] == T[i]:
            q += 1
        if q == len(P):
            print(f"Occorrenza del pattern con spostamento {i - len(P) + 1}")
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
    return ''.join(rd.choice(string.ascii_lowercase) for _ in range(length))

#Genera un pattern ripetuto frequentemente
def generate_repeated_string(length):
   return 'abc' * (length // 3) + 'abc'[:length % 3]


#Tempo di esecuzione medio per una serie di ripetizioni di naive e kmp con text e pattern in input
def test_execution_time(text, pattern, repetitions):
   naive_time = timeit.timeit(lambda: naive_string_matcher(text, pattern), number=repetitions) / repetitions
   kmp_time = timeit.timeit(lambda: kmp_matcher(text, pattern), number=repetitions) / repetitions
   return naive_time, kmp_time


#Confronta i tempi di esecuzione degli algoritmi Naive e KMP su più testi e pattern di lunghezza variabile.
def execution_time_comparison(text_lengths, pattern_lengths, generate_fn, repetitions=30):
    naive_tuples = []
    kmp_tuples = []
    for text_length in text_lengths:
        for pattern_length in pattern_lengths:
            text = generate_fn(text_length)  # Usa la funzione per generare il testo
            pattern = generate_fn(pattern_length)  # Usa la funzione per generare il pattern
            naive_time, kmp_time = test_execution_time(text, pattern, repetitions)
            naive_tuples.append((text_length, pattern_length, naive_time))
            kmp_tuples.append((text_length, pattern_length, kmp_time))
    return naive_tuples, kmp_tuples

#per ogni lunghezza di pattern, crea un grafico con i tempi di esecuzione per entrambi gli algoritmi e lo salva.
def plot_execution_time(naive_tuples, kmp_tuples, base_output_path, pattern_description):
    text_lengths = sorted(set(t[0] for t in naive_tuples))
    pattern_lengths = sorted(set(t[1] for t in naive_tuples))

    # Imposta il percorso di destinazione basato sul tipo di pattern
    output_path = os.path.join(base_output_path, pattern_description)

    # Crea la cartella per salvare i grafici se non esiste
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for pattern_length in pattern_lengths:
        naive_times = [t[2] for t in naive_tuples if t[1] == pattern_length]
        kmp_times = [t[2] for t in kmp_tuples if t[1] == pattern_length]

        plt.figure(figsize=(10, 5))
        plt.plot(text_lengths, naive_times, label='Naive', marker='o')
        plt.plot(text_lengths, kmp_times, label='KMP', marker='o')
        plt.xlabel('Lunghezza testo')
        plt.ylabel('Tempo di esecuzione (secondi)')
        plt.title(f'Confronto tempi di esecuzione con Pattern di lunghezza {pattern_length} ({pattern_description})')
        plt.legend()
        plt.grid(True)

        # Salva il grafico nella cartella specificata
        filename = f'grafico_pattern_{pattern_length}_{pattern_description}.png'
        file_path = os.path.join(output_path, filename)
        plt.savefig(file_path)

# Funzione principale che esegue i test con diversi tipi di pattern
def main(text_lengths_sets, pattern_lengths_sets, repetitions=10):
    base_output_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Latex images', 'Tempo esecuzione')

    # Due casi: testo e pattern casuali, e testo e pattern ripetuti frequentemente
    string_types = [
        ("Testo e pattern casuale", generate_random_string),
        ("Testo pattern ripetuto frequentemente", generate_repeated_string)
    ]

    for string_description, generate_fn in string_types:
        for size in text_lengths_sets:
            text_lengths = text_lengths_sets[size]
            pattern_lengths = pattern_lengths_sets[size]

            # Esegui i test e genera i grafici
            naive_tuples, kmp_tuples = execution_time_comparison(text_lengths, pattern_lengths, generate_fn, repetitions)
            plot_execution_time(naive_tuples, kmp_tuples, base_output_path, string_description)




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