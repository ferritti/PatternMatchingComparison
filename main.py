

def naive_string_matcher(T, P):
    n = len(T)
    m = len(P)

    for s in range(n - m + 1):  #Scorre il testo fino all'indice n - m
        if T[s:s + m] == P:  #Controlla se il pattern coincide con la sottostringa del testo
            print(f"Occorrenza del pattern con spostamento {s}")

