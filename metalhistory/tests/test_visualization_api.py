"""
Test routines for the data visualization class
"""

import metalhistory.visualization_api as vis

import os
import sys
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt

import pandas as pd

# get path of the dataset
DATASET = os.path.abspath(__file__ + "/../../../") + '/data/proc_MA_1k_albums_not_cumulative.csv'

# get path of the api folder
IMG_DIR = os.path.abspath(__file__ + "/../../../") + '/images'



def test_prune():
    """
    Test the prune_and_group function
    """

    # the oracle knows the content of the dataset
    # Soundgarden has 1 album in the dataset
    oracle_artist_not_in_df = 'Soundgarden'
    
    df = vis.prune_and_group(5)
    # so we prune the dataset and once it is grouped by N. of albums, we test against the oracle
    df = df.count().sort_values(by='MA_score', ascending=False)

    assert (oracle_artist_not_in_df in df.index) == False    

    # the oracle knows the content of the dataset
    # Iron Maiden has 16 album in the dataset
    oracle_artist_in_df = 'Iron Maiden'
    oracle_albums = 16

    assert (oracle_artist_in_df in df.index) == True
    assert df.loc[oracle_artist_in_df]['MA_score'] == oracle_albums

    # we check that we have all the keys that we want
    oracle_keys = ['MA_album', 'listeners', 'playcount', 'MA_score']

    keys_in_df = []
    for key in df.keys():
            keys_in_df.append(str(key))

    assert keys_in_df  == oracle_keys


def test_barplot_MA():
    """
    Test the artist_barplot function with the MA score metric
    """

    min_albums = 5
    n_artists = 30
    metric = 'MA_score'

    # we create the image with an absolute path,
    # if relative it will depend from which directory the test is executed
    test_image = IMG_DIR + '/test_barplot_MA.jpg'

    image, df = vis.artist_barplot(min_albums, n_artists, metric, test_image)

    # now we test if the image is there
    # the oracle assumes that the image is there
    oracle_isthere = True

    test_file = Path(test_image)

    assert oracle_isthere == test_file.is_file()

    # we required to use MA_score as metric, so we check that the dataframe uses it
    # moreover the plot should contain the labes: mean, min, max
    oracle_lv1 = ['mean', 'min', 'max']

    assert str(df.keys().get_level_values(0)[0]) == metric and\
            str(df.keys().get_level_values(0)[1]) == metric and\
            str(df.keys().get_level_values(0)[2]) == metric

    assert list(df.keys().get_level_values(1)) == oracle_lv1


def test_barplot_listeners():
    """
    Test the artist_barplot function with the listeners metric
    """

    min_albums = 5
    n_artists = 30
    metric = 'listeners'

    # we create the image with an absolute path,
    # if relative it will depend from which directory the test is executed
    test_image = IMG_DIR + '/test_barplot_listeners.jpg'

    image, df = vis.artist_barplot(min_albums, n_artists, metric, test_image)

    # now we test if the image is there
    # the oracle assumes that the image is there
    oracle_isthere = True

    test_file = Path(test_image)

    assert oracle_isthere == test_file.is_file()

    # we required to use MA_score as metric, so we check that the dataframe uses it
    # moreover the plot should contain the labes: mean, min, max
    oracle_lv1 = ['mean', 'min', 'max']

    assert str(df.keys().get_level_values(0)[0]) == metric and\
            str(df.keys().get_level_values(0)[1]) == metric and\
            str(df.keys().get_level_values(0)[2]) == metric

    assert list(df.keys().get_level_values(1)) == oracle_lv1


def test_barplot_playcount():
    """
    Test the artist_barplot function with the playcount metric
    """

    min_albums = 5
    n_artists = 30
    metric = 'playcount'

    # we create the image with an absolute path,
    # if relative it will depend from which directory the test is executed
    test_image = IMG_DIR + '/test_barplot_playcount.jpg'

    image, df = vis.artist_barplot(min_albums, n_artists, metric, test_image)

    # now we test if the image is there
    # the oracle assumes that the image is there
    oracle_isthere = True

    test_file = Path(test_image)

    assert oracle_isthere == test_file.is_file()

    # we required to use MA_score as metric, so we check that the dataframe uses it
    # moreover the plot should contain the labes: mean, min, max
    oracle_lv1 = ['mean', 'min', 'max']

    assert str(df.keys().get_level_values(0)[0]) == metric and\
            str(df.keys().get_level_values(0)[1]) == metric and\
            str(df.keys().get_level_values(0)[2]) == metric

    assert list(df.keys().get_level_values(1)) == oracle_lv1


def test_text_generation():
    """
    Test the text generation function
    """

    # the oracle creates its own dataset from list
    oracle_values = [2, 1]
    oracle_index = ['IamOracle1', 'IamOracle2']
    oracle_df = pd.DataFrame(oracle_values, index=oracle_index, columns=['count']) 
    oracle_isthere = True

    test_file = IMG_DIR + '/test_txt.txt'
    test_path = vis.generate_text_from_df(oracle_df, test_file)

    test_file = Path(test_path)

    assert oracle_isthere == test_file.is_file()


    with open(test_file) as f:
        words = [line.split() for line in f][0]

    assert len(words) == oracle_values[0] + oracle_values[1]
    assert words[0] == oracle_index[0]
    assert words[1] == oracle_index[0]
    assert words[2] == oracle_index[1]


def test_generate_wordcloud():
    """
    Test the word cloud generation function
    """

    # we use the same text file as the previous function
    test_path = IMG_DIR + '/test_txt.txt'

    figure_path = IMG_DIR + '/test_wordcloud.svg'

    vis.generate_word_cloud(2, test_path, figure_path)

    # now we test if the image is there
    # the oracle assumes that the image is there
    oracle_isthere = True

    test_file = Path(figure_path)

    assert oracle_isthere == test_file.is_file()


def test_wordcloud_MA():
    """
    Test the artist cloud function with the MA score metric
    """

    min_albums = 5
    n_artists = 30
    metric = 'MA_score'

    # we create the image with an absolute path,
    # if relative it will depend from which directory the test is executed
    test_image = IMG_DIR + '/test_cloud_MA.jpg'

    df = vis.artist_cloud(min_albums, n_artists, metric, test_image)

    # now we test if the image is there
    # the oracle assumes that the image is there
    oracle_isthere = True

    test_file = Path(test_image)

    assert oracle_isthere == test_file.is_file()

    # we required to use MA_score as metric, so we check that the series uses it
    # moreover the series should contain n_artists elements
    assert len(df.keys()) == n_artists
    assert df.name == metric


def test_album_covers():
    """
    Test the album cover word cloud function. Test that the output image has
    the correct dimensions and that it was written to disc properly.
    """
    
    width = 1280
    height = 720
    image_name = './images/album_covers_test_image.jpg'
    
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
