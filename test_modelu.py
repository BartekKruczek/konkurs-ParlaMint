from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained(
    "mrm8488/t5-base-finetuned-emotion", use_fast=False
)

model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-emotion")


def get_emotion(text):
    input_ids = tokenizer.encode(text + "</s>", return_tensors="pt")

    output = model.generate(input_ids=input_ids, max_length=2)

    dec = [tokenizer.decode(ids) for ids in output]
    label = dec[0]
    return label


text = "I am very happy today!"
emotion = get_emotion(text).replace("<pad> ", "")
print(emotion)
