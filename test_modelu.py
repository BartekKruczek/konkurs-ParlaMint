import new_model
from deep_translator import GoogleTranslator
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# test wstępny
# sentences = "Serdecznie witam pierwszą osobę w państwie - pana prezydenta Rzeczypospolitej Polskiej. [[Długotrwałe oklaski]] Kłaniam się bardzo nisko i dziękuję za przybycie wszystkim dostojnym gościom. Swoją obecnością uświetniacie państwo tę inaugurację. Wielkie to dla nas uhonorowanie. [[Oklaski]] Pozdrawiam szanownych posłów. Witam słuchających w mediach. [[Oklaski]] Proszę o powstanie i uczczenie chwilą ciszy zmarłych, którzy służyli ojczyźnie. [[Chwila ciszy]] Dziękuję bardzo. Proszę prezydenta Rzeczypospolitej Andrzeja Dudę o wygłoszenie orędzia na 1. posiedzeniu Sejmu VIII kadencji."
# translated_sentences = GoogleTranslator(source="auto", target="en").translate(sentences)

# model_outputs = classifier(translated_sentences)
# print(model_outputs[0][0])
# print(model_outputs[0][0]["label"])


# test końcowej funkcji, dlaczego nie działa
dataframes = []
df1 = pd.DataFrame(
    {
        "text": [
            "Serdecznie witam pierwszą osobę w państwie - pana prezydenta Rzeczypospolitej Polskiej. [[Długotrwałe oklaski]] Kłaniam się bardzo nisko i dziękuję za przybycie wszystkim dostojnym gościom. Swoją obecnością uświetniacie państwo tę inaugurację. Wielkie to dla nas uhonorowanie. [[Oklaski]] Pozdrawiam szanownych posłów. Witam słuchających w mediach. [[Oklaski]] Proszę o powstanie i uczczenie chwilą ciszy zmarłych, którzy służyli ojczyźnie. [[Chwila ciszy]] Dziękuję bardzo. Proszę prezydenta Rzeczypospolitej Andrzeja Dudę o wygłoszenie orędzia na 1. posiedzeniu Sejmu VIII kadencji."
        ]
    }
)
df1.loc[len(df1)] = [
    "Proszę o powstanie i uczczenie chwilą ciszy zmarłych, którzy służyli ojczyźnie. [[Chwila ciszy]]"
]
df2 = pd.DataFrame(
    {
        "text": [
            "Dziękuję bardzo. Proszę prezydenta Rzeczypospolitej Andrzeja Dudę o wygłoszenie orędzia na 1. posiedzeniu Sejmu VIII kadencji."
        ]
    }
)
dataframes.append(df1)
dataframes.append(df2)

