import csv
import os

PLIK_SAL = "sale.csv"
PLIK_REZERWACJI = "rezerwacje.csv"


def wczytaj_sale():
    sale = []
    with open(PLIK_SAL, newline="", encoding="utf-8") as plik:
        czytnik = csv.DictReader(plik)
        for wiersz in czytnik:
            sale.append(wiersz)
    return sale


def wczytaj_rezerwacje():
    if not os.path.exists(PLIK_REZERWACJI):
        return []

    rezerwacje = []
    with open(PLIK_REZERWACJI, newline="", encoding="utf-8") as plik:
        czytnik = csv.DictReader(plik)
        for wiersz in czytnik:
            rezerwacje.append(wiersz)
    return rezerwacje


def zapisz_rezerwacje(rezerwacje):
    naglowki = ["id", "id_sali", "data", "godzina_od", "godzina_do", "osoba"]
    with open(PLIK_REZERWACJI, "w", newline="", encoding="utf-8") as plik:
        pisarz = csv.DictWriter(plik, fieldnames=naglowki)
        pisarz.writeheader()
        pisarz.writerows(rezerwacje)


def czy_sala_wolna(id_sali, data, godzina_od, godzina_do, rezerwacje):
    for r in rezerwacje:
        if r["id_sali"] != id_sali or r["data"] != data:
            continue
        if godzina_od < r["godzina_do"] and godzina_do > r["godzina_od"]:
            return False
    return True


def nowy_numer_rezerwacji(rezerwacje):
    if not rezerwacje:
        return 1
    numery = [int(r["id"]) for r in rezerwacje]
    return max(numery) + 1


def pokaz_sale():
    sale = wczytaj_sale()
    print("\nDostepne sale:")
    for s in sale:
        print(f"{s['id']} - {s['nazwa']} ({s['lokalizacja']}), miejsc: {s['liczba_miejsc']}")


def pokaz_rezerwacje():
    rezerwacje = wczytaj_rezerwacje()
    if not rezerwacje:
        print("\nBrak rezerwacji.")
        return

    print("\nLista rezerwacji:")
    for r in rezerwacje:
        print(f"{r['id']}: sala {r['id_sali']}, {r['data']} {r['godzina_od']}-{r['godzina_do']}, {r['osoba']}")


def dodaj_rezerwacje():
    pokaz_sale()
    id_sali = input("Podaj numer sali: ")
    data = input("Podaj date (RRRR-MM-DD): ")
    godzina_od = input("Godzina rozpoczecia (GG:MM): ")
    godzina_do = input("Godzina zakonczenia (GG:MM): ")
    osoba = input("Imie i nazwisko osoby rezerwujacej: ")

    rezerwacje = wczytaj_rezerwacje()

    if not czy_sala_wolna(id_sali, data, godzina_od, godzina_do, rezerwacje):
        print("Sala jest juz zajeta w tym terminie.")
        return

    nowa_rezerwacja = {
        "id": nowy_numer_rezerwacji(rezerwacje),
        "id_sali": id_sali,
        "data": data,
        "godzina_od": godzina_od,
        "godzina_do": godzina_do,
        "osoba": osoba,
    }
    rezerwacje.append(nowa_rezerwacja)
    zapisz_rezerwacje(rezerwacje)
    print("Rezerwacja zostala dodana.")


def anuluj_rezerwacje():
    pokaz_rezerwacje()
    numer = input("Podaj numer rezerwacji do anulowania: ")
    rezerwacje = wczytaj_rezerwacje()
    nowa_lista = [r for r in rezerwacje if r["id"] != numer]

    if len(nowa_lista) == len(rezerwacje):
        print("Nie znaleziono rezerwacji o takim numerze.")
        return

    zapisz_rezerwacje(nowa_lista)
    print("Rezerwacja zostala anulowana.")


def menu():
    while True:
        print("\n--- System rezerwacji sal szkoleniowych ---")
        print("1. Pokaz sale")
        print("2. Pokaz rezerwacje")
        print("3. Dodaj rezerwacje")
        print("4. Anuluj rezerwacje")
        print("5. Zakoncz")
        wybor = input("Wybierz opcje: ")

        if wybor == "1":
            pokaz_sale()
        elif wybor == "2":
            pokaz_rezerwacje()
        elif wybor == "3":
            dodaj_rezerwacje()
        elif wybor == "4":
            anuluj_rezerwacje()
        elif wybor == "5":
            print("Koniec programu.")
            break
        else:
            print("Nieprawidlowy wybor, sprobuj ponownie.")


if __name__ == "__main__":
    menu()
