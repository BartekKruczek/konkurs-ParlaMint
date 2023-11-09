import new_model
from deep_translator import GoogleTranslator
import pandas as pd

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


def getting_emotion_new_model(self):
    """Zwraca listę dataframów z emocjami, nowy model"""
    # dataframes = self.cleaning_text()
    completed_dataframes = []

    for i in range(0, len(dataframes)):
        df = dataframes[i].copy()
        text_from_df = ""
        text_from_df = df["text"].to_string(index=False)
        # print(len(text_from_df))
        # print(text_from_df)
        if len(text_from_df) < 4999:
            # translated_text = GoogleTranslator(src="auto", target="en").translate(
            #     text_from_df
            # )
            df["emotion"] = new_model.get_emotion(text_from_df)
            completed_dataframes.append(df)
        else:
            df["emotion"] = "NaN"
            completed_dataframes.append(df)

    return completed_dataframes


def test_getting_emotion_new_model(self):
    completed_dataframes = []

    for i in range(0, len(dataframes)):
        df = dataframes[i].copy()
        df["emotion"] = df["text"].apply(
            lambda line: new_model.get_emotion(
                GoogleTranslator(source="auto", target="en").translate(line)
            )
            if len(line) < 4999
            else "NaN"
        )
        completed_dataframes.append(df)

    return completed_dataframes


print(getting_emotion_new_model(dataframes))
