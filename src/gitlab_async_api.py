import asyncio
from aiohttp import ClientSession
import aiohttp
import json
from src.config import settings
from src.util import utility
from src.config.settings import Consts

class GitlabAsyncConnection():
    """For making api call, first a client session must be created in the main thread 
    and then be passed to an instance from this class (which is created by the class method "create").
    After that, the methods can be called using await.
    
    Pay attention that the main_url should not hava a slash at the end of it.
    """
    
    def __init__(self, session:ClientSession, token:str, main_url= None):
        self.session = session
        self.token = token
        self.main_url = main_url if main_url else Consts.Gitlab.API_V4
        self.user_id = ''
    
    async def _init_async(self):
        '''In order to config async functionality into our class we have created
        an async init method to run necessary async functions'''
        data = await self.get_data('user')
        self.user_id = data['username']
    
    @classmethod
    async def create(cls, session:ClientSession, token:str, main_url=None):
        '''Objects of this class should be created by this method only,
        in order for the asyncio module to run correctly.'''

        instance = GitlabAsyncConnection(session, token, main_url)
        await instance._init_async()
        return instance
    
    async def get_data(self, *urls, **headers_params):
        """Gets a response from the gitlab api with the token in the headers and returns the results as a dictionary.
        The parameters and the headers of the get request must be given as dictionaries as key arguments 
        """
                
        main_url = self.main_url
        for url in urls:
            main_url += f"/{url}"
            
        parameters = headers_params.get('parameters') if headers_params.get('parameters') else {}
        headers = headers_params.get('headers') if headers_params.get('headers') else {}
        # insert token to headers
        headers.update({Consts.Gitlab.PRIVATE_TOKEN_TITLE : self.token})
        
        response = await self.session.get(main_url, headers= headers, params= parameters)
        content = await response.text()
        data = json.loads(content)
        return data
        
        

# async def main():
#     async with aiohttp.ClientSession() as session:
#         connection = await GitlabAsyncConnection.create(session, settings.TOKEN)
#         projects = await connection.get_data(f'/users/{connection.user_id}/projects', parameters={'visibility':'private'})
#         # results = await connection.get_data('user')
#         results = ""
#         for project in projects:
#             response_text = utility.format_dict_to_text(project, GitlabSettings.PROJECTS_FIELD_FILTERS)
#             results += response_text
#         print(results)
#         print(connection.user_id)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())    
        