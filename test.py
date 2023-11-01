import pandas as pd

dic = {
    "emotion": ["happy", "sad", "angry"],
    "text": ["I am happy", "I am sad", "I am angry"],
    "Subcorpus": ["a", "b", "c"],
}
df = pd.DataFrame(dic)
print(df)
