import random
import copy
import time
from funkcjaCelu import porownaj_siatki


def tworz_osobnika(wysokosc, szerokosc):
    return [[random.choice([1, 2]) for _ in range(szerokosc)] for _ in range(wysokosc)]

def flatten(siatka):
    return [gen for row in siatka for gen in row]

def unflatten(genotyp, wysokosc, szerokosc):
    return [genotyp[i*szerokosc:(i+1)*szerokosc] for i in range(wysokosc)]

def fitness(siatka, siatka_wzor):
    max_dopasowanie = len(siatka) * len(siatka[0])
    return max_dopasowanie - porownaj_siatki(siatka, siatka_wzor)

# -- KRZYŻowanie --
def krzyzowanie_jednopunktowe(rodzic1, rodzic2):
    gen1 = flatten(rodzic1)
    gen2 = flatten(rodzic2)
    punkt = random.randint(1, len(gen1) - 2)
    dziecko = gen1[:punkt] + gen2[punkt:]
    return unflatten(dziecko, len(rodzic1), len(rodzic1[0]))

def krzyzowanie_uniform(rodzic1, rodzic2):
    gen1 = flatten(rodzic1)
    gen2 = flatten(rodzic2)
    dziecko = [random.choice([g1, g2]) for g1, g2 in zip(gen1, gen2)]
    return unflatten(dziecko, len(rodzic1), len(rodzic1[0]))

# -- Mutacje --
def mutacja_losowa(siatka, prawd_mutacji=0.05):
    nowa = copy.deepcopy(siatka)
    for y in range(len(nowa)):
        for x in range(len(nowa[0])):
            if random.random() < prawd_mutacji:
                nowa[y][x] = 1 if nowa[y][x] == 2 else 2
    return nowa

def mutacja_jednopunktowa(siatka):
    nowa = copy.deepcopy(siatka)
    y = random.randint(0, len(nowa) - 1)
    x = random.randint(0, len(nowa[0]) - 1)
    nowa[y][x] = 1 if nowa[y][x] == 2 else 2
    return nowa

# -- Selekcja turniejowa --
def turniej(oceny, k=3):
    wybrani = random.sample(oceny, k)
    wybrani.sort(reverse=True)
    return wybrani[0][1]

# -- Algorytm genetyczny --
def algorytm_genetyczny(siatka_wzor, populacja_rozmiar=50, pokolenia=100,
                        elita=True, metoda_krzyzowania="uniform", metoda_mutacji="losowa",
                        warunek_stop="idealne"):

    wysokosc, szerokosc = len(siatka_wzor), len(siatka_wzor[0])
    populacja = [tworz_osobnika(wysokosc, szerokosc) for _ in range(populacja_rozmiar)]
    historia = []
    start_time = time.time()

    for epoka in range(pokolenia):
        oceny = [(fitness(os, siatka_wzor), os) for os in populacja]
        oceny.sort(reverse=True)
        najlepszy_fitness = oceny[0][0]
        historia.append(len(siatka_wzor)*len(siatka_wzor[0]) - najlepszy_fitness)

        if warunek_stop == "idealne" and najlepszy_fitness == wysokosc * szerokosc:
            break
        if warunek_stop == "brak_poprawy" and epoka > 10 and all(historia[-1] == h for h in historia[-5:]):
            break

        nowa_populacja = []

        if elita:
            nowa_populacja.append(copy.deepcopy(oceny[0][1]))

        while len(nowa_populacja) < populacja_rozmiar:
            rodzic1 = turniej(oceny)
            rodzic2 = turniej(oceny)

            if metoda_krzyzowania == "jednopunktowe":
                dziecko = krzyzowanie_jednopunktowe(rodzic1, rodzic2)
            else:
                dziecko = krzyzowanie_uniform(rodzic1, rodzic2)

            if metoda_mutacji == "losowa":
                dziecko = mutacja_losowa(dziecko)
            else:
                dziecko = mutacja_jednopunktowa(dziecko)

            nowa_populacja.append(dziecko)

        populacja = nowa_populacja

    najlepszy = max(populacja, key=lambda o: fitness(o, siatka_wzor))
    czas = time.time() - start_time
    blad_koncowy = porownaj_siatki(najlepszy, siatka_wzor)
    return najlepszy, blad_koncowy, epoka + 1, czas, historia