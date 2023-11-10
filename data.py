import model
import new_model
import os
import pandas as pd
import re
import matplotlib.pyplot as plt
import datetime
import spacy
import numpy as np
from deep_translator import GoogleTranslator
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class Reading_files:
    def __init__(self, path):
        self.path = path
        self.nlp = spacy.load("pl_core_news_lg")

    def __repr__(self) -> str:
        return "Klasa do operacji na plikach tekstowych"

    def read_txt_file(self):
        """
        Zwraca listę dataframe'ów, gdzie każdy dataframe to jeden plik tekstowy -> kolumny: speech_id, text. Przykład: [df1, df2, df3, ...]
        """
        print("Starting reading txt files...")
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
        # print("Starting extracting more info...")
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
        print("Starting combining all to one dataframe...")
        dataframes, rest_metadata = self.read_txt_file()
        combined_df = pd.DataFrame()
        combined_dataframes = []

        if len(dataframes) == len(rest_metadata):
            for i in range(0, len(dataframes)):
                combined_df = pd.concat([dataframes[i], rest_metadata[i]], axis=1)
                combined_dataframes.append(combined_df)

        return combined_dataframes

    def cleaning_text(self):
        print("Starting cleaning text...")
        dataframes = self.combining_all_to_one_dataframe()
        cleaned_dataframes = []

        for i in range(0, len(dataframes)):
            df = dataframes[i].copy()
            df["text"] = df["text"].apply(
                lambda line: re.sub(r"\[\[.*?\]\]", "", str(line))
            )
            df["text"] = df["text"].apply(lambda line: re.sub(r"\s+", " ", str(line)))
            cleaned_dataframes.append(df)

        return cleaned_dataframes

    def getting_emotion(self):
        """
        Zwraca listę dataframe z emocjami. Przykład: df -> df
        """
        print("Starting getting emotion...")
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

    def getting_emotion_per_block(self):
        print("Starting getting emotion per block...")

        # tu zlicza emocje w blokach
        def block(text):
            xyz = self.nlp(text)
            sentences = list(xyz.sents)
            sentence_emotions = []
            current_block = ""
            for sentence in sentences:
                if len(current_block) + len(sentence.text) + 1 <= 512:
                    if current_block:
                        current_block += ". " + sentence.text
                    else:
                        current_block = sentence.text
                else:
                    emotion = model.get_emotion(current_block).replace("<pad>", "")
                    sentence_emotions.append(emotion)
                    current_block = sentence.text
            if current_block:
                emotion = model.get_emotion(current_block).replace("<pad>", "")
                sentence_emotions.append(emotion)
            return sentence_emotions

        # jak na razie po staremu
        dataframes = self.cleaning_text()
        sentence_dataframes = []

        for i in range(0, len(dataframes)):
            df = dataframes[i].copy()
            df["emotion"] = df["text"].apply(block)
            sentence_dataframes.append(df)

        return sentence_dataframes

    def checking_if_is_misogynistic(self):
        print("Starting checking if is misogynistic...")
        # inicializacja modelu
        tokenizer = AutoTokenizer.from_pretrained(
            "glombardo/misogynistic-statements-classification-model"
        )
        model = AutoModelForSequenceClassification.from_pretrained(
            "glombardo/misogynistic-statements-classification-model"
        )
        # sprawdza czy wypowiedź jest mizoginistyczna, automatycznie tłumaczenie na hiszpański
        dataframes_list = self.cleaning_text()
        misogynistic_dataframes = []

        for i in range(0, len(dataframes_list)):
            df_copy = dataframes_list[i].copy()
            text_from_df = df_copy["text"].to_string(index=False)

            # tłumaczenie z wykorzystaniem GoogleTranslator
            translated_text = GoogleTranslator(src="auto", target="es").translate(
                text_from_df
            )

            input_ids = tokenizer.encode(translated_text, return_tensors="pt")
            output = model(input_ids)

            if (
                output.logits.softmax(dim=1)[0].tolist()[0]
                > output.logits.softmax(dim=1)[0].tolist()[1]
            ):
                df_copy["misoginic"] = "No"
                misogynistic_dataframes.append(df_copy)
            else:
                df_copy["misoginic"] = "Yes"
                misogynistic_dataframes.append(df_copy)

        return misogynistic_dataframes

    def getting_emotion_new_model(self):
        """Zwraca listę dataframów z emocjami, nowy model"""
        print("Starting getting emotion new model...")
        dataframes = self.cleaning_text()
        completed_dataframes = []

        for i in range(0, len(dataframes)):
            df = dataframes[i].copy()
            # text_from_df = df["text"].to_string(index=False)
            # print(type(text_from_df))
            # df["emotion"] = new_model.get_emotion(text_from_df) # tutaj przekazujemy cały blok tekstu zamiast jednej linijki :(
            df["emotion"] = df["text"].apply(
                lambda line: new_model.get_emotion(line) if len(line) < 512 else "NaN"
            )
            completed_dataframes.append(df)

        return completed_dataframes

    def draw_emotion_frequency(self):
        current_time = datetime.datetime.now()
        current_time = current_time.replace(microsecond=0)
        current_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        save_path = "./Plots"

        # ładowanie danych
        # dataframes_sentence = self.getting_emotion_per_block()
        # dataframes_speech = self.getting_emotion()
        datafames_misogynistic = self.checking_if_is_misogynistic()
        dataframes_speech_new_model = self.getting_emotion_new_model()

        emotions_sentence = []
        covid_emotions_sentence = []

        emotions_speech = []
        covid_emotions_speech = []

        misogynistic_list = []

        emotions_sentence_new_model = []
        covid_emotions_sentence_new_model = []

        # for wypowiedz in dataframes_sentence:
        #     emotions_sentence += list(wypowiedz["emotion"])

        # for dataframe in dataframes_sentence:
        #     covid_emotions_sentence += list(
        #         dataframe.loc[
        #             dataframe["Subcorpus"].str.contains("COVID", na=False), "emotion"
        #         ]
        #     )

        # for wypowiedz in dataframes_speech:
        #     emotions_speech += list(wypowiedz["emotion"])

        # for dataframe in dataframes_speech:
        #     covid_emotions_speech += list(
        #         dataframe.loc[
        #             dataframe["Subcorpus"].str.contains("COVID", na=False), "emotion"
        #         ]
        #     )

        for dataframe in datafames_misogynistic:
            misogynistic_list += list(dataframe["misoginic"])

        for wypowiedz in dataframes_speech_new_model:
            emotions_sentence_new_model += list(wypowiedz["emotion"])

        for dataframe in dataframes_speech_new_model:
            covid_emotions_sentence_new_model += list(
                dataframe.loc[
                    dataframe["Subcorpus"].str.contains("COVID", na=False), "emotion"
                ]
            )

        # zliczanie emocji
        # emotions_count_speech = {}
        # for emotion in emotions_speech:
        #     if emotion in emotions_count_speech:
        #         emotions_count_speech[emotion] += 1
        #     else:
        #         emotions_count_speech[emotion] = 1
        # del emotions_count_speech["Tak"]

        # emotions_count_speech_covid = {}
        # for emotion in covid_emotions_speech:
        #     if emotion in emotions_count_speech_covid:
        #         emotions_count_speech_covid[emotion] += 1
        #     else:
        #         emotions_count_speech_covid[emotion] = 1
        # del emotions_count_speech_covid["Tak"]

        # emotions_count_sentence = {}
        # for emotion in emotions_sentence:
        #     if emotion in emotions_count_sentence:
        #         emotions_count_sentence[emotion] += 1
        #     else:
        #         emotions_count_sentence[emotion] = 1
        # del emotions_count_speech_covid["Tak"]

        # emotions_count_sentence_covid = {}
        # for emotion in covid_emotions_sentence:
        #     if emotion in emotions_count_sentence_covid:
        #         emotions_count_sentence_covid[emotion] += 1
        #     else:
        #         emotions_count_sentence_covid[emotion] = 1
        # del emotions_count_speech_covid["Tak"]

        # zliczanie mizoginistycznych wypowiedzi
        misogynistic_count = {}
        for misogynistic in misogynistic_list:
            if misogynistic in misogynistic_count:
                misogynistic_count[misogynistic] += 1
            else:
                misogynistic_count[misogynistic] = 1

        # zliczanie emocji nowy model
        emotions_count_sentence_new_model = {}
        for emotion in emotions_sentence_new_model:
            if emotion in emotions_count_sentence_new_model:
                emotions_count_sentence_new_model[emotion] += 1
            else:
                emotions_count_sentence_new_model[emotion] = 1

        emotions_count_sentence_covid_new_model = {}
        for emotion in covid_emotions_sentence_new_model:
            if emotion in emotions_count_sentence_covid_new_model:
                emotions_count_sentence_covid_new_model[emotion] += 1
            else:
                emotions_count_sentence_covid_new_model[emotion] = 1

        # rozpakowanie słowników
        # speech_emotions, speech_count = zip(*emotions_count_speech.items())
        # speech_emotions_covid, speech_count_covid = zip(
        #     *emotions_count_speech_covid.items()
        # )

        # sentence_emotions, sentence_count = zip(*emotions_count_sentence.items())
        # sentence_emotions_covid, sentence_count_covid = zip(
        #     *emotions_count_sentence_covid.items()
        # )

        misogynic, misogynic_count = zip(*misogynistic_count.items())

        speech_emotions_new_model, speech_count_new_model = zip(
            *emotions_count_sentence_new_model.items()
        )
        speech_emotions_covid_new_model, speech_count_covid_new_model = zip(
            *emotions_count_sentence_covid_new_model.items()
        )

        # generowanie kolorów
        # speech_colors = []
        # for i in range(0, len(speech_emotions)):
        #     speech_colors.append(
        #         np.random.rand(
        #             3,
        #         )
        #     )

        # speech_colors_covid = []
        # for i in range(0, len(speech_emotions_covid)):
        #     speech_colors_covid.append(
        #         np.random.rand(
        #             3,
        #         )
        #     )

        # sentence_colors = []
        # for i in range(0, len(sentence_emotions)):
        #     sentence_colors.append(
        #         np.random.rand(
        #             3,
        #         )
        #     )

        # sentence_colors_covid = []
        # for i in range(0, len(sentence_emotions_covid)):
        #     sentence_colors_covid.append(
        #         np.random.rand(
        #             3,
        #         )
        #     )

        # Tworzenie subplots
        plt.figure(figsize=(16, 9), dpi=600)
        plt.subplots_adjust(hspace=0.5)

        plt.subplot(1, 2, 1)
        plt.bar(speech_emotions_new_model, speech_count_new_model)
        plt.xlabel("Emotion (Per Speech)")
        plt.ylabel("Frequency")
        plt.title("Emotion Frequency Distribution (Per Speech)")

        plt.subplot(1, 2, 2)
        plt.bar(speech_emotions_covid_new_model, speech_count_covid_new_model)
        plt.xlabel("Emotion COVID (Per Speech)")
        plt.ylabel("Frequency")
        plt.title("Emotion COVID Frequency Distribution (Per Speech)")

        # plt.subplot(2, 2, 3)
        # plt.bar(sentence_emotions, sentence_count, color=sentence_colors)
        # plt.xlabel("Emotion (Per Block)")
        # plt.ylabel("Frequency")
        # plt.title("Emotion Frequency Distribution (Per Block)")

        # plt.subplot(2, 2, 4)
        # plt.bar(
        #     sentence_emotions_covid, sentence_count_covid, color=sentence_colors_covid
        # )
        # plt.xlabel("Emotion COVID (Per Block)")
        # plt.ylabel("Frequency")
        # plt.title("Emotion COVID Frequency Distribution (Per Block)")

        plt.subplot(2, 2, 3)
        plt.bar(misogynic, misogynic_count)
        plt.xlabel("Misogynic")
        plt.ylabel("Frequency")
        plt.title("Misogynic Frequency Distribution")

        if save_path:
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            save_file = os.path.join(
                save_path,
                "emotion_frequency_plot_{}.png".format(current_time),
            )
            plt.savefig(save_file)
