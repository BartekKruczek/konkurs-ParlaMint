#
import re
import spacy
import model
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

text = "Serdecznie witam pierwszą osobę w państwie - pana prezydenta Rzeczypospolitej Polskiej. [[Długotrwałe oklaski]] Kłaniam się bardzo nisko i dziękuję za przybycie wszystkim dostojnym gościom. Swoją obecnością uświetniacie państwo tę inaugurację. Wielkie to dla nas uhonorowanie. [[Oklaski]] Pozdrawiam szanownych posłów. Witam słuchających w mediach. [[Oklaski]] Proszę o powstanie i uczczenie chwilą ciszy zmarłych, którzy służyli ojczyźnie. [[Chwila ciszy]] Dziękuję bardzo. Proszę prezydenta Rzeczypospolitej Andrzeja Dudę o wygłoszenie orędzia na 1. posiedzeniu Sejmu VIII kadencji."
text2 = "Serdecznie witam pierwszą osobę w państwie - pana prezydenta Rzeczypospolitej Polskiej. [[Długotrwałe oklaski]] Kłaniam się bardzo nisko i dziękuję za przybycie wszystkim dostojnym gościom. Swoją obecnością uświetniacie państwo tę inaugurację. Wielkie to dla nas uhonorowanie. [[Oklaski]] Pozdrawiam szanownych posłów. Witam słuchających w mediach. [[Oklaski]] Proszę o powstanie i uczczenie chwilą ciszy zmarłych, którzy służyli ojczyźnie. [[Chwila ciszy]] Dziękuję bardzo. Proszę prezydenta Rzeczypospolitej Andrzeja Dudę o wygłoszenie orędzia na 1. posiedzeniu Sejmu VIII kadencji."

text = re.sub(r"\[\[.*?\]\]", "", text)
text = re.sub(r"\s+", " ", text)

text2 = re.sub(r"\[\[.*?\]\]", "", text2)
text2 = re.sub(r"\s+", " ", text2)

nlp = spacy.load("pl_core_news_lg")


def split_text_into_blocks(text, max_length=64):
    blocks = []
    current_block = ""

    for sentence in text.split(". "):
        if len(current_block) + len(sentence) + 1 <= max_length:
            if current_block:
                current_block += ". "
            current_block += sentence
        else:
            blocks.append(current_block)
            current_block = sentence

    if current_block:
        blocks.append(current_block)

    return blocks


def get_emotion_for_text(text):
    blocks = split_text_into_blocks(text)
    emotions = []

    for block in blocks:
        emotion = model.get_emotion(block).replace("<pad>", "")
        emotions.append(emotion)

    return emotions


dataframe = pd.DataFrame()
dataframe["text"] = [text]

dataframe2 = pd.DataFrame()
dataframe2["text"] = [text2]

dataframe["emotions"] = dataframe["text"].apply(get_emotion_for_text)
dataframe2["emotions"] = dataframe2["text"].apply(get_emotion_for_text)

sentence_dataframes = []
sentence_dataframes.append(dataframe)
sentence_dataframes.append(dataframe2)

emotions = []
for emotions_list in sentence_dataframes:
    for element in emotions_list["emotions"]:
        for x in element:
            emotions.append(x)
print(emotions)

emotions_count = {}
for emotion in emotions:
    if emotion in emotions_count:
        emotions_count[emotion] += 1
    else:
        emotions_count[emotion] = 1
print(emotions_count)

emotions, counts = zip(*emotions_count.items())

colors = [np.random.rand(3) for _ in emotions]

plt.figure(figsize=(16, 9), dpi=300)
plt.bar(emotions, counts, color=colors)
plt.show()
