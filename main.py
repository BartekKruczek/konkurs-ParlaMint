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

    file_reading.read_txt_file()

    # tworzenie słownika z tekstem i emocją
    # file_reading.combine_text_and_emotion()

    # zbieranie wszystkich słowników w jeden słownik
    # master_dictionary = file_reading.combine_all_to_one_dictionary()
    # print(master_dictionary)

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
