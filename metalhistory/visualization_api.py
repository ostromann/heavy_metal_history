"""
Class allowing some nice visualization of heavy metal data
"""

from .data_query_functions import LastFM

# visualization libraries
import pandas as pd
import os
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

class Visualize():
    def __init__(self, csv='data.csv'):
        """
        Create Visualize object that can be used to visualize the data.

        Parameters
        ----------
        Dataset

        """

        try:
            self.dataset = csv
        except FileNotFoundError:
            print("The specified file could not be loaded.")

        self.directory_path = os.path.abspath(__file__ + "/../")


    def artist_barplot(self, n_albums=15, n_artists=30, path='artist_bar.svg'):
        """
        Visualize a histogram plot with 'n_artists' artist names that have published at least 'n_albums' albums.
        Artist are scored based on the average of the MA score of each album.
        Average, Max and Min values are plotted.
        """

        artist_df = self.prune_and_group(n_albums)

        # manipulate DF to retain useful statistics for the plot
        artist_description = artist_df.describe()
        artist_description.drop(['count', 'std', '25%', '50%', '75%'], axis=1, level=1, inplace=True)
        artist_sorted = artist_description.sort_values(by=("MA_score", "mean"), ascending=False)
        # drop upper level in columns names
        artist_sorted.columns = artist_sorted.columns.droplevel()
        # keep the requested number of artists
        # note that n_artists is higher than the size of the dataframe, no exception is raised
        artist_sorted = artist_sorted.head(n_artists)

        plt.figure(figsize=(300,100))
        artist_sorted.plot.bar()
        plt.xticks(rotation=70)
        plt.title("Statistics on artists with at least " + str(n_albums) + " albums.")
        plt.xlabel("")
        plt.ylabel("MA score")
        plt.tight_layout()
        plt.savefig(path)
        plt.close("all")


    def artist_cloud(self, sorting='quantity', words_limit=20, min_albums=15, path='/artist_cloud.svg'):
        """
        Visualize a world cloud with artist names.
        The artist names displayed depend on the sorting criteria.
        The atists are selected such that they published at least 'min_albums' albums.
        Up to 'words_limit' names are displayed.
        The figure will be saved in the specified path.
        """

        artist_df = self.prune_and_group(min_albums)

        if sorting == 'quantity':
            artist_df = artist_df.count().sort_values(by='MA_score', ascending=False)["MA_score"]
        elif sorting == 'quality':
            artist_df = artist_df.mean().sort_values(by='MA_score', ascending=False)["MA_score"]
        else:
            print("Sorting method not available, continuing with default option.")
            artist_df = artist_df.count().sort_values(by='MA_score', ascending=False)["MA_score"]

        artist_df = artist_df.head(words_limit)

        # create and generate a word cloud image
        txt_path = self.generate_text_from_df(artist_df)
        self.generate_word_cloud(words_limit, txt_path, path)


    def load_dataframe(self):
        """
        Import the csv as dataframe
        """
        df = pd.read_csv(self.dataset)

        return df


    def prune_and_group(self, n=15):
        """
        Return the dataset of the artists with N>=n albums.
        Group the dataset by artist.
        """

        df = self.load_dataframe()
        # Groupby by artist
        artist_df = df.groupby('artist')
        # sort artist by album count
        artist_by_count = artist_df.count().sort_values(by='album', ascending=False)
        # save the dataframe with discarded artists
        discarded = artist_by_count.drop(artist_by_count[artist_by_count.album >= n].index)
        for artist in discarded.index:
            df = df.drop(artist_df.get_group(artist).index)

        return df.groupby('artist')


    def generate_text_from_df(self, df, file_name='/artist_cloud.txt'):
        """
        Generate a textfile froma dataframe to use in the word cloud.
        Return the path to the file so it's easy to locate it.
        """
        # the dataframe is indexed with the artists names that we need to access
        index_obj = df.index
        index_list = []

        txt_path = self.directory_path + file_name
        # cancel the file if it exists
        out_file = open(txt_path, 'w')
        out_file.write("")
        
        for name in index_obj:
            # replace space with tabs so that artists names with multiple words are counted as a single entity
            index_list.append(name.replace(' ', '_'))
            count = round(df.loc[name])
            # create a file.txt containing artists names repeated N times where N is the number of published albums
            out_file = open(txt_path, 'a')
            for i in range(count):
                out_file.write(index_list[-1] + " ")

        return txt_path


    def generate_word_cloud(self, words, txt_file, figure_name='/artist_cloud.svg'):
        """
        Generate the word cloud out of a txt file.
        The parameter 'words' specifies the number of words in the could.
        """

        out_file = open(txt_file, 'r')
        contents = out_file.read()
        wordcloud = WordCloud(collocations=False, max_words=words).generate(contents)

        # Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(figure_name)
        plt.close("all")
