import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import time

start = time.time()

# Wczytaj dane z dużego excela
# Zakładam, że plik ten znajduje się w bieżącym katalogu, możesz dostosować ścieżkę do pliku
excel_path = "final_file.xlsx"
df = pd.read_excel(excel_path)

# Jeśli masz wartości tekstowe w kolumnie "emotions", możesz je przekształcić na listę emocji
emotions_list = df["emotion"].str.split(",").explode().str.strip()

# Wybierz 6 najczęstszych emocji
top_emotions = emotions_list.value_counts().nlargest(6).index

# Utwórz subplot z dwoma wierszami i jedną kolumną
fig = make_subplots(
    rows=2,
    cols=1,
    subplot_titles=["Top 6 Emotions for COVID", "Top 6 Emotions Overall"],
)

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
fig.write_image("emotions_chart_subplot.jpg", format="jpg")


# Utwórz subplot z dwoma wierszami i jedną kolumną dla przypadku "WAR"
fig_war = make_subplots(
    rows=2,
    cols=1,
    subplot_titles=["Top 6 Emotions for WAR", "Top 6 Emotions Overall for WAR"],
)

# Filtruj dane, aby uwzględnić tylko te emocje dla przypadku "WAR"
war_df = df[df["Subcorpus"] == "WAR"]
war_filtered_emotions = (
    war_df["emotion"]
    .str.split(",")
    .explode()
    .str.strip()[
        war_df["emotion"].str.split(",").explode().str.strip().isin(top_emotions)
    ]
)

# Filtruj dane, aby uwzględnić tylko te emocje ogólnie
war_filtered_emotions_overall = emotions_list[emotions_list.isin(top_emotions)]

# Utwórz wykres słupkowy dla emocji w przypadku "WAR"
bar_war = px.bar(
    war_filtered_emotions.value_counts(),
    x=war_filtered_emotions.value_counts().index,
    y=war_filtered_emotions.value_counts().values,
    labels={"x": "Emotions", "y": "Count"},
    title="Top 6 Emotions for WAR",
).update_traces(
    textposition="outside",
    text=war_filtered_emotions.value_counts().values,
    hoverinfo="x+text",
)

# Utwórz wykres słupkowy dla emocji ogólnie dla przypadku "WAR"
bar_overall_war = px.bar(
    war_filtered_emotions_overall.value_counts(),
    x=war_filtered_emotions_overall.value_counts().index,
    y=war_filtered_emotions_overall.value_counts().values,
    labels={"x": "Emotions", "y": "Count"},
    title="Top 6 Emotions Overall for WAR",
).update_traces(
    textposition="outside",
    text=war_filtered_emotions_overall.value_counts().values,
    hoverinfo="x+text",
)

# Dodaj wykresy do subplotu dla przypadku "WAR"
fig_war.add_trace(bar_war.data[0], row=1, col=1)
fig_war.add_trace(bar_overall_war.data[0], row=2, col=1)

# Zmień rozmiar obrazu na 1920x1080 pikseli dla przypadku "WAR"
fig_war.update_layout(width=1920, height=1080)

# Dostosuj tytuły osi dla przypadku "WAR"
fig_war.update_xaxes(title_text="Emotions", row=2, col=1)
fig_war.update_yaxes(title_text="Count", row=2, col=1)

# Zapisz wykres jako plik JPG dla przypadku "WAR"
fig_war.write_image("emotions_chart_subplot_war.jpg", format="jpg")

end = time.time()
print("Time elapsed:", end - start)
