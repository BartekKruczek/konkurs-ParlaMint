import model
import os
import pandas as pd


class Reading_files:
    def __init__(self, path):
        self.path = path

    def __repr__(self) -> str:
        return "Klasa do operacji na plikach tekstowych"

    def read_txt_file(self):
        """
        Zwraca listę dataframe'ów, gdzie każdy dataframe to jeden plik tekstowy -> kolumny: speech_id, text. Przykład: [df1, df2, df3, ...]
        """
        dataframes = []
        df = pd.DataFrame()
        for root, dirs, files in os.walk(self.path):
            for dir in dirs:
                for root, dir, files in os.walk(os.path.join(self.path, dir)):
                    for file in files:
                        if file.endswith(".txt"):
                            with open(
                                os.path.join(root, file), "r", encoding="utf-8"
                            ) as f:
                                df = pd.read_csv(
                                    f,
                                    sep="\t",
                                    header=None,
                                    names=["speech_id", "text", "file_name"],
                                )
                                df["file_name"] = file
                                new_df = self.extract_more_info(
                                    df=df,
                                    old_root=root,
                                )  # funkcja do wglądu poniżej
                                dataframes.append(new_df)
        return dataframes

    def combine_text_and_emotion(self):
        """
        Lista zawierająca tekst i emocję. Przykład: [["tekst", emocja], ["tekst", emocja], ...]. Jest problem, bo wczytywane zdania są za długie.
        """
        combined_list = []
        dataframes = self.read_txt_file()

        for df in dataframes:
            for index, row in df.iterrows():
                text = row["text"]
                if len(text) < 512:
                    emotion = model.get_emotion(text)
                    combined_list.append([text, emotion])
                else:
                    continue

        return combined_list

    def extract_more_info(self, df, old_root):
        """
        Jak na razie próbna funkcja, będzie pobierała płeć, wiek i godność mówcy. Wszystko bedzie zapisywane w dataframe'ie.
        """
        new_df = pd.DataFrame()
        for root, dir, files in os.walk(old_root):
            for file in files:
                if file.endswith(".tsv"):
                    tsv_filename = os.path.join(root, file)
                    with open(tsv_filename, "r", encoding="utf-8") as f:
                        temporary_df = pd.read_csv(f, sep="\t")
                        new_df = pd.concat([df, temporary_df["Speaker_gender"]])

        return new_df
