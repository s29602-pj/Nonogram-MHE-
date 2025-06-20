import itertools
import time
import copy
import random


from funkcjaCelu import porownaj_siatki
from funkcjaCelu import generuj_sasiedztwo


#Pelen przeglad
def pelny_przeglad(wysokosc, szerokosc, siatka_wzor):
    start_time = time.time()
    licznik = 0

    for kombinacja in itertools.product([1, 2], repeat=wysokosc * szerokosc):#generuje wszystkie możliwe kombinacje elementów z podanej listy,
        licznik += 1

        siatka = [
            list(kombinacja[y * szerokosc:(y + 1) * szerokosc])#wycinanie wierszy prosty stystem 0:5np
            for y in range(wysokosc)#Powtarzaj coś dla każdego wiersza siatki, od y = 0 do y = wysokosc - 1.
        ]

        bledy = porownaj_siatki(siatka, siatka_wzor)

        if bledy == 0:
            czas = time.time() - start_time
            print(f"\n Znaleziono idealne rozwiązanie w próbie nr {licznik}")
            print(f" Czas przeszukiwania: {czas:.4f} sekundy")
            return siatka, 0



def algorytm_wspinaczkowy_klasyczny(siatka_start, siatka_wzor):
    start_time = time.time()
    aktualna = copy.deepcopy(siatka_start)#robi pełną, niezależną kopię aktualna = [wiersz.copy() for wiersz in siatka_start]
    blad_aktualny = porownaj_siatki(aktualna, siatka_wzor)
    iteracja = 0

    while True:
        iteracja += 1
        sasiedzi = generuj_sasiedztwo(aktualna)
        najlepszy = min(sasiedzi, key=lambda s: porownaj_siatki(s, siatka_wzor))#Porównuj elementy według tej konkretnej wartości,Dla każdego s (czyli siatki), oblicz coś
        blad_najlepszy = porownaj_siatki(najlepszy, siatka_wzor)

        if blad_najlepszy < blad_aktualny:
            aktualna = najlepszy
            blad_aktualny = blad_najlepszy
        else:
            break #minimum lokalne


        if blad_aktualny == 0:
            break

    czas = time.time() - start_time
    return aktualna, blad_aktualny, iteracja, czas


def algorytm_wspinaczkowy_losowy(siatka_start, siatka_wzor):
    start_time = time.time()
    aktualna = copy.deepcopy(siatka_start)#robi pełną, niezależną kopię
    blad_aktualny = porownaj_siatki(aktualna, siatka_wzor)

    iteracja = 0

    while True:
        iteracja += 1

        sasiedzi = generuj_sasiedztwo(aktualna)
        losowy = random.choice(sasiedzi)
        blad_losowy = porownaj_siatki(losowy, siatka_wzor)

        if blad_losowy <= blad_aktualny:
            aktualna = losowy
            blad_aktualny = blad_losowy

        if blad_aktualny == 0:
            break
        if iteracja > 10000:#specjalnie poniewaz to moze trwac bardzo dlugo albo nawet program moze sie zawiersic mozna zwiekszy zazwyczaj 5x5 wyszukuje  100 iles
            print("Przekroczono limit iteracji!")
            break

    czas = time.time() - start_time
    return aktualna, blad_aktualny, iteracja, czas
