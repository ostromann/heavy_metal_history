"""
Test routines for the LastFM class
"""

import os
import pytest
from dotenv import load_dotenv
from metalhistory.data_query_functions import LastFM

BASE_STR = 'http://ws.audioscrobbler.com/2.0/?'


def get_api_key():
    """
    Retrieve the API key without using the LastFM class.
    """
    env_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir, '.env'))
    load_dotenv(dotenv_path=env_path)
    return os.getenv('LASTFM_API_KEY')


def test_authenticate():
    """
    Test the authenticate_from_dotenv function.
    In the .env file there is a value for ORACLE_KEY for testing purposes.
    """
    oracle_key = 'thisIsTheOracleKey123'
    lastFM_obj = LastFM()
    api_key = lastFM_obj.authenticate_from_dotenv('ORACLE_KEY')
    assert oracle_key == api_key


def test_build_request_dummy_input():
    """
    Test the build_request function with dummy inputs.
    """
    lastFM_obj = LastFM()
    api_key = get_api_key()
    kwargs = {'method': 'dummyMethod',
              'format_spec': 'json',
              'dummyArg1': 'arg1',
              'dummyArg2': 'arg2'}
    request_str = lastFM_obj.build_request(**kwargs)
    correct_str = BASE_STR + '&api_key=' + api_key + \
        '&method=dummyMethod' + \
        '&dummyArg1=arg1' + \
        '&dummyArg2=arg2' + \
        '&format=json'
    assert request_str == correct_str


def test_build_request_non_clean_input():
    """
    Test the build_request function with inputs that should be formated before
    returning the final url.
    """
    lastFM_obj = LastFM()
    api_key = get_api_key()
    kwargs = {'method': 'album.getinfo',
              'format_spec': 'incorrect_format',
              'artist': 'Black Sabbath',
              'album': '  Paranoid'}
    request_str = lastFM_obj.build_request(**kwargs)
    correct_str = BASE_STR + '&api_key=' + api_key + \
        '&method=album.getinfo' + \
        '&artist=Black%20Sabbath' + \
        '&album=Paranoid'
    assert request_str == correct_str


def test_clean_string():
    """
    Test the clean_string function.
    """
    lastFM_obj = LastFM()
    dirty_str = '  text with bad formattiñg!  '
    correct_str = 'text%20with%20bad%20formatti%C3%B1g%21'
    cleaned_str = lastFM_obj.clean_string(dirty_str)
    assert cleaned_str == correct_str


def test_get_album_matches_return_types():
    """
    Test that the get_album_matches function returns correct data types.
    """
    lastFM_obj = LastFM()
    matches = lastFM_obj.get_album_matches(album='Paranoid')
    assert type(matches) is dict
    assert 'results' in matches.keys()
    assert type(matches['results']) is dict
    assert 'albummatches' in matches['results'].keys()


def test_get_album_matches_invalid_args():
    """
    Test that the get_album_matches function raises a ValueError if invalid
    arguments are given.
    """
    lastFM_obj = LastFM()
    with pytest.raises(ValueError):
        matches = lastFM_obj.get_album_matches(artist='Black Sabbath', album='Paranoid')


def test_get_album_matches_required_args():
    """
    Test that the get_album_matches function raises a ValueError if a required
    argument was not specified.
    """
    lastFM_obj = LastFM()
    with pytest.raises(ValueError):
        matches = lastFM_obj.get_album_matches(verbose=0)


def test_get_album_info():
    """
    Test the get_album_info function
    """


def test_gget_track_info():
    """
    Test the get_track_info function
    """
