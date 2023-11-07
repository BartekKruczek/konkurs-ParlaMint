from transformers import pipeline
from deep_translator import GoogleTranslator

classifier = pipeline(
    task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None
)

sentences = "Serdecznie witam pierwszą osobę w państwie - pana prezydenta Rzeczypospolitej Polskiej. [[Długotrwałe oklaski]] Kłaniam się bardzo nisko i dziękuję za przybycie wszystkim dostojnym gościom. Swoją obecnością uświetniacie państwo tę inaugurację. Wielkie to dla nas uhonorowanie. [[Oklaski]] Pozdrawiam szanownych posłów. Witam słuchających w mediach. [[Oklaski]] Proszę o powstanie i uczczenie chwilą ciszy zmarłych, którzy służyli ojczyźnie. [[Chwila ciszy]] Dziękuję bardzo. Proszę prezydenta Rzeczypospolitej Andrzeja Dudę o wygłoszenie orędzia na 1. posiedzeniu Sejmu VIII kadencji."
translated_sentences = GoogleTranslator(source="auto", target="en").translate(sentences)

model_outputs = classifier(translated_sentences)
print(model_outputs[0][0])
print(model_outputs[0][0]["label"])
# produces a list of dicts for each of the labels
