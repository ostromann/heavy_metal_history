"""
Class allowing some nice visualization of heavy metal data
"""

from .data_query_functions import LastFM

# visualization libraries
import numpy as np
import pandas as pd
import os
import squarify
import ast
import math
import requests
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

        # TODO: check which variables could be defined here, e.g. paths


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


    def artist_barplot(self, n_albums=15, n_artists=30, path='artist_bar.svg'):
        """
        Visualize a histogram plot with 'n_artists' artist names that have published at least 'n_albums' albums.
        Artist are scored based on the average of the MA score of each album.
        Average, Max and Min values are plotted.
        """

        df = self.prune_N(n_albums)
        artist_df = df.groupby('artist')

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


    def artist_quantity_cloud(self, words_limit=20, min_albums=15, path='artist_qtcloud.svg'):
        # TODO: merge this function with the quality cloud by adding a sorting method in the parameters
        """
        Visualize a world cloud with artist names.
        The artist names displayed depend on the number of albums published.
        The atists are selected such that they published at least 'min_albums' albums.
        Up to 'words_limit' names are displayed.
        The figure will be saved in the specified path.
        """

        df = self.prune_N(min_albums)
        artist_df = df.groupby('artist')

        artist_df = artist_df.count().sort_values(by='MA_score', ascending=False)["MA_score"]
        artist_df = artist_df.head(words_limit)
        # the dataframe is indexed with the artists names that we need to access
        index_obj = artist_df.index
        index_list = []

        file_dir = os.path.abspath(__file__ + "/../")
        txt_path = file_dir + '/artist_qtcloud.txt'
        # cancel the file if it exists
        out_file = open(txt_path, 'w')
        out_file.write("")
        
        for name in index_obj:
            # replace space with tabs so that artists names with multiple words are counted as a single entity
            index_list.append(name.replace(' ', '_'))
            count = artist_df.loc[name]
            # create a file.txt containing artists names repeated N times where N is the number of published albums
            out_file = open(txt_path, 'a')
            for i in range(count):
                out_file.write(index_list[-1] + " ")

        # create and generate a word cloud image
        out_file = open(txt_path, 'r')
        contents = out_file.read()
        wordcloud = WordCloud(collocations=False, max_words=words_limit).generate(contents)

        # Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(path)
        plt.close("all")


    def artist_quality_cloud(self, words_limit=20, min_albums=15, path='artist_qlcloud.svg'):
        # TODO: merge this function with the quantity cloud by adding a sorting method in the parameters
        """
        Visualize a world cloud with artist names.
        The artist names displayed depend on the score average of albums published.
        The atists are selected such that they published at least 'min_albums' albums.
        Up to 'words_limit' names are displayed.
        The figure will be saved in the specified path.
        """

        df = self.prune_N(min_albums)
        artist_df = df.groupby('artist')

        artist_df = artist_df.mean().sort_values(by='MA_score', ascending=False)["MA_score"]
        artist_df = artist_df.head(words_limit)
        # the dataframe is indexed with the artists names that we need to access
        index_obj = artist_df.index
        index_list = []

        file_dir = os.path.abspath(__file__ + "/../")
        txt_path = file_dir + '/artist_qlcloud.txt'
        # cancel the file if it exists
        out_file = open(txt_path, 'w')
        out_file.write("")
        
        for name in index_obj:
            # replace space with tabs so that artists names with multiple words are counted as a single entity
            index_list.append(name.replace(' ', '_'))
            # create a file.txt containing artists names repeated N times where N is the number of published albums
            count = round(artist_df.loc[name])
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
        plt.close("all")


    def genre_cloud(self, threshold=20, path='./'):
        """
        Visualize a world cloud with genre names.
        The genre names correspond to the most influential ones, from 1 to threshold.
        The figure will be saved in the specified path.
        """
    
    def album_covers(self, width=1280, height=720, image_name='./vis/album_covers.jpg'):
        """
        Visualize a wordcloud but use album covers instead of names.
        """

        # Load data
        df = self.load_dataframe()
        df = df[['artist', 'album', 'playcount', 'images']]
        df = df.sort_values('playcount', ascending=False)

        # Format image URLs
        def format_image_str(s):
            # TODO: get the largest image in case some image sizes are not present
            s = s.replace('"', "'")
            s = ast.literal_eval(s)
            return s[-1]['#text']
        df['images'] = df.apply(lambda row: format_image_str(row['images']), axis=1)

        # Compute album cover positions using squarify
        values = list(df['playcount'])
        values = squarify.normalize_sizes(values, height, width)
        rects = squarify.squarify(values, 0., 0., height, width)

        # Compute integer values for slicing
        for rect in rects:
            rect['x1'] = max(0, math.floor(rect['x']))
            rect['y1'] = max(0, math.floor(rect['y']))
            rect['x2'] = min(height, math.ceil(rect['x'] + rect['dx']))
            rect['y2'] = min(width,  math.ceil(rect['y'] + rect['dy']))

        # Create the image
        img = np.zeros((height, width, 3), np.uint8)
        for i, url in enumerate(df['images']):
            rect = rects[i]
            im = Image.open(requests.get(url, stream=True).raw)
            im = im.convert('RGB')
            im = im.resize((rect['y2']-rect['y1'], rect['x2']-rect['x1']))
            im = np.asarray(im)
            img[rect['x1']:rect['x2'], rect['y1']:rect['y2'], :] = im

        # Save the image
        dir_name = os.path.dirname(image_name)
        if dir_name != '' and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        img = Image.fromarray(img)
        img.save(image_name)























    
