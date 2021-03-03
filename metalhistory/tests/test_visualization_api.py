"""
Test routines for the data visualization class
"""

from metalhistory.visualization_api import Visualize

import os
import sys
from pathlib import Path

import pandas as pd

# get path of the dataset
root_dir = os.path.abspath(__file__ + "/../../../")
data_path = root_dir + '/data/MA_10k_albums.csv'

# get path of the api folder
file_dir = os.path.abspath(__file__ + "/../../")



def test_load_dataset():
    """
    Test the load function.
    """
    vis = Visualize(data_path)
    df = vis.load_dataframe()

    # the oracle has knows the first raw of the dataset
    oracle_artist = 'Slayer'
    oracle_album = 'Reign in Blood'
    oracle_score = 36.01

    assert oracle_artist == df['artist'][0]
    assert oracle_album == df['album'][0]
    assert oracle_score == df['MA_score'][0]


def test_prune():
    """
    Test the prune_and_group function
    """
    vis = Visualize(data_path)

    # the oracle knows that Iron Maiden has published 38 albums
    oracle_artist = 'Iron Maiden'
    oracle_albums = 38

    # so we prune the dataset and once it is grouped by N. of albums, we check that Iron Maiden is there
    artist_df = vis.prune_and_group(oracle_albums)
    artist_by_count = artist_df.count().sort_values(by='MA_score', ascending=False)

    assert oracle_artist == artist_by_count.index[0]


def test_artist_barplot():
    """
    Test the artist bar plot function.
    """

    vis = Visualize(data_path)
    n_albums = 15
    n_artists = 30

    # we create the image with an absolute path,
    # if relative it will depend from which directory the test is executed
    test_path = file_dir + '/test_artist_barplot.svg'

    vis.artist_barplot(n_albums, n_artists, test_path)

    # now we test if the image is there
    # the oracle assumes that the image is there
    oracle_isthere = True

    test_file = Path(test_path)

    assert oracle_isthere == test_file.is_file()


def test_generate_txt():
    """
    Test function for the generate txt from df function.
    """

    vis = Visualize(data_path)
    
    # the oracle know that Iron Maiden has published 38 albums
    # so we create a txt file just with Iron Maiden entry which should be 'Iron_Maiden' repeated 38 times.
    # The first 11 caracters should also be 'Iron_Maiden'
    oracle_albums = 38
    oracle_isthere = True
    oracle_string = 'Iron_Maiden'

    artist_df = vis.prune_and_group(oracle_albums)
    artist_df = artist_df.count().sort_values(by='MA_score', ascending=False)["MA_score"]
    test_path = vis.generate_text_from_df(artist_df, file_name='/test_txt.txt')

    test_file = Path(test_path)

    out_file = open(test_path, 'r')
    first_artist = out_file.read(11)

    assert oracle_isthere == test_file.is_file()
    assert oracle_string == first_artist


def test_generate_wordcloud():
    """
    Test function to generate a world cloud
    """

    vis = Visualize(data_path)

    test_path = file_dir + '/test_txt.txt'

    figure_path = file_dir + '/test_wordcloud.svg'

    vis.generate_word_cloud(1, test_path, figure_path)

    # now we test if the image is there
    # the oracle assumes that the image is there
    oracle_isthere = True

    test_file = Path(figure_path)

    assert oracle_isthere == test_file.is_file()


def test_artist_quantity():
    """
    Test the artist quantity cloud function.
    """

    vis = Visualize(data_path)
    n_albums = 15
    words = 30

    # we create the image with an absolute path,
    # if relative it will depend from which directory the test is executed
    test_path = file_dir + '/test_artist_qtcloud.svg'

    vis.artist_cloud('quantity', words, n_albums, test_path)

    # now we test if the image is there
    # the oracle assumes that the image is there
    oracle_isthere = True

    test_file = Path(test_path)

    assert oracle_isthere == test_file.is_file()


def test_artist_quality():
    """
    Test the artist quality cloud function.
    """

    vis = Visualize(data_path)
    n_albums = 15
    words = 30

    # we create the image with an absolute path,
    # if relative it will depend from which directory the test is executed
    test_path = file_dir + '/test_artist_qlcloud.svg'

    vis.artist_cloud('quality', words, n_albums, test_path)

    # now we test if the image is there
    # the oracle assumes that the image is there
    oracle_isthere = True

    test_file = Path(test_path)

    assert oracle_isthere == test_file.is_file()
