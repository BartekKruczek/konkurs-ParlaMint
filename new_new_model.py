from deep_translator import GoogleTranslator
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")
model = AutoModelForSequenceClassification.from_pretrained("SamLowe/roberta-base-go_emotions")


def get_emotion(text):
    translated_sentence = GoogleTranslator(source="auto", target="en").translate(text)
    input = tokenizer.encode(translated_sentence, return_tensors="pt")
    model_outputs = model.generate(input)

    if len(translated_sentence) < 1024:
        return model_outputs[0][0]["label"]
    else:
        return "NaN"
