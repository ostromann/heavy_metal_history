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
DATASET = os.path.abspath(__file__ + "/../../../") + '/data/proc_MA_1k_albums_not_cumulative.csv'

# get path of the api folder
IMG_PATH = os.path.abspath(__file__ + "/../../../") + '/images'



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
