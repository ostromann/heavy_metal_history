import requests
from dotenv import load_dotenv
import numpy as np
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

        api_key = self.authenticate_from_dotenv('LASTFM_API_KEY')
        self.api_str = '&api_key=' + api_key
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


    def build_request(self, method, format_spec='json', verbose=0, **kwargs):
        """
        Build a request string to pass to API. Note that the method-specific
        API arguments are not validated here, this should be done beforehand.

        Parameters
        ----------

        method : API Method used (check https://www.last.fm/api)

        format_spec : Format specification (JSON or XML)

        verbose : Verbosity level (higher = more verbose)
        
        kwargs : Method-specific keyword arguments for the API request

        Returns
        ----------
        str
            URL of the API Request.

        """
        request_str = self.base_str + self.api_str + '&method='+method
        
        for key in kwargs.keys():
            request_str += '&' + key + '=' + self.clean_string(kwargs[key])
        
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
        

    def get_album_matches(self, verbose=0, **kwargs):
        """
        Search for an album by name. Returns album matches sorted by relevance.
        The arguments to the API request are specified as keyword arguments.
        See https://www.last.fm/api/show/album.search for a description of
        required and optional arguments as well as combinations thereof.

        Parameters
        ----------

        verbose : Verbosity level (higher = more verbose)
        
        kwargs : Keyword arguments specifying the album.search API request

        Raises
        ----------
        
        ValueError : If the arguments are not valid

        Returns
        ----------
        dict
            Album matches sorted by relevance
        """

        # Check that all keyword arguments are valid
        valid_args = ['limit', 'page', 'album']
        for key in kwargs.keys():
            if key not in valid_args:
                raise ValueError('%s is not in the list of valid keyword arguments.' % key)
        
        # Check that an album is specified
        if 'album' not in kwargs.keys():
            raise ValueError('An album must be specified.')
        
        method = 'album.search'
        request_str = self.build_request(method=method, verbose=verbose, **kwargs)
        return requests.get(request_str).json()


    def get_album_info(self, verbose=0, **kwargs):
        """
        Get the metadata and tracklist for an album on Last.fm. The arguments
        to the API request are specified as keyword arguments. See
        https://www.last.fm/api/show/album.getInfo for a description of
        required and optional arguments as well as combinations thereof.

        Parameters
        ----------

        verbose : Verbosity level (higher = more verbose)
        
        kwargs : Keyword arguments specifying the album.getInfo API request
        
        Raises
        ----------
        
        ValueError : If the arguments are not valid

        Returns
        ----------
        dict
            Album info
        """
        
        # Check that all keyword arguments are valid
        valid_args = ['artist', 'album', 'mbid', 'autocorrect', 'username', 'lang']
        for key in kwargs.keys():
            if key not in valid_args:
                raise ValueError('%s is not in the list of valid keyword arguments.' % key)
        
        # If mbid is specified, validate that none of artist/album are specified simultaneously
        mbid = kwargs['mbid'] if 'mbid' in kwargs.keys() else None
        if mbid is not None and any(x in kwargs.keys() for x in ['artist', 'album']):
            raise ValueError('mbid was given together with artist or album.\n' + \
                             'Specify either mbid only, or both artist+album.')
        
        # If mbid is not specified, check that both artist/album are specified
        if mbid is None and not all(x in kwargs.keys() for x in ['artist', 'album']):
            raise ValueError('Neither mbid nor artist+album was specified.\n' + \
                             'Specify either mbid only, or both artist+album.')
        
        # Check that autocorrect is either 0 or 1
        autocorrect = kwargs['autocorrect'] if 'autocorrect' in kwargs.keys() else None
        if autocorrect is not None and autocorrect not in [0, 1, 0., 1., '0', '1']:
            raise ValueError('autocorrect argument must be either 0 or 1.')
        
        method = 'album.getinfo'
        try:
            r_data = requests.get(self.build_request(method=method, verbose=verbose, **kwargs)).json()['album']
        except KeyError:
            r_data = np.nan
        return r_data


    def get_track_info(self, verbose=0, **kwargs):
        """
        Get the metadata for a track on Last.fm. The arguments to the API
        request are specified as keyword arguments. See
        https://www.last.fm/api/show/track.getInfo for a description of
        required and optional arguments as well as combinations thereof.

        Parameters
        ----------

        verbose : Verbosity level (higher = more verbose)
        
        kwargs : Keyword arguments specifying the track.getInfo API request
        
        Raises
        ----------
        
        ValueError : If the arguments are not valid

        Returns
        ----------
        dict
            Track info.
        """
        
        # Check that all keyword arguments are valid
        valid_args = ['mbid', 'track', 'artist', 'username', 'autocorrect']
        for key in kwargs.keys():
            if key not in valid_args:
                raise ValueError('%s is not in the list of valid keyword arguments.' % key)
        
        # If mbid is specified, validate that none of artist/track are specified simultaneously
        mbid = kwargs['mbid'] if 'mbid' in kwargs.keys() else None
        if mbid is not None and any(x in kwargs.keys() for x in ['artist', 'track']):
            raise ValueError('mbid was given together with artist or track.\n' + \
                             'Specify either mbid only, or both artist+track.')
        
        # If mbid is not specified, check that both artist/track are specified
        if mbid is None and not all(x in kwargs.keys() for x in ['artist', 'track']):
            raise ValueError('Neither mbid nor artist+track was specified.\n' + \
                             'Specify either mbid only, or both artist+track.')
        
        # Check that autocorrect is either 0 or 1
        autocorrect = kwargs['autocorrect'] if 'autocorrect' in kwargs.keys() else None
        if autocorrect is not None and autocorrect not in [0, 1, 0., 1., '0', '1']:
            raise ValueError('autocorrect argument must be either 0 or 1.')
        
        method = 'track.getinfo'
        try:
            r_data = requests.get(self.build_request(method=method, verbose=verbose, **kwargs)).json()['track']
        except KeyError:
            r_data = np.nan

        return r_data

