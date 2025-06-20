







def parsuj(s: str) -> list[list[int]]:
    return [list(map(int, czesc.split(','))) for czesc in s[1:-1].split('","')]#map zwraca obiekt
#Usuń pierwszy i ostatni znak → s[1:-1],Podziel tekst na kawałki → .split('","'),Podziel liczby w środku → .split(',')
#Zamień teksty na liczby → map(int, ...),Złóż to w listę list → [list(...) for ...]




def permutacje(wartosci, wiersz, przesuniecie=0):
    if not wartosci:
        yield []
        return
    aktualna, *reszta = wartosci
    maks_start = len(wiersz) - sum(reszta) - len(reszta) - aktualna + 1#bez jedynki pomijamy ostatnie miejsce
    for i in range(maks_start):
        if 1 in wiersz[i:i + aktualna]:
            continue
        prefix = [1] * (i + przesuniecie) + [2] * aktualna
        for sufix in permutacje(reszta, wiersz[i + aktualna + 1:], 1):
            yield prefix + sufix#Zwracasz cały wiersz jako jedno możliwe rozwiązanie





def rozwiaz_wiersz(wartosci, wiersz):
    dlugosc = len(wiersz)
    kandydaci = [
        p + [1] * (dlugosc - len(p))
        for p in permutacje(wartosci, wiersz)
        if all(r == 0 or r == v for r, v in zip(wiersz, p + [1] * (dlugosc - len(p))))
    ]
    if not kandydaci:
        return wiersz
    return [kandydaci[0][i] if all(k[i] == kandydaci[0][i] for k in kandydaci) else 0 for i in range(dlugosc)]

def rozwiaz(wiersze_wartosci, kolumny_wartosci, siatka):
    zmiana = True
    wysokosc, szerokosc = len(siatka), len(siatka[0])
    while zmiana:
        zmiana = False
        for y, wartosci_wiersza in enumerate(wiersze_wartosci):
            wiersz = rozwiaz_wiersz(wartosci_wiersza, siatka[y])
            for x, komorka in enumerate(wiersz):
                if komorka and siatka[y][x] != komorka:
                    siatka[y][x] = komorka
                    zmiana = True
        for x, wartosci_kolumny in enumerate(kolumny_wartosci):
            kolumna = rozwiaz_wiersz(wartosci_kolumny, [siatka[y][x] for y in range(wysokosc)])
            for y, komorka in enumerate(kolumna):
                if komorka and siatka[y][x] != komorka:
                    siatka[y][x] = komorka
                    zmiana = True

def drukuj_siatke(siatka):
        for wiersz in siatka:
            print("".join("- *"[komorka] for komorka in wiersz))


