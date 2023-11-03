import re
import spacy
import model
import pandas as pd

text = "Serdecznie witam pierwszą osobę w państwie - pana prezydenta Rzeczypospolitej Polskiej. [[Długotrwałe oklaski]] Kłaniam się bardzo nisko i dziękuję za przybycie wszystkim dostojnym gościom. Swoją obecnością uświetniacie państwo tę inaugurację. Wielkie to dla nas uhonorowanie. [[Oklaski]] Pozdrawiam szanownych posłów. Witam słuchających w mediach. [[Oklaski]] Proszę o powstanie i uczczenie chwilą ciszy zmarłych, którzy służyli ojczyźnie. [[Chwila ciszy]] Dziękuję bardzo. Proszę prezydenta Rzeczypospolitej Andrzeja Dudę o wygłoszenie orędzia na 1. posiedzeniu Sejmu VIII kadencji."

text = re.sub(r"\[\[.*?\]\]", "", text)
text = re.sub(r"\s+", " ", text)
# print(text)
# print(len(text))

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

dataframe["emotions"] = dataframe["text"].apply(get_emotion)

print(dataframe)
