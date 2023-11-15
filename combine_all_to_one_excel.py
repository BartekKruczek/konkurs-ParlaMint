import pandas as pd
from openpyxl import load_workbook
import time

start = time.time()
# Utwórz pustą ramkę danych
final_dataframe = pd.DataFrame()

# Lista plików XLSX
files = [
    "output_file_emocje_2023-11-13_09-44-35_Emo_2016.xlsx",
    "output_file_emocje_2023-11-14_12-16-44_Emo_2022.xlsx",
    "output_file_emocje_2023-11-15_01-16-17_Emo_2015.xlsx",
    "output_file_emocje_2023-11-15_05-56-11_Emo_2020.xlsx",
]

# Pętla po każdym pliku
for file in files:
    # Utwórz pustą ramkę danych dla danego pliku
    file_dataframe = pd.DataFrame()

    # Wczytaj plik XLSX
    xls = pd.ExcelFile(file)

    # Pętla po arkuszach w pliku
    for sheet_name in xls.sheet_names:
        # Wczytaj arkusz do ramki danych
        sheet_dataframe = pd.read_excel(file, sheet_name)

        # Dołącz arkusz do ramki danych dla pliku
        file_dataframe = pd.concat([file_dataframe, sheet_dataframe], ignore_index=True)

    # Dołącz ramkę danych dla pliku do ramki danych końcowej
    final_dataframe = pd.concat([final_dataframe, file_dataframe], ignore_index=True)

# Zapisz ramkę danych końcową do nowego pliku XLSX
final_dataframe.to_excel("final_file.xlsx", index=False)
end = time.time()
print(end - start)
