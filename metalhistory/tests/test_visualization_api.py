"""
Test routines for the data visualization class
"""

import metalhistory.visualization_api as vis

import os
import sys
from pathlib import Path
from PIL import Image

import pandas as pd

# get path of the dataset
root_dir = os.path.abspath(__file__ + "/../../../")
data_path = root_dir + '/data/MA_10k_albums.csv'

# get path of the api folder
file_dir = os.path.abspath(__file__ + "/../../")



def test_prune():
    """
    Test the prune_and_group function
    """

    # the oracle knows that Iron Maiden has published 38 albums
    oracle_artist = 'Iron Maiden'
    oracle_albums = 38

    # so we prune the dataset and once it is grouped by N. of albums, we check that Iron Maiden is there
    artist_df = vis.prune_and_group(data_path, oracle_albums)
    artist_by_count = artist_df.count().sort_values(by='MA_score', ascending=False)

    assert oracle_artist == artist_by_count.index[0]


def test_artist_barplot():
    """
    Test the artist bar plot function.
    """

    n_albums = 15
    n_artists = 30

    # we create the image with an absolute path,
    # if relative it will depend from which directory the test is executed
    test_path = file_dir + '/test_artist_barplot.svg'

    vis.artist_barplot(data_path, n_albums, n_artists, test_path)

    # now we test if the image is there
    # the oracle assumes that the image is there
    oracle_isthere = True

    test_file = Path(test_path)

    assert oracle_isthere == test_file.is_file()


def test_generate_txt():
    """
    Test function for the generate txt from df function.
    """
    
    # the oracle know that Iron Maiden has published 38 albums
    # so we create a txt file just with Iron Maiden entry which should be 'Iron_Maiden' repeated 38 times.
    # The first 11 caracters should also be 'Iron_Maiden'
    oracle_albums = 38
    oracle_isthere = True
    oracle_string = 'Iron_Maiden'

    artist_df = vis.prune_and_group(data_path, oracle_albums)
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

    n_albums = 15
    words = 30

    # we create the image with an absolute path,
    # if relative it will depend from which directory the test is executed
    test_path = file_dir + '/test_artist_qtcloud.svg'

    vis.artist_cloud(data_path, 'quantity', words, n_albums, test_path)

    # now we test if the image is there
    # the oracle assumes that the image is there
    oracle_isthere = True

    test_file = Path(test_path)

    assert oracle_isthere == test_file.is_file()


def test_artist_quality():
    """
    Test the artist quality cloud function.
    """

    n_albums = 15
    words = 30

    # we create the image with an absolute path,
    # if relative it will depend from which directory the test is executed
    test_path = file_dir + '/test_artist_qlcloud.svg'

    vis.artist_cloud(data_path, 'quality', words, n_albums, test_path)

    # now we test if the image is there
    # the oracle assumes that the image is there
    oracle_isthere = True

    test_file = Path(test_path)

    assert oracle_isthere == test_file.is_file()


def test_album_covers():
    """
    Test the album cover word cloud function. Test that the output image has
    the correct dimensions and that it was written to disc properly.
    """
    
    width = 1280
    height = 720
    image_name = './metalhistory/tests/album_covers_test_image.jpg'
    
    img = vis.album_covers(num_albums=5, width=width, height=height,
                           image_name=image_name)
    
    # Check that the returned image has the correct size
    out_width, out_height = img.size
    assert width == out_width
    assert height == out_height
    
    # Check that the written image exists and that it has the correct size
    assert os.path.isfile(image_name)
    img = Image.open(image_name)
    out_width, out_height = img.size
    assert width == out_width
    assert height == out_height
    os.remove(image_name)
