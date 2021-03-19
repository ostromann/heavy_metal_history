import requests
from dotenv import load_dotenv
import numpy as np
import os
import sys
import urllib.parse
import xmltodict
import yaml
import time

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

        with open('metalhistory/config.yaml') as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)

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
        return urllib.parse.quote(str(string).strip())
        

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

        response = requests.get(self.build_request(method=method, verbose=verbose, **kwargs))
        if not response.ok:
            raise RuntimeError('LastFM API responded with status code %s.' % (response.status_code))

        return response.json()


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
        valid_args = ['artist', 'album', 'mbid', 'autocorrect', 'username', 'lang', 'fields']
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

        response = requests.get(self.build_request(method=method, verbose=verbose, **kwargs))
        if not response.ok:
            raise RuntimeError('LastFM API responded with status code %s.' % (response.status_code))

        try:
            try:
                r_data = requests.get(self.build_request(method=method, verbose=verbose, **kwargs)).json()['album']
                fields = kwargs['fields'] if 'fields' in kwargs.keys() else None
                if fields is not None:
                    r_dict = self.response_formatter(r_data, fields)
                    return r_dict
            except ValueError:
                print('JSONDecodeError while querying for', kwargs['artist'], kwargs['album'])
                r_data = np.nan
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

        response = requests.get(self.build_request(method=method, verbose=verbose, **kwargs))
        if not response.ok:
            raise RuntimeError('LastFM API responded with status code %s.' % (response.status_code))

        try:
            r_data = response.json()['track']
        except KeyError:
            r_data = np.nan

        return r_data


    def get_tags(self, tags):
        """
        Retrieve list of tags from nested dictionary of attachted tags to an album.

        Parameters
        ----------

        tags : nested dictionary of tags.

        Returns
        ----------
        list
            List of tags.

        """
        tag_list = []
        ignored_tag_list = []
        for tag in tags['tag']:
            if type(tag['name'])==str:
                name = tag['name']
                if tag['name'].lower() in self.config['user settings']['accepted tags']:
                    tag_list.append(tag['name'].lower())
                else:
                    ignored_tag_list.append(tag['name'].lower())
        return tag_list, ignored_tag_list

    def get_release_date(self, mbid):
        """
        Retrieve the releaste date of an album based on a musicbrainz id.

        Parameters
        ----------

        mbid : musicbrainz id

        Returns
        ----------
        str
            Release date of the album.

        """
        if mbid is not None:
            response = requests.get('http://musicbrainz.org/ws/2/release/' + str(mbid) + '?inc=release-groups&fmt=xml')
            while response.status_code == 503:
                retry_margin = 2
                retry_after = int(response.headers['Retry-After']) + retry_margin
                
                print('Response code 503. Waiting for %d seconds.' % (retry_after))
                time.sleep(retry_after)
                response = requests.get('http://musicbrainz.org/ws/2/release/' + str(mbid) + '?inc=release-groups&fmt=xml')

            if response.status_code == 200:
                response_dict = xmltodict.parse(response.text)
                release_date = response_dict['metadata']['release']['release-group']['first-release-date']
                return release_date
            
            if response.status_code == 404:
                return None
            
            else:
                raise RuntimeError('Musicbrainz API responded with status code', response.status_code)

        else:
            return None

    def response_formatter(self, json, fields):
        """
        Format the large json response to a dictionary of requested fields

        Parameters
        ----------

        json : LastFM response of a album info.

        fields : list of fields to be returned

        Returns
        ----------
        dict
            Request fields of album info.

        """
        r_dict = {}
        if type(fields) == str:
            fields = [fields]

        for field in fields:
            if field not in self.config['system settings']['lastfm']['accepted fields']:
                print('\'%s\' not in list of accepted fields! Setting value to None. Check metalhistory/config.yaml for accepted fields.' % (field))
                r_dict[field] = None
            else:
                if field == 'release-date':
                    r_dict[field] = self.get_release_date(json['mbid'])
                elif field == 'tags':
                    r_dict[field], r_dict['ignored tags'] = self.get_tags(json['tags'])
                else:
                    r_dict[field] = json[field]
        return r_dict
