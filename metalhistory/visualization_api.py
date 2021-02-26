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


    def prune_N(self, n=5):
        """
        Prune the dataset from the artists with N<n albums.
        """

        df = self.load_dataframe()
        # Groupby by artist
        artist = df.groupby('artist')
        # sort artist by album count
        artist = artist.count().sort_values(by='album', ascending=False)
        artist.drop(artist[artist.album < n].index, inplace=True)

        return artist



    def album_cloud(self, threshold=20, path='./'):
        #TODO: implement this with a real dataset
        """
        Visualize a world cloud with album names.
        The album names correspond to the most influential ones, from 1 to threshold.
        The figure will be saved in the specified path.
        """


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
