# Load model directly
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from googletrans import Translator

translator = Translator()


tokenizer = AutoTokenizer.from_pretrained(
    "glombardo/misogynistic-statements-classification-model"
)
model = AutoModelForSequenceClassification.from_pretrained(
    "glombardo/misogynistic-statements-classification-model"
)

# tekst nie ma na celu obrażać kobiet, jest wykorzystywany w celach testowych i naukowych
text = "Chcę cię zgwałcić wredna suko"
translated_text = translator.translate(text, src="pl", dest="es").text
print(translated_text)

input_ids = tokenizer.encode(text, return_tensors="pt")
output = model(input_ids)

if (
    output.logits.softmax(dim=1)[0].tolist()[0]
    > output.logits.softmax(dim=1)[0].tolist()[1]
):
    print("Not misogynistic")
else:
    print("Misogynistic")
