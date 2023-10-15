from data import Reading_files


def main():
    print("Please wait...")

    # test wczytywania plików
    path = "./ParlaMint-PL.conllu/ParlaMint-PL_2015-11-12-sejm-01-1.conllu"
    file_reading = Reading_files(path=path)

    # tworzenie słownika z tekstem i emocją
    file_reading.combine_text_and_emotion()

    # zbieranie wszystkich słowników w jeden słownik
    print(file_reading.combine_all_to_one_dictionary())

    print("Done!")


try:
    if __name__ == "__main__":
        main()
except Exception as e:
    print(e)
