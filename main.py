from data import Reading_files
from plotting_data import Plotting_data

"""
Jak na razie przetestowane dla jednego pliku. Dodać funkcjonalość dla wielu plików. Naprawić wyświetlanie emocji "anger". Pomyśleć nad innymi sposobami wizualizacji danych.
"""


def main():
    print("Please wait...")

    # test wczytywania plików
    path = "./ParlaMint-PL.conllu/ParlaMint-PL_2015-11-12-sejm-01-1.conllu"
    file_reading = Reading_files(path=path)

    # tworzenie słownika z tekstem i emocją
    file_reading.combine_text_and_emotion()

    # zbieranie wszystkich słowników w jeden słownik
    master_dictionary = file_reading.combine_all_to_one_dictionary()
    print(master_dictionary)

    # inicjalizacja klasy do wizualizacji danych
    plotting_data = Plotting_data(master_dictionary=master_dictionary)

    # tworznie chmury emocji
    plotting_data.plotting_emotion_cloud()

    print("Done!")


try:
    if __name__ == "__main__":
        main()
except Exception as e:
    print(e)
