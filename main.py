import sys
from podstawaNono import parsuj
from podstawaNono import rozwiaz
from podstawaNono import drukuj_siatke

from funkcjaCelu import generuj_sasiedztwo
from funkcjaCelu import generuj_losowa_siatke
from funkcjaCelu import porownaj_siatki

from algorytmy import pelny_przeglad
from algorytmy import algorytm_wspinaczkowy_losowy
from algorytmy import algorytm_wspinaczkowy_klasyczny

from wyzarzanie import algorytm_symulowanego_wyzarzania

from porowanie import  porownaj_metody

from genetyczny import algorytm_genetyczny

from tabu import algorytm_tabu
from zbieznosc import generuj_wykres_zbieznosci




def main():
    if len(sys.argv) != 2: #dlugosc argumentów
        print("Brak pliku wejściowego. Możesz wpisać dane ręcznie.")
        print("Wpisz dane w 4 liniach (szerokość, wysokość, kolumny, wiersze):")
        dane = [
            input("Wpisz szerokość: "),
            input("Wpisz wysokość: "),
            input("Wpisz kolumny: "),
            input("Wpisz wiersze: ")
        ] # moze dodac tutaj ze dane zostaly zle podane???
    else:
        sciezka_pliku = sys.argv[1]
        try:#tutaj obslugujemy blad
            with open(sciezka_pliku, 'r', encoding='utf-8') as file:
                dane = file.read().strip().split("\n")#wczytuje cały plik jako jeden długi string,usuwa białe znaki z początku i końca,dzieli tekst na listę linii.
        except Exception as e:#przechwytuje bład
            print(f"Błąd przy wczytywaniu pliku: {e}")
            return
#Tak samo jak na ML zrobic
    if len(dane) != 4:
        print(f"Błąd: Dane muszą zawierać dokładnie 4 linie, ale znaleziono {len(dane)}.")
        return

    szerokosc, wysokosc, kolumny_raw, wiersze_raw = dane
    szerokosc, wysokosc = int(szerokosc), int(wysokosc)
    kolumny = parsuj(kolumny_raw)
    wiersze = parsuj(wiersze_raw)

    siatka = [[0] * szerokosc for _ in range(wysokosc)]#stwórz listę wierszy, a w każdym wierszu umieść szerokosc zer
    rozwiaz(wiersze, kolumny, siatka)
    print("Rozwiązanie początkowe (idealne):")
    drukuj_siatke(siatka)

    siatka_wzor = [wiersz.copy() for wiersz in siatka] #nasz punkt odniesienia,przejdz po każdym wierszu w siatce
    siatka_start = generuj_losowa_siatke(wysokosc, szerokosc) # losowa do nie ktorych dalem ja tutaj zeby nie bylo pozniej zamieszania

#Losowanie
    print("\nLosowa siatka:")
    siatka_losowa = generuj_losowa_siatke(wysokosc, szerokosc)
    drukuj_siatke(siatka_losowa)
    roznica = porownaj_siatki(siatka_losowa, siatka_wzor)
    print(f"Różnica względem wzorca: {roznica} pól")


#Najlepszy sasiad zmiana
    print("\nNajlepsze sąsiedztwo:")
    sasiedztwa = generuj_sasiedztwo(siatka)
    najlepszego_sasiedztwa = min(sasiedztwa, key=lambda s: porownaj_siatki(s, siatka_wzor))#POWTORZYC
    #wybiera najlepszy, co wybrac, oblicz bledy, jednolinijkowa funkcja tworzona w miejscu
    drukuj_siatke(najlepszego_sasiedztwa)
    print(f"Różnica względem wzorca: {porownaj_siatki(najlepszego_sasiedztwa, siatka_wzor)} pól")

#Pelen przeglad
    najlepsza, bledy = pelny_przeglad(wysokosc, szerokosc, siatka_wzor)
    drukuj_siatke(najlepsza)
    print(f"Różnica względem wzorca: {bledy} pól")

#Klasyczny
    wynik_klasyczny, blad_klasyczny, iteracje_klasyczny, czas_klasyczny = algorytm_wspinaczkowy_klasyczny(
    siatka_start, siatka_wzor)
    print("Wspinaczka klasyczna:")
    drukuj_siatke(wynik_klasyczny)
    print(f"Błędy: {blad_klasyczny}, Iteracje: {iteracje_klasyczny}, Czas: {czas_klasyczny:.4f}s")

#Losowy
    wynik_losowy, blad_losowy, iteracje_losowy, czas_losowy = algorytm_wspinaczkowy_losowy(siatka_start, siatka_wzor)
    print("Wspinaczka losowa:")
    drukuj_siatke(wynik_losowy)
    print(f"Błędy: {blad_losowy}, Iteracje: {iteracje_losowy}, Czas: {czas_losowy:.4f}s")



#Algorytm tabu z cofnieciem
    wynik_tabu, blad_tabu, iteracje_tabu, czas_tabu, historia = algorytm_tabu(
        siatka_start, siatka_wzor, max_iteracje=10
    )
    print("Tabu (bez ograniczeń):")
    drukuj_siatke(wynik_tabu)
    print(f"Błędy: {blad_tabu}, Iteracje: {iteracje_tabu}, Czas: {czas_tabu:.4f}s")

    if len(historia) > 1:
        print("\nCofnięcie o 1 krok:")
        drukuj_siatke(historia[-2])




#Algorytm wyzarzania
    wynik_sa, blad_sa, iteracje_sa, czas_sa = algorytm_symulowanego_wyzarzania(
        siatka_start, siatka_wzor, T_start=100.0, T_koniec=0.1, alfa=0.95)

    print("Symulowane wyżarzanie:")
    drukuj_siatke(wynik_sa)
    print(f"Błędy: {blad_sa}, Iteracje: {iteracje_sa}, Czas: {czas_sa:.4f}s")


#algorytm genetyczny
    wynik_ga, blad_ga, iteracje_ga, czas_ga, historia_ga = algorytm_genetyczny(
        siatka_wzor,
        populacja_rozmiar=500,
        pokolenia=100,
        elita=True,
        metoda_krzyzowania="uniform",
        metoda_mutacji="losowa",
        warunek_stop="brak_poprawy"
    )

    print("Algorytm genetyczny:")
    drukuj_siatke(wynik_ga)
    print(f"Błędy: {blad_ga}, Iteracje: {iteracje_ga}, Czas: {czas_ga:.4f}s")


#Wyniki i porownania czasow
    wyniki = [
        ("Wspinaczka klasyczna", blad_klasyczny, iteracje_klasyczny, czas_klasyczny),
        ("Wspinaczka losowa", blad_losowy, iteracje_losowy, czas_losowy),
        ("Tabu (bez ograniczeń)", blad_tabu, iteracje_tabu, czas_tabu),
        ("Symulowane wyżarzanie", blad_sa, iteracje_sa, czas_sa),
    ]

    porownaj_metody(wyniki)

    generuj_wykres_zbieznosci(siatka_start, siatka_wzor, liczba_prob=100)







if __name__ == "__main__":
    main()
