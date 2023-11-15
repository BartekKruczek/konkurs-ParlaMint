import pandas as pd
import os
import plotly.express as px
import plotly.io as pio


def process_excel_file(file_path):
    # Sprawdź, czy plik istnieje
    if not os.path.isfile(file_path):
        print(f"Plik {file_path} nie istnieje.")
        return

    # Wczytaj wszystkie arkusze z pliku Excel
    try:
        excel_data = pd.read_excel(file_path, sheet_name=None)
    except Exception as e:
        print(f"Błąd podczas odczytu pliku {file_path}: {e}")
        return

    # Przetwarzaj każdy arkusz z pliku
    for sheet_name, df in excel_data.items():
        # Sprawdź, czy istnieje kolumna 'Subcorpus' i 'Emotion'
        if "Subcorpus" not in df.columns or "emotion" not in df.columns:
            # print(
            #     f"Arkusz {sheet_name} w pliku {file_path} nie zawiera wymaganych kolumn 'Subcorpus' lub 'Emotion'."
            # )
            continue

        # Filtruj wiersze, gdzie 'Subcorpus' zawiera słowo 'COVID'
        covid_rows = df[df["Subcorpus"].str.contains("COVID", case=False, na=False)]

        # Jeśli są wiersze związane z COVID, wypisz emocje z kolumny 'Emotion'
        if not covid_rows.empty:
            emotions = covid_rows["emotion"].value_counts()

            # Wygeneruj wykres słupkowy
            fig = px.bar(
                emotions,
                x=emotions.index,
                y=emotions.values,
                title=f"Emocje związane z COVID w arkuszu {sheet_name} pliku {file_path}",
            )
            # fig.show(renderer="svg")
            output_file_path = (
                f"wykres_{sheet_name}_{file_path.replace('.xlsx', '')}.png"
            )
            pio.write_image(
                fig, output_file_path, format="png", scale=4
            )  # Zmiana formatu i skali
            print(f"Zapisano wykres do pliku: {output_file_path}")
        # else:
        # print(
        #     f"Brak wierszy związanych z COVID w arkuszu {sheet_name} pliku {file_path}"
        # )


# Lista plików Excel do przetworzenia
excel_files = [
    "output_file_emocje_2023-11-13_09-44-35_Emo_2016.xlsx",
    "output_file_emocje_2023-11-14_12-16-44_Emo_2022.xlsx",
    "output_file_emocje_2023-11-15_01-16-17_Emo_2015.xlsx",
    "output_file_emocje_2023-11-15_05-56-11_Emo_2020.xlsx",
]  # Dodaj swoje pliki

# Przetwarzaj każdy plik z listy
print("Przetwarzanie plików...")
for file in excel_files:
    process_excel_file(file)
print("Przetwarzanie plików zakończone.")
