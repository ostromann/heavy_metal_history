import requests
from dotenv import load_dotenv
import os
import sys

class LastFM():
    def __init__(self):
        """
        Create LastFM API Object that can be used to query the database.

        Parameters
        ----------
        None


        Examples
        ----------
        Creating an LastFM API Object and querying album information:

        >>> import metalhistory.utils as utils
        >>> 
        >>> lastfm = utils.LastFM()
        >>> lastfm = utils.LastFM()
        >>> lastfm.get_album_info('Black Sabbath', 'Paranoid', verbose=1)

        """

        apy_key = self.authenticate_from_dotenv('LASTFM_API_KEY')
        self.api_str = '&api_key=' + self.api_key
        self.base_str = 'http://ws.audioscrobbler.com/2.0/?'
        pass



    def authenticate_from_dotenv(self, key_name):
        #TODO: Check if API key is present and valid!
        #TODO: Check if the services actually require Authentication. Many of them don't! e.g. https://www.last.fm/api/show/artist.search 
        """
        Load LastFM API from .env file
        """
        # get path of the .env file
        script_dir = os.path.dirname(__file__)
        parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
        env_path = os.path.join(parent_dir, '.env')
        # load .env file from path
        load_dotenv(dotenv_path=env_path)
        api_key = os.getenv(key_name)

        return str(api_key)


    def build_request(self,*, method, artist=None, album=None, track=None, format_spec='json', verbose=0):
        #TODO: Verify validity of the built request string.
        """
        Build an request string to pass to API.

        Parameters
        ----------

        method : API Method used (check https://www.last.fm/api)

        artist : The artist name

        track : The track name

        album : The album name

        format_spec : Format specification (JSON or XML)

        verbose : Verbosity level (higher = more verbose)

        Returns
        ----------
        str
            URL of the API Request.

        """
        request_str = self.base_str + self.api_str + '&method='+method

        if artist is not None:
            request_str += '&artist='+self.clean_string(artist)
        if album is not None:
            request_str += '&album='+self.clean_string(album)
        if track is not None:
            request_str += '&track='+self.clean_string(track)
        if format_spec is not None:
            if format_spec == 'json':
                request_str += '&format=json'

        if verbose > 0:
            print('Generated API Request:', request_str)
        return request_str

    def clean_string(self, string):
        """
        Clean string to fit to an HTTP Request.
        Removing tailing whitespaces and replacing special characters.

        Parameters
        ----------

        string : The string to process

        Returns
        ----------
        string
            Cleaned string.
        """
        return str(string).strip().replace('&','%26')
        

    def get_album_matches(self, artist, album, verbose=0):
        #TODO: encode be explicit which parameters are mandatory and optional
        """
        Search for an album by name. (Artist is optional!). Returns album matches sorted by relevance.

        Parameters
        ----------

        artist : The artist name

        album : The album name

        verbose : Verbosity level (higher = more verbose)

        Returns
        ----------
        dict
            Album matches sorted by relevance
        """

        method = 'album.search'
        request_str = self.build_request(method=method, artist=artist, album=album, verbose=verbose)
        return requests.get(request_str).json()

    def get_album_info(self, artist, album, verbose=0):
        #TODO: Check out the musicbrainz id option instead of album name
        """
        Get the metadata and tracklist for an album on Last.fm using the album name. (Artist is optional!)

        Parameters
        ----------

        artist : The artist name

        album : The album name

        verbose : Verbosity level (higher = more verbose)

        Returns
        ----------
        dict
            Album info
        """  

        method = 'album.getinfo'
        try:
            r_data = requests.get(self.build_request(method=method, artist=artist, album=album, verbose=verbose)).json()['album']
        except KeyError:
            r_data = np.nan
        return r_data

    def get_track_info(self, artist, album, track, verbose=0):
        #TODO: Check out the musicbrainz id option instead of track name
        """
        Get the metadata for a track on Last.fm using the artist/track name.

        Parameters
        ----------

        artist : The artist name

        album : The album name

        track : The track name

        verbose : Verbosity level (higher = more verbose)

        Returns
        ----------
        dict
            Track info.
        """

        method = 'track.getinfo'
        try:
            r_data = requests.get(self.build_request(method=method, track=track, artist=artist, album=album, verbose=verbose)).json()['track']
        except KeyError:
            r_data = np.nan

        return r_data

