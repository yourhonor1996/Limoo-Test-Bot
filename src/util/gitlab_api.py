
import requests
import json
from src.config import settings
from src.config.settings import Consts



class GitlabAPI():
    
    def __init__(self, token:str, main_url= None) -> None:
        self.token = token
        self.main_url = main_url if main_url else Consts.Gitlab.API_V4
        self.user_id = self.get_user_id()
    
    
    def get_data_with_token(self, *urls, **headers_params):
        """Gets a response from the gitlab api with the token in the headers and returns the results as a dictionary.
        
        The parameters and the headers of the get request must be in the headers_param dictionary, specified with the words:
        'headers' and 'parameters' as dictionaries.

        Returns:
            a tuple of (int, list[dict]) = (status_code, results)
        """
        main_url = self.main_url
        for url in urls:
            main_url += f"/{url}"
        
        parameters = headers_params.get('parameters') if headers_params.get('parameters') else {}
        headers = headers_params.get('headers') if headers_params.get('headers') else {}
        
        headers.update({Consts.Gitlab.PRIVATE_TOKEN_TITLE : self.token})
        response = requests.get(main_url, headers= headers, params= parameters)
        jsonify = json.loads(response.content)

        return int(response.status_code), jsonify


    def data_from_user(self, needed_data:"str | list[str]"):
        """Gets the needed data from the user API and returns a dictionary of the results.

        Args:
            needed_data (str): the data needed to be filtered from the results dictiornary

        Raises:
            Exception: when the type of the given data is not right

        Returns:
            str | dict[str:str]: results
        """
        statuscode, data = self.get_data_with_token('user')
        if type(needed_data) is str:
            return data[needed_data]
        elif type(needed_data) is list:
            results = {}
            for item in needed_data:
                results.update({item : data[item]})
            return results
        else:
            raise Exception('The given data type is not appropriate.')


    def get_user_id(self):
        return self.data_from_user('username')
    
    
    def get_projects(self, visibility= None):
        '''Returns a list of projects based on their visibility. 
        Visibility can be either: public, internal, private
        If visibility is None it will return all repositories.'''
        if visibility:
            status, results = self.get_data_with_token(f'users/{self.user_id}/projects', parameters= {'visibility':visibility})
            return results
        status, results = self.get_data_with_token(f'users/{self.user_id}/projects')


