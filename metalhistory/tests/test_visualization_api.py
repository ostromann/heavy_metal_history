"""
Test routines for the data visualization class
"""

from metalhistory.visualization_api import Visualize

import os
import sys
import pandas as pd


# get path of the dataset
root_dir = os.path.abspath(__file__ + "/../../../")
data_path = root_dir + '/data/MA_10k_albums.csv'


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
    Test the prune_N function
    """
    vis = Visualize(data_path)

    # the oracle knows that Iron Maiden has published 38 albums
    oracle_artist = 'Iron Maiden'
    oracle_albums = 38

    # so we prune the dataset and once it is grouped by N. of albums, we check that Iron Maiden is there
    df = vis.prune_N(oracle_albums)
    artist_df = df.groupby('artist')
    artist_by_count = artist_df.count().sort_values(by='MA_score', ascending=False)

    assert oracle_artist == artist_by_count.index[0]


def test_artist_cloud(threshold=20, path='./'):
    """
    Test the artist word cloud.
    """


def test_album_cloud(threshold=20, path='./'):
    """
    Test the album word cloud.
    """


def test_genre_cloud(threshold=20, path='./'):
    """
    Test the genres word cloud.
    """