import asyncio
from limoo import LimooDriver
from src.config import settings
from src.gitlab_async_api import GitlabAsyncConnection
import aiohttp
from src.util import utility

# TODO creat an event handler class 
# TODO create conveniece classes for this shit ass sdk


async def respond(event, session):
        data = event['data']
        # event['data']['message'] = data['event['data']['message']']

        if (event['event'] == 'message_created' and not (event['data']['message']['type'] or event['data']['message']['user_id'] == self['id'])):
            message_id = event['data']['message']['id']
            thread_root_id = event['data']['message']['thread_root_id']
            direct_reply_message_id = thread_root_id and event['data']['message']['id']

            if event['data']['message']['text'].startswith("/gitlab-projects"):
                token = event['data']['message']['text'].split()[1]
                connection = await GitlabAsyncConnection.create(session, token)
                projects = await connection.get_data(f'/users/{connection.user_id}/projects')

                results = []
                filters = settings.PROJECTS_FIELD_FILTERS
                for project in projects:
                    results.append(utility.filter_dict(project, filters))
                response_text = str(results)
                
            
            response = await ld.messages.create(
                workspace_id= data['workspace_id'],
                conversation_id= event['data']['message']['conversation_id'],
                text= response_text,
                thread_root_id= thread_root_id or message_id,
                direct_reply_message_id= direct_reply_message_id)
            

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