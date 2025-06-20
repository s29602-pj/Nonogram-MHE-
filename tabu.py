import time
import copy
from funkcjaCelu import porownaj_siatki
from funkcjaCelu import generuj_sasiedztwo




def algorytm_tabu(siatka_start, siatka_wzor, max_iteracje=None):
    start_time = time.time()
    aktualna = copy.deepcopy(siatka_start)
    najlepsza = copy.deepcopy(aktualna)
    blad_najlepszy = porownaj_siatki(najlepsza, siatka_wzor)
    tabu = [copy.deepcopy(aktualna)]
    historia = [copy.deepcopy(aktualna)]

    iteracja = 0
    while True:
        iteracja += 1

        sasiedzi = generuj_sasiedztwo(aktualna)
        sasiedzi_dopuszczalni = [s for s in sasiedzi if s not in tabu]#######

        if not sasiedzi_dopuszczalni:
            if len(historia) > 1:
                aktualna = copy.deepcopy(historia[-2])
                historia = historia[:-1]
                continue
            else:
                break

        najlepszy_kandydat = min(sasiedzi_dopuszczalni, key=lambda s: porownaj_siatki(s, siatka_wzor))#######
        blad_kandydata = porownaj_siatki(najlepszy_kandydat, siatka_wzor)

        aktualna = najlepszy_kandydat
        historia.append(copy.deepcopy(aktualna))
        tabu.append(copy.deepcopy(aktualna))

        if blad_kandydata < blad_najlepszy:
            najlepsza = copy.deepcopy(najlepszy_kandydat)
            blad_najlepszy = blad_kandydata

        if blad_najlepszy == 0:
            break

        # Awaryjne zatrzymanie, jeśli użytkownik nie poda limitu
        if max_iteracje is not None and iteracja >= max_iteracje:
            print("Zatrzymano algorytm po osiągnięciu limitu iteracji.")
            break

    czas = time.time() - start_time
    return najlepsza, blad_najlepszy, iteracja, czas, historia