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
