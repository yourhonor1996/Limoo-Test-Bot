import asyncio
from limoo import LimooDriver
from src.config import settings
from src.gitlab_async_api import GitlabAsyncConnection
import aiohttp
from src.util import utility
from src.util.utility import LimooMessage
from src.config.settings import Consts

# TODO creat an event handler class 
# TODO create conveniece classes for this shit ass sdk


async def gitlab_respond(event, session):

    if (event['event']== 'message_created' and not (event['data']['message']['type'] or event['data']['message']['user_id'] == self['id'])):
        message = LimooMessage(event, ld)

        # if we have a gitlab project command ...
        if message.text.startswith(Consts.Commands.GITLAB_PROJECTS):
            
            message_split = message.text.split()
            visibility = message_split[1]
            token = message_split[2]
            
            if not visibility in Consts.Gitlab.VALID_VISIBILITIES:
                response_text = Consts.Gitlab.TEXT_INVALID_COMMAND
            else:
                # create a connection to the gilab api- the user_id is stored in the api
                connection = await GitlabAsyncConnection.create(session, token)
                if visibility == 'all':
                # get all the private projects using the user id and the given parameters
                    projects = await connection.get_data(f'/users/{connection.user_id}/projects')
                else:
                    projects = await connection.get_data(f'/users/{connection.user_id}/projects', parameters={'visibility':visibility})
                
                response_text = "***Here are your projects:***\n"
                filters = Consts.Gitlab.PROJECTS_FIELD_FILTERS
                for i, project in enumerate(projects):
                    response_text += f"**{i+1} - {project['name']}:**\n"
                    project_text = utility.format_dict_to_text(project, filters)
                    response_text += project_text
                
                await message.reply_in_thread(response_text)
        
        # if we have a help command
        if message.text.startswith(Consts.Commands.HELP):
            await message.reply_in_same_context(Consts.Commands.HELP_TEXT)
        

async def main():
    async with aiohttp.ClientSession() as session:
        global ld, self
        ld = LimooDriver('web.limoo.im', settings.BOT_USERNAME, settings.BOT_PASSWORD)
        try:
            self = await ld.users.get()
            forever = asyncio.get_running_loop().create_future()
            ld.set_event_handler(lambda event: asyncio.create_task(gitlab_respond(event, session)))
            await forever
        finally:
            await ld.close()

asyncio.run(main())