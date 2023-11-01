import model
import os
import pandas as pd
import re
import matplotlib.pyplot as plt
import datetime
import spacy


class Reading_files:
    def __init__(self, path, case):
        self.path = path
        self.case = case
        self.nlp = spacy.load("pl_core_news_lg")

    def __repr__(self) -> str:
        return "Klasa do operacji na plikach tekstowych"

    def read_txt_file(self):
        """
        Zwraca listę dataframe'ów, gdzie każdy dataframe to jeden plik tekstowy -> kolumny: speech_id, text. Przykład: [df1, df2, df3, ...]
        """
        dataframes = []
        rest_metadata = []
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
                                new_df = self.extract_more_info(old_root=root)
                                dataframes.append(df)
                                rest_metadata.append(new_df)
        return dataframes, rest_metadata

    def extract_more_info(self, old_root):
        """
        Tworzenie dataframe'a z dodatkowymi informacjami o pliku tekstowym. Przykład: [df1, df2, df3, ...] -> df
        """
        temporary_df = pd.DataFrame()
        for root, dir, files in os.walk(old_root):
            for file in files:
                if file.endswith(".tsv"):
                    tsv_filename = os.path.join(root, file)
                    with open(tsv_filename, "r", encoding="utf-8") as f:
                        temporary_df = pd.read_csv(f, sep="\t")

        return temporary_df

    def combining_all_to_one_dataframe(self):
        """
        Łączy wszystkie dataframe'y w jeden. Przykład: [df1, df2, df3, ...] -> df
        """
        dataframes, rest_metadata = self.read_txt_file()
        combined_df = pd.DataFrame()
        combined_dataframes = []

        if len(dataframes) == len(rest_metadata):
            for i in range(0, len(dataframes)):
                combined_df = pd.concat([dataframes[i], rest_metadata[i]], axis=1)
                combined_dataframes.append(combined_df)

        return combined_dataframes

    def cleaning_text(self):
        dataframes = self.combining_all_to_one_dataframe()
        cleaned_dataframes = []

        for i in range(0, len(dataframes)):
            df = dataframes[i].copy()
            df["text"] = df["text"].apply(
                lambda line: re.sub(r"\[\[.*?\]\]", "", str(line))
            )
            cleaned_dataframes.append(df)

        return cleaned_dataframes

    def getting_emotion(self):
        """
        Zwraca dataframe z emocjami. Przykład: df -> df
        """
        # jak na razie testowo
        dataframes = self.cleaning_text()
        completed_dataframes = []

        for i in range(0, len(dataframes)):
            df = dataframes[i].copy()
            df["emotion"] = df["text"].apply(
                lambda line: model.get_emotion(str(line)).replace("<pad>", "")
                if len(line) < 512
                else "NaN"
            )
            completed_dataframes.append(df)

        return completed_dataframes

    # def getting_emotion_per_sentence(self):
    #     dataframes = self.cleaning_text()
    #     sentence_emotions = []

    #     for i in range(0, len(dataframes)):
    #         df = dataframes[i].copy()
    #         sentences = df["text"].apply(
    #             lambda line: [sent.text for sent in self.nlp(line).sents]
    #         )
    #         emotions = [
    #             model.get_emotion(str(sentence)).replace("<pad>", "")
    #             for sentence_list in sentences
    #             for sentence in sentence_list
    #             if len(str(sentence)) < 512
    #         ]
    #         sentence_emotions.append(emotions)

    #     return sentence_emotions

    def draw_emotion_frequency(self):
        current_time = datetime.datetime.now()
        current_time = current_time.replace(microsecond=0)
        current_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        save_path = "./Plots"

        # dataframes_sentence = self.getting_emotion_per_sentence()
        dataframes_speech = self.getting_emotion()

        emotions_sentence = []
        covid_emotions_sentence = []

        emotions_speech = []
        covid_emotions_speech = []

        # for wypowiedz in dataframes_sentence:
        #     for sentence_emotions in wypowiedz:
        #         emotions_sentence += sentence_emotions

        # for wypowiedz in dataframes_sentence:
        #     for sentence_emotions in wypowiedz:
        #         covid_emotions_sentence += (
        #             sentence_emotions if wypowiedz["Subcorpus"] == "COVID" else None
        #         )
        # # Usuwanie None z listy
        # covid_emotions_sentence = [
        #     emotion for emotion in covid_emotions_sentence if emotion is not None
        # ]

        for wypowiedz in dataframes_speech:
            emotions_speech += list(wypowiedz["emotion"])

        for wypowiedz in dataframes_speech:
            emotions_speech += list(wypowiedz["emotion"])
            covid_emotions_speech += [
                emotion
                for emotion in list(wypowiedz["emotion"])
                if "COVID" in wypowiedz["Subcorpus"]
            ]

        # Tworzenie subplots
        plt.figure(figsize=(16, 9), dpi=300)
        plt.subplots_adjust(hspace=0.5)

        # Subplot dla emocji na poziomie zdań
        # plt.subplot(2, 2, 1)
        # plt.hist(emotions_sentence, bins=20)
        # plt.xlabel("Emotion (Per Sentence)")
        # plt.ylabel("Frequency")
        # plt.title("Emotion Frequency Distribution (Per Sentence)")
        # plt.grid(True)

        # Subplot dla emocji na poziomie wypowiedzi
        plt.subplot(1, 2, 1)
        plt.hist(emotions_speech, bins=7)
        plt.xlabel("Emotion (Per Speech)")
        plt.ylabel("Frequency")
        plt.title("Emotion Frequency Distribution (Per Speech)")
        # plt.grid(True)

        plt.subplot(1, 2, 2)
        plt.hist(covid_emotions_speech, bins=7)
        plt.xlabel("Emotion COVID (Per Speech)")
        plt.ylabel("Frequency")
        plt.title("Emotion COVID Frequency Distribution (Per Speech)")
        # plt.grid(True)

        # plt.subplot(2, 2, 4)
        # plt.hist(covid_emotions_sentence, bins=20)
        # plt.xlabel("Emotion COVID (Per Sentence)")
        # plt.ylabel("Frequency")
        # plt.title("Emotion COVID Frequency Distribution (Per Sentence)")
        # plt.grid(True)

        if save_path:
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            save_file = os.path.join(
                save_path,
                "emotion_frequency_plot_{}.png".format(current_time),
            )
            plt.savefig(save_file)
