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
    file_dir = os.path.abspath(__file__ + "/../../")
    test_path = file_dir + '/test_artist_barplot.svg'

    vis.artist_barplot(n_albums, n_artists, test_path)

    # now we test if the image is there
    # the oracle assumes that the image is there
    oracle_isthere = True

    test_file = Path(test_path)

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
    file_dir = os.path.abspath(__file__ + "/../../")
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
    file_dir = os.path.abspath(__file__ + "/../../")
    test_path = file_dir + '/test_artist_qlcloud.svg'

    vis.artist_cloud('quality', words, n_albums, test_path)

    # now we test if the image is there
    # the oracle assumes that the image is there
    oracle_isthere = True

    test_file = Path(test_path)

    assert oracle_isthere == test_file.is_file()
