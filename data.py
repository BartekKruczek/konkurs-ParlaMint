import model
import os


class Reading_files:
    def __init__(self, path):
        self.path = path

    def __repr__(self) -> str:
        return "Klasa do operacji na plikach tekstowych"

    def read_file(self):
        text_lines = []
        gender_info = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("# text"):
                    text_lines.append(line)
                if line.startswith("# speaker_gender"):
                    gender_info.append(line.split()[-1])
        return text_lines, gender_info

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
