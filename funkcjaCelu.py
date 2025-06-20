import copy
import random


def porownaj_siatki(s1, s2):
    bledy = 0
    for y in range(len(s1)):
        for x in range(len(s1[0])):#nie ma [0], bo s1 to lista wierszy — więc len(s1) to liczba wierszy.
            if s1[y][x] != s2[y][x]:#chcemy policzyć ile jest kolumn w jednym wierszu
                bledy += 1
    return bledy

def generuj_sasiedztwo(siatka):
    wysokosc = len(siatka)
    szerokosc = len(siatka[0])# sprawdzmy tylko pierwszy bo reszta ma tyle samo
    sasiedzi = []

    for _ in range(10):  # 10 sasiadow nie, nie wazne ktory
        nowa = copy.deepcopy(siatka)
        y = random.randint(0, wysokosc - 1)#wybierasz a b
        x = random.randint(0, szerokosc - 1)

        # Zamień tylko 1 ↔ 2
        if nowa[y][x] == 1:
            nowa[y][x] = 2
        elif nowa[y][x] == 2:
            nowa[y][x] = 1

        sasiedzi.append(nowa)

    return sasiedzi

def generuj_losowa_siatke(wysokosc, szerokosc):
    return [[random.choice([1, 2]) for _ in range(szerokosc)] for _ in range(wysokosc)]#for _ in range(szerokosc)tworzy 1 wiersz,(wysokosc)	tworzy wszystkie wiersze (całą siatkę)