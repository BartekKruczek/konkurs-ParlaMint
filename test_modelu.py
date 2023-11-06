from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained(
    "glombardo/misogynistic-statements-classification-model"
)

model = AutoModelWithLMHead.from_pretrained(
    "glombardo/misogynistic-statements-classification-model"
)

text = "Test text"


def get_emotion(text):
    input_ids = tokenizer.encode(text + "</s>", return_tensors="pt")

    output = model.generate(input_ids=input_ids, max_length=2)

    dec = [tokenizer.decode(ids) for ids in output]
    label = dec[0]
    return label
