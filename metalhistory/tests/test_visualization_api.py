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