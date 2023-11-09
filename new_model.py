from transformers import pipeline
from deep_translator import GoogleTranslator

classifier = pipeline(
    task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None
)


def get_emotion(text):
    translated_sentence = GoogleTranslator(source="auto", target="en").translate(text)
    model_outputs = classifier(translated_sentence)

    if len(translated_sentence) > 4999:
        return "NaN"
    else:
        return model_outputs[0][0]["label"]
