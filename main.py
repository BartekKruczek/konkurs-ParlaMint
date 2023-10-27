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
    wanted_case = "COVID"
    file_reading = Reading_files(path=path, case=wanted_case)

    # rysoawnie wykresu częstości występowania emocji
    file_reading.draw_emotion_frequency()

    print("Done!", file=open("logs.txt", "a", encoding="utf-8"))

    sys.stdout = open("logs.txt", "a", encoding="utf-8")
    sys.stdout.close()


try:
    if __name__ == "__main__":
        main()
except Exception as e:
    print(e)
