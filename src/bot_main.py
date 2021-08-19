import asyncio
from limoo import LimooDriver
from src.config import settings
from src.gitlab_async_api import GitlabAsyncConnection
import aiohttp
from src.util import utility
from src.config.settings import Commands, GitlabSettings

# TODO creat an event handler class 
# TODO create conveniece classes for this shit ass sdk


async def respond(event, session):
        data = event['data']
        if (event['event'] == 'message_created' and not (event['data']['message']['type'] or event['data']['message']['user_id'] == self['id'])):
            message_id = event['data']['message']['id']
            thread_root_id = event['data']['message']['thread_root_id']
            direct_reply_message_id = thread_root_id and event['data']['message']['id']

            # if we have a gitlab project command ...
            if event['data']['message']['text'].startswith(Commands.GITLAB_PROJECTS):
                
                message_split = event['data']['message']['text'].split()
                visibility = message_split[1]
                token = message_split[2]
                
                if not visibility in GitlabSettings.VALID_VISIBILITIES:
                    response_text = GitlabSettings.TEXT_INVALID_COMMAND
                else:
                    # create a connection to the gilab api- the user_id is stored in the api
                    connection = await GitlabAsyncConnection.create(session, token)
                    if visibility == 'all':
                    # get all the private projects using the user id and the given parameters
                        projects = await connection.get_data(f'/users/{connection.user_id}/projects')
                    else:
                        projects = await connection.get_data(f'/users/{connection.user_id}/projects', parameters={'visibility':visibility})
                    
                    response_text = "***Here are your projects:***\n"
                    filters = GitlabSettings.PROJECTS_FIELD_FILTERS
                    for i, project in enumerate(projects):
                        response_text += f"**{i+1} - {project['name']}:**\n"
                        project_text = utility.format_dict_to_text(project, filters)
                        response_text += project_text
                    
                    response = await ld.messages.create(
                        workspace_id= data['workspace_id'],
                        conversation_id= event['data']['message']['conversation_id'],
                        text= response_text)
            
            # if we have a help command
            if event['data']['message']['text'].startswith(Commands.HELP):
                text= Commands.HELP_TEXT
                response = await ld.messages.create(
                    workspace_id= data['workspace_id'],
                    conversation_id= event['data']['message']['conversation_id'],
                    text= text)
            

async def main():
    async with aiohttp.ClientSession() as session:
        global ld, self
        ld = LimooDriver('web.limoo.im', settings.BOT_USERNAME, settings.BOT_PASSWORD)
        try:
            self = await ld.users.get()
            forever = asyncio.get_running_loop().create_future()
            ld.set_event_handler(lambda event: asyncio.create_task(respond(event, session)))
            await forever
        finally:
            await ld.close()

asyncio.run(main())