test_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam pulvinar urna a ligula tristique, eu tincidunt odio euismod. Sed vel congue odio. Integer vestibulum, ex id efficitur posuere, justo lacus pharetra sem, ac elementum libero purus id ligula. Etiam ultricies, felis ut fringilla volutpat, nulla velit ultrices neque, nec dictum quam turpis vel metus. Ut et sollicitudin elit, ut tristique elit. Vivamus lacinia sodales neque, eget vestibulum elit venenatis vel. Integer euismod elit vel felis ultrices, id tincidunt mauris dignissim. Quisque bibendum dui in ligula egestas, vel tincidunt velit dictum. In hac habitasse platea dictumst. Curabitur vulputate quam id ex facilisis, nec vulputate sem pellentesque. Curabitur facilisis vel quam nec facilisis. Nunc in efficitur ligula. Ut nec orci eu ex malesuada auctor. Nunc vel sapien in purus fermentum dapibus. Aliquam a orci libero. Phasellus auctor ultrices leo, vel condimentum est consequat vel. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum ultrices felis vitae risus volutpat, eu cursus velit aliquam. Nullam in dui eu ex ultrices interdum. Quisque fermentum tincidunt quam, ac congue odio venenatis vel. Suspendisse potenti. Nullam non massa ut metus ullamcorper pharetra eu ac massa. Nam accumsan nisl et tincidunt sodales. Fusce at augue id libero congue fringilla. Nullam euismod fringilla lacus, nec efficitur elit malesuada vel. Morbi tincidunt auctor augue, sit amet consequat quam facilisis eu. Proin eleifend justo id leo vulputate volutpat. Aenean eu mauris id risus malesuada tristique nec ut velit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Ut imperdiet vel erat non euismod. Donec vitae purus at ligula ullamcorper euismod sit amet a elit. Integer eu tincidunt felis. Nulla facilisi. In hac habitasse platea dictumst. Nunc vehicula mi vel orci luctus, eu tempor elit varius. Fusce efficitur velit eu ex varius, at sodales nulla laoreet. Sed ut augue vel erat luctus sagittis. Curabitur eleifend vestibulum efficitur. Ut ut rhoncus ex. Vivamus facilisis libero at augue sagittis, nec feugiat nisl rhoncus. Vivamus sollicitudin, eros at fermentum tincidunt, metus arcu aliquet mi, vel pulvinar nisl quam eget ligula. Fusce nec tristique ligula. Sed ac dui eu ex tincidunt egestas vel vel libero. Duis non purus orci. Aliquam eu scelerisque elit. Suspendisse interdum lacus a arcu venenatis, ac dignissim justo laoreet. Etiam convallis, enim vel congue hendrerit, lacus sem ultrices libero, at vulputate arcu justo vitae dui. Ut sodales erat vel ante malesuada, non iaculis tortor dapibus. Integer ut hendrerit dui, nec consectetur sem. Fusce eget sem at odio sodales cursus. Integer nec semper justo. Vivamus euismod a metus vitae cursus. Aenean ac justo nec libero cursus dignissim. Integer vel odio vel urna vulputate finibus. Vestibulum eget est ex. Fusce suscipit leo nec efficitur congue. Phasellus ut malesuada justo, ut venenatis mauris. Sed efficitur dapibus erat, id rhoncus tortor semper nec. Curabitur fermentum, quam et rhoncus dapibus, neque purus cursus tellus, a eleifend libero purus at elit."
df3 = pd.DataFrame({"text": [test_text]})
dataframes.append(df3)

print(dataframes[0])


def checking_if_is_misogynistic():
    print("Starting checking if is misogynistic...")
    # inicializacja modelu
    tokenizer = AutoTokenizer.from_pretrained(
        "glombardo/misogynistic-statements-classification-model"
    )
    model = AutoModelForSequenceClassification.from_pretrained(
        "glombardo/misogynistic-statements-classification-model"
    )
    # sprawdza czy wypowiedź jest mizoginistyczna, automatycznie tłumaczenie na hiszpański
    dataframes_list = dataframes
    misogynistic_dataframes = []

    for i in range(0, len(dataframes_list)):
        df_copy = dataframes_list[i].copy()
        text_from_df = df_copy["text"].to_string(index=False)

        # tłumaczenie z wykorzystaniem GoogleTranslator
        translated_text = GoogleTranslator(src="auto", target="es").translate(
            text_from_df
        )

        input_ids = tokenizer.encode(translated_text, return_tensors="pt")
        output = model(input_ids)

        if (
            output.logits.softmax(dim=1)[0].tolist()[0]
            > output.logits.softmax(dim=1)[0].tolist()[1]
        ):
            df_copy["misoginic"] = "No"
            misogynistic_dataframes.append(df_copy)
        else:
            df_copy["misoginic"] = "Yes"
            misogynistic_dataframes.append(df_copy)
        print("Calculated misogynistic for speech {}".format(i + 1))

    return misogynistic_dataframes


def test_getting_emotion_new_model():
    completed_dataframes = []

    for i in range(0, len(dataframes)):
        df = dataframes[i].copy()
        df["emotion"] = df["text"].apply(
            lambda line: new_model.get_emotion(line) if len(line) < 2048 else "NaN"
        )
        completed_dataframes.append(df)

    return completed_dataframes


def saving_to_csv():
    dataframes = test_getting_emotion_new_model()
    # dataframes = checking_if_is_misogynistic()

    with pd.ExcelWriter("output_file_test.xlsx") as writer:
        for i, df in enumerate(dataframes):
            sheet_name = f"Sheet_{i+1}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)


saving_to_csv()
