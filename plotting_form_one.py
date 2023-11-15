import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import time

# Wczytaj dane z dużego excela
# Zakładam, że plik ten znajduje się w bieżącym katalogu, możesz dostosować ścieżkę do pliku
excel_path = "final_file.xlsx"


def covid(path):
    df = pd.read_excel(path)
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

    fear_count_covid = covid_filtered_emotions.value_counts().get("fear", 0)
    total_emotions_covid = len(covid_filtered_emotions)
    percent_fear_covid = (fear_count_covid / total_emotions_covid) * 100

    # Filtruj dane, aby uwzględnić tylko te emocje ogólnie
    filtered_emotions = emotions_list[emotions_list.isin(top_emotions)]

    # Utwórz subplot z dwoma wierszami i jedną kolumną
    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=["Top 6 Emotions for WAR", "Top 6 Emotions Overall"],
    )

    # Utwórz wykres słupkowy dla emocji w przypadku "COVID"
    bar_covid = px.bar(
        covid_filtered_emotions.value_counts(),
        x=covid_filtered_emotions.value_counts().index,
        y=covid_filtered_emotions.value_counts().values,
        labels={"x": "Emotions", "y": "Count"},
        title="Top 6 Emotions for COVID",
    ).update_traces(
        textposition="outside",
        text=covid_filtered_emotions.value_counts().values,
        hoverinfo="x+text",
    )

    # Utwórz wykres słupkowy dla emocji ogólnie
    bar_overall = px.bar(
        filtered_emotions.value_counts(),
        x=filtered_emotions.value_counts().index,
        y=filtered_emotions.value_counts().values,
        labels={"x": "Emotions", "y": "Count"},
        title="Top 6 Emotions Overall",
    ).update_traces(
        textposition="outside",
        text=filtered_emotions.value_counts().values,
        hoverinfo="x+text",
    )

    # Dodaj wykresy do subplotu
    fig.add_trace(bar_covid.data[0], row=1, col=1)
    fig.add_trace(bar_overall.data[0], row=2, col=1)

    # Zmień rozmiar obrazu na 1920x1080 pikseli
    fig.update_layout(width=1920, height=1080)

    # Dostosuj tytuły osi
    fig.update_xaxes(title_text="Emotions", row=2, col=1)
    fig.update_yaxes(title_text="Count", row=2, col=1)

    # Zapisz wykres jako plik JPG
    fig.write_image("emotions_chart_subplot_covid.jpg", format="jpg")

    return percent_fear_covid


def war(path):
    df = pd.read_excel(path)
    # Jeśli masz wartości tekstowe w kolumnie "emotions", możesz je przekształcić na listę emocji
    emotions_list = df["emotion"].str.split(",").explode().str.strip()

    # Wybierz 6 najczęstszych emocji
    top_emotions = emotions_list.value_counts().nlargest(6).index

    # Filtruj dane, aby uwzględnić tylko te emocje dla przypadku "COVID"
    covid_df = df[df["Subcorpus"] == "War"]
    covid_filtered_emotions = (
        covid_df["emotion"]
        .str.split(",")
        .explode()
        .str.strip()[
            covid_df["emotion"].str.split(",").explode().str.strip().isin(top_emotions)
        ]
    )

    fear_count_covid = covid_filtered_emotions.value_counts().get("fear", 0)
    total_emotions_covid = len(covid_filtered_emotions)
    percent_fear_covid = (fear_count_covid / total_emotions_covid) * 100

    # Filtruj dane, aby uwzględnić tylko te emocje ogólnie
    filtered_emotions = emotions_list[emotions_list.isin(top_emotions)]

    # Utwórz subplot z dwoma wierszami i jedną kolumną
    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=["Top 6 Emotions for War", "Top 6 Emotions Overall"],
    )

    # Utwórz wykres słupkowy dla emocji w przypadku "COVID"
    bar_covid = px.bar(
        covid_filtered_emotions.value_counts(),
        x=covid_filtered_emotions.value_counts().index,
        y=covid_filtered_emotions.value_counts().values,
        labels={"x": "Emotions", "y": "Count"},
        title="Top 6 Emotions for War",
    ).update_traces(
        textposition="outside",
        text=covid_filtered_emotions.value_counts().values,
        hoverinfo="x+text",
    )

    # Utwórz wykres słupkowy dla emocji ogólnie
    bar_overall = px.bar(
        filtered_emotions.value_counts(),
        x=filtered_emotions.value_counts().index,
        y=filtered_emotions.value_counts().values,
        labels={"x": "Emotions", "y": "Count"},
        title="Top 6 Emotions Overall",
    ).update_traces(
        textposition="outside",
        text=filtered_emotions.value_counts().values,
        hoverinfo="x+text",
    )

    # Dodaj wykresy do subplotu
    fig.add_trace(bar_covid.data[0], row=1, col=1)
    fig.add_trace(bar_overall.data[0], row=2, col=1)

    # Zmień rozmiar obrazu na 1920x1080 pikseli
    fig.update_layout(width=1920, height=1080)

    # Dostosuj tytuły osi
    fig.update_xaxes(title_text="Emotions", row=2, col=1)
    fig.update_yaxes(title_text="Count", row=2, col=1)

    # Zapisz wykres jako plik JPG
    fig.write_image("emotions_chart_subplot_war.jpg", format="jpg")

    return percent_fear_covid


start = time.time()

percent_covid = covid(excel_path)
percent_war = war(excel_path)

end = time.time()
print("Time: ", end - start)
print("Percent of fear in COVID: ", percent_covid)
print("Percent of fear in WAR: ", percent_war)
