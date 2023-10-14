from data import Reading_files


def main():
    print("Please wait...")
    # test wczytywania plików
    path = "./ParlaMint-PL.conllu/ParlaMint-PL_2015-11-12-sejm-01-1.conllu"
    file_reading = Reading_files(path=path)

    # text_lines = file_reading.read_file()
    # for line in text_lines:
    #     print(line.strip("# text").strip())

    # inicjalizacja modelu
    # for line in text_lines:
    #     print(model.get_emotion(line.strip("# text").strip()))

    print(file_reading.combine_text_and_emotion())
    print("Done!")


try:
    if __name__ == "__main__":
        main()
except Exception as e:
    print(e)
