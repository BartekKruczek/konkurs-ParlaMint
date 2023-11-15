import pandas as pd
import plotly.express as px

# Wczytaj dane z dużego excela
# Zakładam, że plik ten znajduje się w bieżącym katalogu, możesz dostosować ścieżkę do pliku
excel_path = "final_file.xlsx"
df = pd.read_excel(excel_path)

# Sprawdź kolumnę "Subcorpus" i wybierz wiersze, gdzie wartość to "COVID"
covid_df = df[df["Subcorpus"] == "COVID"]

# Jeśli masz wartości tekstowe w kolumnie "emotions", możesz je przekształcić na listę emocji
emotions_list = covid_df["emotion"].str.split(",").explode().str.strip()

# Wybierz 6 najczęstszych emocji
top_emotions = emotions_list.value_counts().nlargest(6).index

# Filtruj dane, aby uwzględnić tylko te emocje
filtered_emotions = emotions_list[emotions_list.isin(top_emotions)]

# Utwórz wykres słupkowy za pomocą biblioteki Plotly Express
fig = px.bar(
    filtered_emotions.value_counts(),
    x=filtered_emotions.value_counts().index,
    y=filtered_emotions.value_counts().values,
    labels={"x": "Emotions", "y": "Count"},
    title='Top 6 Emotions Distribution for Subcorpus containing "COVID"',
)

# Zapisz wykres jako plik JPG
fig.write_image("emotions_chart.jpg", width=1920, height=1080)
