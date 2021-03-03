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


def test_get_album_matches_bad_request():
    """
    Test that the get_track_info function raises a RuntimeError if the
    the response from the LastFM API is not ok
    """
    lastFM_obj = LastFM()

    # forcefully set wrong API key
    lastFM_obj.api_str=''
    with pytest.raises(RuntimeError):
        info = lastFM_obj.get_album_matches(album='Paranoid')


def test_get_album_info_return_types():
    """
    Test that the get_album_info function returns correct data types.
    """
    lastFM_obj = LastFM()
    info = lastFM_obj.get_album_info(artist='Black Sabbath', album='Paranoid')
    assert type(info) is dict
    assert 'name' in info.keys()
    assert type(info['name']) is str
    assert 'tracks' in info.keys()
    assert type(info['tracks']) is dict


def test_get_album_info_invalid_args():
    """
    Test that the get_album_info function raises a ValueError if invalid
    arguments are given.
    """
    lastFM_obj = LastFM()
    with pytest.raises(ValueError):
        info = lastFM_obj.get_album_info(artist='Black Sabbath', album='Paranoid',
                                         invalid_arg='invalid_arg')


def test_get_album_info_required_args():
    """
    Test that the get_album_info function raises a ValueError if required
    arguments are not specified.
    """
    lastFM_obj = LastFM()
    with pytest.raises(ValueError):
        info = lastFM_obj.get_album_info(artist='Black Sabbath')


def test_get_album_info_combined_args():
    """
    Test that the get_album_info function raises a ValueError if mbid is
    specified together with artist/album.
    """
    lastFM_obj = LastFM()
    with pytest.raises(ValueError):
        info = lastFM_obj.get_album_info(artist='Black Sabbath', album='Paranoid',
                                         mbid='2982b682-36ea-3605-b959-04e746736070')


def test_get_album_info_autocorrect():
    """
    Test that the get_album_info function raises a ValueError if the
    autocorrect argument is given a value other than 0 or 1.
    """
    lastFM_obj = LastFM()
    with pytest.raises(ValueError):
        info = lastFM_obj.get_album_info(artist='Black Sabbath', album='Paranoid',
                                         autocorrect=2)


def test_get_album_info_bad_request():
    """
    Test that the get_track_info function raises a RuntimeError if the
    the response from the LastFM API is not ok
    """
    lastFM_obj = LastFM()

    # forcefully set wrong API key
    lastFM_obj.api_str=''
    with pytest.raises(RuntimeError):
        info = lastFM_obj.get_album_info(artist='Black Sabbath', album='Paranoid')

def test_get_album_info_correct_fields():
    """
    Test that the get_album_info function returns a dictionary value of correct type
    if an accepted field is passed in argument.
    """
    lastFM_obj = LastFM()
    fields = lastFM_obj.config['system settings']['lastfm']['accepted fields']
    print(fields)
    info = lastFM_obj.get_album_info(artist='Black Sabbath', album='Paranoid',
                                         fields=fields)
    assert type(info) is dict
    for field in fields:
        assert field in info.keys()
        assert info[field] != None


def test_get_album_info_incorrect_fields():
    """
    Test that the get_album_info function returns a dictionary value of type None
    if an
    unaccepted field is passed in argument.
    """
    lastFM_obj = LastFM()
    info = lastFM_obj.get_album_info(artist='Black Sabbath', album='Paranoid',
                                         fields=['wrong_field', 'wrong_field_2'])
    assert type(info) is dict
    assert 'wrong_field' in info.keys()
    assert info['wrong_field'] == None
    assert 'wrong_field_2' in info.keys()
    assert info['wrong_field_2'] == None


def test_get_track_info_return_types():
    """
    Test that the get_track_info function returns correct data types.
    """
    lastFM_obj = LastFM()
    info = lastFM_obj.get_track_info(artist='Black Sabbath', track='War Pigs')
    assert type(info) is dict
    assert 'name' in info.keys()
    assert type(info['name']) is str
    assert 'artist' in info.keys()
    assert type(info['artist']) is dict


def test_get_track_info_invalid_args():
    """
    Test that the get_track_info function raises a ValueError if invalid
    arguments are given.
    """
    lastFM_obj = LastFM()
    with pytest.raises(ValueError):
        info = lastFM_obj.get_track_info(artist='Black Sabbath', track='War Pigs',
                                         invalid_arg='invalid_arg')


def test_get_track_info_required_args():
    """
    Test that the get_track_info function raises a ValueError if required
    arguments are not specified.
    """
    lastFM_obj = LastFM()
    with pytest.raises(ValueError):
        info = lastFM_obj.get_track_info(artist='Black Sabbath')


def test_get_track_info_combined_args():
    """
    Test that the get_track_info function raises a ValueError if mbid is
    specified together with artist/track.
    """
    lastFM_obj = LastFM()
    with pytest.raises(ValueError):
        info = lastFM_obj.get_track_info(artist='Black Sabbath', track='War Pigs',
                                         mbid='c2786bd8-7dc7-4633-ab6c-70c70ebd432f')


def test_get_track_info_autocorrect():
    """
    Test that the get_track_info function raises a ValueError if the
    autocorrect argument is given a value other than 0 or 1.
    """
    lastFM_obj = LastFM()
    with pytest.raises(ValueError):
        info = lastFM_obj.get_track_info(artist='Black Sabbath', track='War Pigs',
                                         autocorrect=2)

def test_get_track_info_bad_request():
    """
    Test that the get_track_info function raises a RuntimeError if the
    the response from the LastFM API is not ok
    """
    lastFM_obj = LastFM()

    # forcefully set wrong API key
    lastFM_obj.api_str=''
    with pytest.raises(RuntimeError):
        info = lastFM_obj.get_track_info(artist='Black Sabbath', track='War Pigs')
