"""
Class allowing some nice visualization of heavy metal data
"""

from .data_query_functions import LastFM

# visualization libraries
import numpy as np
import pandas as pd
from os import path
from PIL import Image
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


    def load_dataframe(self):
        """
        Import the csv as dataframe
        """
        df = pd.read_csv(self.dataset)

        return df


    def prune_N(self, n=15):
        """
        Return the dataset of the artists with N>=n albums.
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

        return df


    def artist_barplot(self, n_albums=20, path='artist_bar.svg'):
        """
        Visualize a histogram plot with artist names.
        Artist are scored based on the average of the MA score of each album
        """

        df = self.prune_N(n_albums)
        artist_df = df.groupby('artist')

        plt.figure(figsize=(15,12))
        artist_df.mean().sort_values(by='MA_score', ascending=False)["MA_score"].plot.bar()
        plt.xticks(rotation=70)
        plt.title("Best artist with at least " + str(n_albums) + " albums.")
        plt.xlabel("")
        plt.ylabel("Average MA score")
        plt.savefig(path)


    def artist_cloud(self, words_limit=20, min_albums=15, path='artist_cloud.svg'):
        #TODO: implement this with a real dataset
        """
        Visualize a world cloud with artist names.
        The artist names correspond to the most influential ones, from 1 to 'ords_limits'.
        The atists are selected such that they published at least 'min_albums' albums.
        The figure will be saved in the specified path.
        """

        df = self.prune_N(min_albums)
        artist_df = df.groupby('artist')

        artist_df = artist_df.count().sort_values(by='MA_score', ascending=False)["MA_score"]
        index_obj = artist_df.index
        index_list = []

        txt_path = 'artist_cloud.txt'
        # cancel the file if it exists
        out_file = open(txt_path, 'w')
        out_file.write("")
        
        for name in index_obj:
            # replace space with tabs so that artists names with multiple words are counted as a single entity
            index_list.append(name.replace(' ', '_'))
            count = artist_df.loc[name]
            out_file = open(txt_path, 'a')
            for i in range(count):
                out_file.write(index_list[-1] + " ")

        # create and generate a word cloud image:
        out_file = open(txt_path, 'r')
        contents = out_file.read()
        wordcloud = WordCloud(collocations=False, max_words=words_limit).generate(contents)

        # Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(path)


    def album_cloud(self, threshold=20, path='./'):
        #TODO: implement this with a real dataset
        """
        Visualize a world cloud with album names.
        The album names correspond to the most influential ones, from 1 to threshold.
        The figure will be saved in the specified path.
        """


    def genre_cloud(self, threshold=20, path='./'):
        #TODO: implement this with a real dataset
        """
        Visualize a world cloud with genre names.
        The genre names correspond to the most influential ones, from 1 to threshold.
        The figure will be saved in the specified path.
        """
