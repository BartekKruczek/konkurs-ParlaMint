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
