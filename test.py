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
# print(text)
# print(len(text))
text2 = re.sub(r"\[\[.*?\]\]", "", text2)
text2 = re.sub(r"\s+", " ", text2)

nlp = spacy.load("pl_core_news_lg")


def get_emotion(text):
    xyz = nlp(text)
    sentences = list(xyz.sents)
    sentence_emotions = []

    for sentence in sentences:
        sentence_text = sentence.text
        emotion = model.get_emotion(sentence_text).replace("<pad>", "")
        sentence_emotions.append(emotion)

    return sentence_emotions


dataframe = pd.DataFrame()
dataframe["text"] = [text]

dataframe2 = pd.DataFrame()
dataframe2["text"] = [text2]


dataframe["emotions"] = dataframe["text"].apply(get_emotion)
dataframe2["emotions"] = dataframe2["text"].apply(get_emotion)

sentence_dataframes = []
sentence_dataframes.append(dataframe)
sentence_dataframes.append(dataframe2)

# for i in range(0, len(sentence_dataframes)):
#     df = sentence_dataframes[i].copy()
#     df["sentences"] = df["text"].apply(
#         lambda line: [sent.text for sent in nlp(line).sents]
#     )
#     df["emotion"] = df["sentences"].apply(
#         lambda sentence_list: [
#             model.get_emotion(str(sentence)).replace("<pad>", "")
#             for sentence in sentence_list
#             if len(sentence) < 512
#         ]
#     )
#     sentence_dataframes.append(df)

print(sentence_dataframes)

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
plt.figure(figsize=(10, 5))
plt.bar(emotions, counts)
plt.show()
