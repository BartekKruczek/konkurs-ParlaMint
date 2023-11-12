from transformers import pipeline
from deep_translator import GoogleTranslator

classifier = pipeline(
    task="text-classification",
    model="SamLowe/roberta-base-go_emotions",
    top_k=None,
    max_length=5000,
    truncation=True,
)


def get_emotion(text):
    translated_sentence = GoogleTranslator(source="auto", target="en").translate(text)
    model_outputs = classifier(translated_sentence)

    if len(translated_sentence) < 1024:
        return model_outputs[0][0]["label"]
    else:
        return "NaN"
