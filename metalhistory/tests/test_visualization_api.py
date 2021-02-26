"""
Test routines for the data visualization class
"""

from metalhistory.visualization_api import Visualize

import os
import sys
import pandas as pd


# get path of the dataset
script_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
data_path = os.path.join(parent_dir, '/data/MA_10k_albums.csv')

def test_load_dataset():
    """
    Test the load function.
    """
    vis = Visualize(data_path)
    df = vis.load_dataframe()

    df.head()


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