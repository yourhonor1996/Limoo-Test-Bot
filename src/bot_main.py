from src.util.utility import config_django
config_django()
import asyncio
from limoo import LimooDriver
from src.config import settings
from src.gitlab_async_api import GitlabAsyncConnection
import aiohttp
from src.util import utility
from src.util.utility import LimooMessage
from src.config.settings import Consts, Commands

from src import models
from asgiref.sync import sync_to_async
# TODO creat an event handler class 
# TODO create conveniece classes for this shit ass sdk
# TODO cache the state variables instead of querying them from the database

PROJECTS_STATES = Commands.Gitlab.PROJETS_STATES
WEBHOOK_STATES = Commands.Gitlab.WEBHOOK_STATES
# CUR_PROJECT_STATE = Commands.Gitlab.STATE_END
# CUR_WEBHOOK_STATE = Commands.Gitlab.STATE_END


async def gitlab_respond(event, session):
    # global PROJECTS_STATES
    # global WEBHOOK_STATES
    global CUR_PROJECT_STATE
    global CUR_WEBHOOK_STATE

    if (event['event']== 'message_created' and not (event['data']['message']['type'] or event['data']['message']['user_id'] == self['id'])):
        # create a LimooMessage instance to manipulate messages
        message = LimooMessage(event, ld)
        
        async def show_private_projects():
            """Shows the projects in an acceptable format"""
            connection = await GitlabAsyncConnection.create(session, user.gitlab_token)
            projects = await connection.get_data(f'/users/{connection.user_id}/projects', parameters={'visibility':'private'})
            print(create_user)
        
            # create response text
            response_text = "***Here are your projects:***\n"
            filters = Consts.Gitlab.PROJECTS_FIELD_FILTERS
            for i, project in enumerate(projects):
                response_text += f"**{i+1} - {project['name']}:**\n"
                project_text = utility.format_dict_to_text(project, filters)
                response_text += project_text
            # send the response
            await message.reply_in_thread(response_text)
            
            
        # create or get the user, workspace and conversation
        user, create_user = models.User.objects.get_or_create(user_id= message.user_id)
        workspace, create_workspace = models.WorkSpace.objects.get_or_create(user= user, workspace_id= message.workspace_id)
        conversation, create_conversation = models.Conversation.objects.get_or_create(workspace= workspace, conversation_id= message.conversation_id)

        # create a message thread in the db
        thread_root_id = message.thread_root_id or message.id
        thread, create_thread = models.Thread.objects.get_or_create(conversation= conversation, thread_root_id= thread_root_id)
        
        # # ----------------------------------Gitlab Start----------------------------------- #
        # if we have a /gitlab command ...
        if message.text == Commands.Gitlab.CMD_START:
            # CUR_PROJECT_STATE = Commands.Gitlab.STATE_START
            # CUR_WEBHOOK_STATE = Commands.Gitlab.STATE_START
            thread.conv_state = Commands.Gitlab.STATE_START
            thread.save()
            await message.reply_in_thread(Commands.Gitlab.TEXT_START)

        # # ----------------------------------PROJECTS: Start----------------------------------- #
        elif thread.conv_state == Commands.Gitlab.STATE_START and message.text == Commands.Gitlab.CMD_GITLAB_PROJECTS:
            # if the user already exists and has a gitlab_token then just show the projects
            if not create_user and user.gitlab_token:
                await show_private_projects()
                # CUR_PROJECT_STATE = Commands.Gitlab.STATE_END
                thread.conv_state = Commands.Gitlab.STATE_END
                thread.save()
            else:
                await message.reply_in_thread("Please Enter your private key:")
                # CUR_PROJECT_STATE = PROJECTS_STATES.GET_PVT_KEY
                thread.conv_state = PROJECTS_STATES.GET_PVT_KEY
                thread.save()

        # ------------------------PROJECTS: Get Private Key------------------------- #
        elif thread.conv_state == PROJECTS_STATES.GET_PVT_KEY:
            user_token = str(message.text).strip()
            # if the token is valid -> proceed, else -> ask for it again (the state won't change)
            if utility.validate_gitlab_token(user_token):
                user.gitlab_token = user_token
                user.save()
                await show_private_projects()
                # CUR_PROJECT_STATE = Commands.Gitlab.STATE_END
                thread.conv_state = Commands.Gitlab.STATE_END
                thread.save()
            else:
                await message.reply_in_thread("The token is not valid, pleas enter again!")
            
        # --------------------------PROJECTS: Show_Results-------------------------- #
        # elif CUR_PROJECT_STATE == PROJECTS_STATES.SHOW_RESULTS:
        #     print(5)
            
        #     # message_split = message.text.split()
        #     # visibility = message_split[1]
        #     # token = message_split[2]
        #     # if not visibility in Consts.Gitlab.VALID_VISIBILITIES:
        #     #     response_text = Commands.Gitlab.TEXT_INVALID_COMMAND
        #     # else:
            
        #     # create a connection to the gilab api- the user_id is stored in the api
        #     connection = await GitlabAsyncConnection.create(session, user.gitlab_tokenen)
            
        #     # if visibility == 'all':
        #     # # get all the private projects using the user id and the given parameters
        #     #     projects = await connection.get_data(f'/users/{connection.user_id}/projects')
        #     # else:
        #     #     projects = await connection.get_data(f'/users/{connection.user_id}/projects', parameters={'visibility':visibility})
        #     projects = await connection.get_data(f'/users/{connection.user_id}/projects', parameters={'visibility':'private'})
            
        #     # create response text
        #     response_text = "***Here are your projects:***\n"
        #     filters = Consts.Gitlab.PROJECTS_FIELD_FILTERS
        #     for i, project in enumerate(projects):
        #         response_text += f"**{i+1} - {project['name']}:**\n"
        #         project_text = utility.format_dict_to_text(project, filters)
        #         response_text += project_text
        #     # send the response
        #     CUR_PROJECT_STATE = Commands.Gitlab.STATE_END
        #     await message.reply_in_thread(response_text)
            
        # # -------------------------WEBHOOK: Start webhook-------------------------- #
        # # -------------------------WEBHOOK: Command-Events-------------------------- #
        # elif CUR_WEBHOOK_STATE == WEBHOOK_STATES.CMD_EVENTS:
        #     ...
        # # --------------------------WEBHOOK: Show Webhook--------------------------- #
        # elif CUR_WEBHOOK_STATE == WEBHOOK_STATES.SHOW_WEBHOOK:
        #         ...

                
        # if we have a help command
        if message.text.startswith(Commands.Help.CMD_HELP):
            await message.reply_in_same_context(Commands.Help.HELP_TEXT)
        

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