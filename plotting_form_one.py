import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

# Wczytaj dane z dużego excela
# Zakładam, że plik ten znajduje się w bieżącym katalogu, możesz dostosować ścieżkę do pliku
excel_path = "final_file.xlsx"
df = pd.read_excel(excel_path)

# Jeśli masz wartości tekstowe w kolumnie "emotions", możesz je przekształcić na listę emocji
emotions_list = df["emotion"].str.split(",").explode().str.strip()

# Wybierz 6 najczęstszych emocji
top_emotions = emotions_list.value_counts().nlargest(6).index

# Filtruj dane, aby uwzględnić tylko te emocje dla przypadku "COVID"
covid_df = df[df["Subcorpus"] == "COVID"]
covid_filtered_emotions = (
    covid_df["emotion"]
    .str.split(",")
    .explode()
    .str.strip()[
        covid_df["emotion"].str.split(",").explode().str.strip().isin(top_emotions)
    ]
)

# Filtruj dane, aby uwzględnić tylko te emocje ogólnie
filtered_emotions = emotions_list[emotions_list.isin(top_emotions)]

# Utwórz subplot z dwoma wierszami i jedną kolumną
fig = make_subplots(
    rows=2,
    cols=1,
    subplot_titles=["Top 6 Emotions for COVID", "Top 6 Emotions Overall"],
)

# Utwórz wykres słupkowy dla emocji w przypadku "COVID"
fig.add_trace(
    px.bar(
        covid_filtered_emotions.value_counts(),
        x=covid_filtered_emotions.value_counts().index,
        y=covid_filtered_emotions.value_counts().values,
        labels={"x": "Emotions", "y": "Count"},
        title="Top 6 Emotions for COVID",
    ).data[0],
    row=1,
    col=1,
)

# Utwórz wykres słupkowy dla emocji ogólnie
fig.add_trace(
    px.bar(
        filtered_emotions.value_counts(),
        x=filtered_emotions.value_counts().index,
        y=filtered_emotions.value_counts().values,
        labels={"x": "Emotions", "y": "Count"},
        title="Top 6 Emotions Overall",
    ).data[0],
    row=2,
    col=1,
)

# Zmień rozmiar obrazu na 1920x1080 pikseli
fig.update_layout(width=1920, height=1080)

# Zapisz wykres jako plik JPG
fig.write_image("emotions_chart_subplot.jpg", format="jpg")
