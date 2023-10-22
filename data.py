import model
import os
import pandas as pd


class Reading_files:
    def __init__(self, path):
        self.path = path

    def __repr__(self) -> str:
        return "Klasa do operacji na plikach tekstowych"

    def read_txt_file(self):
        df = None
        for root, dirs, files in os.walk(self.path):
            for dir in dirs:
                if dir == 2022:  # jak na razie testujemy dla 2022 roku
                    for root, dir, files in os.walk(os.path.join(dir, self.path)):
                        for file in files:
                            if file.endswith(".txt"):
                                df = pd.read_csv(
                                    os.path.join(root, file), sep=" ", header=None
                                )
                            else:
                                continue
        return df

    def write_to_txt(self, df):
        """
        Zapis dataframe do pliku txt, jak na razie na jednym folderze
        """
        test_file = "test.txt"
        df = self.read_txt_file()
        df.to_csv(test_file, sep=" ", header=None, index=False)

    def combine_text_and_emotion(self):
        """
        Wstępnie stworzony słownik = {tekst: emocja} -> może się przydać do wizualizacji
        """
        combined_list = []
        text_lines, gender_info = self.read_file()

        for i, line in enumerate(text_lines):
            cleaned_line = line.strip("# text").strip()
            emotion = model.get_emotion(cleaned_line)

            # Jeśli dostępna jest informacja o płci mówcy, dodaj ją do listy
            if i < len(gender_info):
                gender = gender_info[i]
                combined_list.append([cleaned_line, emotion, gender])
            else:
                combined_list.append([cleaned_line, emotion])

        return combined_list

    def combine_all_to_one_dictionary(self):
        """
        Słownik master, gdzie kluczem jest nazwa pliku, a wartością lista zawierająca tekst, emocję i płeć mówcy:
        {nazwa_pliku: [["tekst", emocja, płeć mówcy], ["tekst", emocja, płeć mówcy], ...]}
        """
        master_dictionary = {}

        # Pobieranie nazwy pliku
        file_name = os.path.basename(self.path)

        master_dictionary[file_name] = self.combine_text_and_emotion()

        return master_dictionary
