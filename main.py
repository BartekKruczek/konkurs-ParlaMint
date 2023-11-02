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

    # test
    cleaned = file_reading.cleaning_text()
    print(cleaned[0].head(10), file=open("logs.txt", "a", encoding="utf-8"))
    print(
        type(cleaned[0]["Subcorpus"][0]), file=open("logs.txt", "a", encoding="utf-8")
    )
    emotions_speech = []
    for wypowiedz in cleaned:
        emotions_speech += list(wypowiedz["speech_id"])
    print(emotions_speech[0], file=open("logs.txt", "a", encoding="utf-8"))
    print(type(emotions_speech[0]), file=open("logs.txt", "a", encoding="utf-8"))

    covid_emotions_speech = []
    for wypowiedz in cleaned:
        emotions_speech += list(wypowiedz["speech_id"])
        covid_emotions_speech += [
            emotion
            for emotion, subcorpus in zip(
                list(wypowiedz["speech_id"]), list(wypowiedz["Subcorpus"])
            )
            if "COVID" in subcorpus
        ]

    # rysoawnie wykresu częstości występowania emocji
    # x, y = file_reading.draw_emotion_frequency()
    # for a, b in zip(x, y):
    #     print(type(a), type(b), file=open("logs.txt", "a", encoding="utf-8"))

    print("Done!", file=open("logs.txt", "a", encoding="utf-8"))

    sys.stdout = open("logs.txt", "a", encoding="utf-8")
    sys.stdout.close()


try:
    if __name__ == "__main__":
        main()
except Exception as e:
    print(e)
