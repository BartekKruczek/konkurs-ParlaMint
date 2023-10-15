import wordcloud
import os
import matplotlib.pyplot as plt


class Plotting_data:
    def __init__(self, master_dictionary) -> None:
        self.master_dictionary = master_dictionary

    def __repr__(self) -> str:
        return "Klasa do wizualizacji danych"

    def creating_plots_directory(self):
        """
        Tworzenie folderu na wykresy
        """
        try:
            os.mkdir("Plots")
        except FileExistsError:
            pass

    def counting_emotions(self):
        """
        Zliczanie emocji
        """
        emotion_counts = {}

        for key, value in self.master_dictionary.items():
            for emotion in value.values():
                if emotion in emotion_counts:
                    emotion_counts[emotion] += 1
                else:
                    emotion_counts[emotion] = 1

        return emotion_counts

    def plotting_emotion_cloud(self):
        """
        Tworzenie chmury emocji
        """
        self.creating_plots_directory()

        cloud = wordcloud.WordCloud().generate_from_frequencies(
            self.counting_emotions()
        )
        plt.figure(figsize=(16, 9), dpi=1200)
        plt.imshow(cloud)
        plt.savefig("Plots/emotion_cloud.png")
