"""
Test routines for the LastFM class
"""

from metalhistory.data_query_functions import LastFM

def test_authenticate():
    """
    Test the authenticate_from_dotenv function.
    In the .env file there is a value for ORACLE_KEY for testing purposes.
    """
    oracle_key = 'thisIsTheOracleKey123'
    lastFM_obj = LastFM()
    api_key = lastFM_obj.authenticate_from_dotenv('ORACLE_KEY')

    assert oracle_key == api_key


def test_build_request():
    """
    Test the build_request function
    """


def test_clean_string():
    """
    Test the clean_string function
    """


def test_get_album_matches():
    """
    Test the get_album_matches function
    """


def test_get_album_info():
    """
    Test the get_album_info function
    """

def test_gget_track_info():
    """
    Test the get_track_info function
    """
