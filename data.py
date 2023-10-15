import model


class Reading_files:
    def __init__(self, path):
        self.path = path

    def __repr__(self) -> str:
        return "Klasa do odczytu plików"

    def read_file(self):
        text_lines = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("# text"):
                    text_lines.append(line)
        return text_lines

    def combine_text_and_emotion(self):
        """
        Wstępnie stworzony słownik = {tekst: emocja} -> może się przydać do wizualizacji
        """
        combined_dictionary = {}
        text_lines = self.read_file()

        for line in text_lines:
            cleaned_line = line.strip("# text").strip()
            emotion = model.get_emotion(cleaned_line)
            combined_dictionary[cleaned_line] = emotion

        # czyszczenie słownika
        combined_dictionary = {
            key.lstrip("= ").strip(): value.lstrip("<pad> ").strip()
            for key, value in combined_dictionary.items()
        }

        return combined_dictionary
