# Load model directly
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from deep_translator import GoogleTranslator
import pandas as pd


tokenizer = AutoTokenizer.from_pretrained(
    "glombardo/misogynistic-statements-classification-model"
)
model = AutoModelForSequenceClassification.from_pretrained(
    "glombardo/misogynistic-statements-classification-model"
)

# tekst nie ma na celu obrażać kobiet, jest wykorzystywany w celach testowych i naukowych
text = "Jesteś najwredniejszym i najgłupszym facetem na świecie."
df = pd.DataFrame()
df["text"] = [text]
text2 = "Jesteś najwredniejszą i najgłupszą kobietą na świecie."
df2 = pd.DataFrame()
df2["text"] = [text2]
dfl = []
dfl.append(df)
dfl.append(df2)

misoginic_df = []

for i in range(0, len(dfl)):
    df_copy = dfl[i].copy()
    text_from_df = df_copy["text"].to_string(index=False)
    # print(text_from_df)
    # print(type(text_from_df))
    translated_text = GoogleTranslator(src="auto", target="es").translate(text_from_df)

    input_ids = tokenizer.encode(text_from_df, return_tensors="pt")
    output = model(input_ids)

    if (
        output.logits.softmax(dim=1)[0].tolist()[0]
        > output.logits.softmax(dim=1)[0].tolist()[1]
    ):
        df_copy["misoginic"] = "No"
        misoginic_df.append(df_copy)
    else:
        df_copy["misoginic"] = "Yes"
        misoginic_df.append(df_copy)

for i in range(0, len(misoginic_df)):
    print(misoginic_df[i]["misoginic"])
