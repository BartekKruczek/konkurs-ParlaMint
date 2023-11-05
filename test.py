# import re
# import spacy
# import model
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# text = "Serdecznie witam pierwszą osobę w państwie - pana prezydenta Rzeczypospolitej Polskiej. [[Długotrwałe oklaski]] Kłaniam się bardzo nisko i dziękuję za przybycie wszystkim dostojnym gościom. Swoją obecnością uświetniacie państwo tę inaugurację. Wielkie to dla nas uhonorowanie. [[Oklaski]] Pozdrawiam szanownych posłów. Witam słuchających w mediach. [[Oklaski]] Proszę o powstanie i uczczenie chwilą ciszy zmarłych, którzy służyli ojczyźnie. [[Chwila ciszy]] Dziękuję bardzo. Proszę prezydenta Rzeczypospolitej Andrzeja Dudę o wygłoszenie orędzia na 1. posiedzeniu Sejmu VIII kadencji."
# text2 = "Serdecznie witam pierwszą osobę w państwie - pana prezydenta Rzeczypospolitej Polskiej. [[Długotrwałe oklaski]] Kłaniam się bardzo nisko i dziękuję za przybycie wszystkim dostojnym gościom. Swoją obecnością uświetniacie państwo tę inaugurację. Wielkie to dla nas uhonorowanie. [[Oklaski]] Pozdrawiam szanownych posłów. Witam słuchających w mediach. [[Oklaski]] Proszę o powstanie i uczczenie chwilą ciszy zmarłych, którzy służyli ojczyźnie. [[Chwila ciszy]] Dziękuję bardzo. Proszę prezydenta Rzeczypospolitej Andrzeja Dudę o wygłoszenie orędzia na 1. posiedzeniu Sejmu VIII kadencji."

# text = re.sub(r"\[\[.*?\]\]", "", text)
# text = re.sub(r"\s+", " ", text)
# # print(text)
# # print(len(text))
# text2 = re.sub(r"\[\[.*?\]\]", "", text2)
# text2 = re.sub(r"\s+", " ", text2)

# nlp = spacy.load("pl_core_news_lg")


# def get_emotion(text):
#     xyz = nlp(text)
#     sentences = list(xyz.sents)
#     sentence_emotions = []

#     for sentence in sentences:
#         blocks = []
#         test_sentence_list_length_below_512 = []
#         sentence_text = sentence.text
#         test_sentence_list_length_below_512.append(
#             sentence_text
#         )  # dodawanie zdań do listy, tworzenie bloku
#         count = 0
#         for elem in test_sentence_list_length_below_512:
#             count += len(elem)
#             if count > 512:
#                 blocks.append(test_sentence_list_length_below_512)
#                 test_sentence_list_length_below_512 = []
#         print(count)
#         for elem in test_sentence_list_length_below_512:
#             print(elem)
#         for block in blocks:
#             # emotion = model.get_emotion(sentence_text).replace("<pad>", "")
#             emotion = model.get_emotion(block).replace("<pad>", "")
#             sentence_emotions.append(emotion)

#     return sentence_emotions


# dataframe = pd.DataFrame()
# dataframe["text"] = [text]

# dataframe2 = pd.DataFrame()
# dataframe2["text"] = [text2]


# dataframe["emotions"] = dataframe["text"].apply(get_emotion)
# dataframe2["emotions"] = dataframe2["text"].apply(get_emotion)

# sentence_dataframes = []
# sentence_dataframes.append(dataframe)
# sentence_dataframes.append(dataframe2)

# print(sentence_dataframes)

# emotions = []
# for emotions_list in sentence_dataframes:
#     for element in emotions_list["emotions"]:
#         for x in element:
#             emotions.append(x)
# print(emotions)

# emotions_count = {}
# for emotion in emotions:
#     if emotion in emotions_count:
#         emotions_count[emotion] += 1
#     else:
#         emotions_count[emotion] = 1
# print(emotions_count)

# # deleting key from emotions_count dictionary
# # del emotions_count["Tak"]

# emotions, counts = zip(*emotions_count.items())

# # generating colors for each emotion
# colors = []
# for i in range(0, len(emotions)):
#     colors.append(
#         np.random.rand(
#             3,
#         )
#     )


# plt.figure(figsize=(16, 9), dpi=300)
# plt.bar(emotions, counts, color=colors)
# plt.show()

import re
import spacy
import model
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

text = "Serdecznie witam pierwszą osobę w państwie - pana prezydenta Rzeczypospolitej Polskiej. [[Długotrwałe oklaski]] Kłaniam się bardzo nisko i dziękuję za przybycie wszystkim dostojnym gościom. Swoją obecnością uświetniacie państwo tę inaugurację. Wielkie to dla nas uhonorowanie. [[Oklaski]] Pozdrawiam szanownych posłów. Witam słuchających w mediach. [[Oklaski]] Proszę o powstanie i uczczenie chwilą ciszy zmarłych, którzy służyli ojczyźnie. [[Chwila ciszy]] Dziękuję bardzo. Proszę prezydenta Rzeczypospolitej Andrzeja Dudę o wygłoszenie orędzia na 1. posiedzeniu Sejmu VIII kadencji."
text2 = "Serdecznie witam pierwszą osobę w państwie - pana prezydenta Rzeczypospolitej Polskiej. [[Długotrwałe oklaski]] Kłaniam się bardzo nisko i dziękuję za przybycie wszystkim dostojnym gościom. Swoją obecnością uświetniacie państwo tę inaugurację. Wielkie to dla nas uhonorowanie. [[Oklaski]] Pozdrawiam szanownych posłów. Witam słuchających w mediach. [[Oklaski]] Proszę o powstanie i uczczenie chwilą ciszy zmarłych, którzy służyli ojczyźnie. [[Chwila ciszy]] Dziękuję bardzo. Proszę prezydenta Rzeczypospolitej Andrzeja Dudę o wygłoszenie orędzia na 1. posiedzeniu Sejmu VIII kadencji."


def get_emotion(text):
    xyz = nlp(text)
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


nlp = spacy.load("pl_core_news_lg")

dataframe = pd.DataFrame()
dataframe["text"] = [text]

dataframe2 = pd.DataFrame()
dataframe2["text"] = [text2]

dataframe["emotions"] = dataframe["text"].apply(get_emotion)
dataframe2["emotions"] = dataframe2["text"].apply(get_emotion)

sentence_dataframes = []
sentence_dataframes.append(dataframe)
sentence_dataframes.append(dataframe2)

emotions = []
for emotions_list in sentence_dataframes:
    for element in emotions_list["emotions"]:
        for x in element:
            emotions.append(x)

emotions_count = {}
for emotion in emotions:
    if emotion in emotions_count:
        emotions_count[emotion] += 1
    else:
        emotions_count[emotion] = 1

emotions, counts = zip(*emotions_count.items())

colors = []
for i in range(0, len(emotions)):
    colors.append(
        np.random.rand(
            3,
        )
    )

plt.figure(figsize=(16, 9), dpi=300)
plt.bar(emotions, counts, color=colors)
plt.show()
