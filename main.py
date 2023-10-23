from data import Reading_files
from plotting_data import Plotting_data
import sys

"""
Jak na razie przetestowane dla jednego pliku. Dodać funkcjonalość dla wielu plików. Naprawić wyświetlanie emocji "anger". Pomyśleć nad innymi sposobami wizualizacji danych.
"""


def main():
    print("Please wait...", file=open("logs.txt", "a", encoding="utf-8"))

    # test wczytywania plików
    path = "./ParlaMint-PL.txt"
    file_reading = Reading_files(path=path)

    # sprawdzanie czyszczenia
    print(file_reading.cleaning_text(), file=open("logs.txt", "a", encoding="utf-8"))

    # klasyfikacja emocji, na razie testowo
    # file_reading.getting_emotion()

    # inicjalizacja klasy do wizualizacji danych
    # plotting_data = Plotting_data(master_dictionary=master_dictionary)

    # tworznie chmury emocji
    # plotting_data.plotting_emotion_cloud()

    print("Done!", file=open("logs.txt", "a", encoding="utf-8"))

    sys.stdout = open("logs.txt", "a", encoding="utf-8")
    sys.stdout.close()


try:
    if __name__ == "__main__":
        main()
except Exception as e:
    print(e)
