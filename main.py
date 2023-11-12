from data import Reading_files
from plotting_data import Plotting_data

"""
Jak na razie przetestowane dla jednego pliku. Dodać funkcjonalość dla wielu plików. Naprawić wyświetlanie emocji "anger". Pomyśleć nad innymi sposobami wizualizacji danych.
"""


def main():
    print("Please wait...")

    # wczytywania plików
    path = "./ParlaMint-PL2.txt"
    file_reading = Reading_files(path=path)

    # test
    # file_reading.getting_emotion_new_model()

    # rysoawnie wykresu częstości występowania emocji
    # file_reading.draw_emotion_frequency()

    # wartość jeden = liczy emocje, wartość dwa = liczy mizoginię
    pomocnicza = 1

    file_reading.saving_to_csv(pomocnicza=pomocnicza)

    print("Done!")


try:
    if __name__ == "__main__":
        main()
except Exception as e:
    print(e)
