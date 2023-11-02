import pandas as pd

dic = {
    "emotion": ["happy", "sad", "angry"],
    "text": ["I am happy", "I am sad", "I am angry"],
    "Subcorpus": ["a", "b", "c"],
}
df = pd.DataFrame(dic)

dic2 = {
    "emotion": ["happy", "sad", "angry"],
    "text": ["I am happy", "I am sad", "I am angry"],
    "Subcorpus": ["c", "a", "b"],
}
df2 = pd.DataFrame(dic2)

df_list = [df, df2]
print(df_list)


emotions_speech = []
covid_emotions_speech = []

for wypowiedz in df_list:
    emotions_speech += list(wypowiedz["emotion"])
    covid_emotions_speech += [
        emotion
        for emotion, subcorpus in zip(
            list(wypowiedz["emotion"]), list(wypowiedz["Subcorpus"])
        )
        if "a" in subcorpus
    ]


print(emotions_speech)
print(covid_emotions_speech)

for x, y in zip(emotions_speech, covid_emotions_speech):
    print(type(x), type(y))
