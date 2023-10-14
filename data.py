class Reading_files:
    def __init__(self, path):
        self.path = path

    def __repr__(self) -> str:
        return "Klasa do odczytu plików"

    def read_file(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return f.read()
