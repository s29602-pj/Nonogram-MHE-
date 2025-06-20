import math
import time
import random
import copy
from funkcjaCelu import porownaj_siatki
from funkcjaCelu import generuj_sasiedztwo

def algorytm_symulowanego_wyzarzania(siatka_start, siatka_wzor,
                                      T_start=100.0, T_koniec=0.1, alfa=0.95):
    start_time = time.time()
    aktualna = copy.deepcopy(siatka_start)
    blad_aktualny = porownaj_siatki(aktualna, siatka_wzor)
    najlepsza = copy.deepcopy(aktualna)
    blad_najlepszy = blad_aktualny

    T = T_start
    iteracja = 0

    while T > T_koniec:
        iteracja += 1
        sasiedzi = generuj_sasiedztwo(aktualna)
        kandydat = random.choice(sasiedzi)
        blad_kandydata = porownaj_siatki(kandydat, siatka_wzor)

        delta = blad_kandydata - blad_aktualny

        if delta < 0:
            aktualna = kandydat
            blad_aktualny = blad_kandydata
        else:
            p = math.exp(-delta / T)
            if random.random() < p:
                aktualna = kandydat
                blad_aktualny = blad_kandydata

        if blad_aktualny < blad_najlepszy:
            najlepsza = copy.deepcopy(aktualna)
            blad_najlepszy = blad_aktualny

        if blad_najlepszy == 0:
            break

        T *= alfa  # schładzanie

    czas = time.time() - start_time
    return najlepsza, blad_najlepszy, iteracja, czas