# Load model directly
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from deep_translator import GoogleTranslator


tokenizer = AutoTokenizer.from_pretrained(
    "glombardo/misogynistic-statements-classification-model"
)
model = AutoModelForSequenceClassification.from_pretrained(
    "glombardo/misogynistic-statements-classification-model"
)

# tekst nie ma na celu obrażać kobiet, jest wykorzystywany w celach testowych i naukowych
text = "Jesteś najwredniejszym i najgłupszym facetem na świecie."

translated_text = GoogleTranslator(src="auto", target="es").translate(text)

input_ids = tokenizer.encode(text, return_tensors="pt")
output = model(input_ids)

if (
    output.logits.softmax(dim=1)[0].tolist()[0]
    > output.logits.softmax(dim=1)[0].tolist()[1]
):
    print("No")
else:
    print("Yes")
