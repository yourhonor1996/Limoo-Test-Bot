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
import secrets

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

    if (event['event']== 'message_created' and 
        not (event['data']['message']['type'] or event['data']['message']['user_id'] == self['id'])):
        # create a LimooMessage instance to manipulate messages
        message = LimooMessage(event, ld)
        
        async def show_private_projects():
            """Shows the projects in an acceptable format"""
            connection = await GitlabAsyncConnection.create(session, user.gitlab_token)
            projects = await connection.get_data(
                f'/users/{connection.user_id}/projects',
                parameters={'visibility':'private'})
        
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
        workspace, create_workspace = models.WorkSpace.objects.get_or_create(
            user= user, workspace_id= message.workspace_id)
        conversation, create_conversation = models.Conversation.objects.get_or_create(
            workspace= workspace, conversation_id= message.conversation_id)

        # create a message thread in the db
        thread_root_id = message.thread_root_id or message.id
        thread, create_thread = models.Thread.objects.get_or_create(
            conversation= conversation,thread_root_id= thread_root_id)
        
        # # -----------------------------------Gitlab Start------------------------------------ #
        # if we have a /gitlab command ...
        if message.text.strip() == Commands.Gitlab.CMD_START:
            # CUR_PROJECT_STATE = Commands.Gitlab.STATE_START
            # CUR_WEBHOOK_STATE = Commands.Gitlab.STATE_START
            thread.conv_state = Commands.Gitlab.STATE_START
            thread.save()
            await message.reply_in_thread(Commands.Gitlab.TEXT_START)

        # # ----------------------------------PROJECTS: Start----------------------------------- #
        elif (thread.conv_state == Commands.Gitlab.STATE_START and 
            message.text.strip() == Commands.Gitlab.CMD_GITLAB_PROJECTS):
            # if the user already exists and has a gitlab_token then just show the projects
            if not create_user and user.gitlab_token:
                thread.conv_state = Commands.Gitlab.STATE_END
                thread.save()
                await show_private_projects()
                # CUR_PROJECT_STATE = Commands.Gitlab.STATE_END
            else:
                await message.reply_in_thread(Commands.Gitlab.TEXT_PROJECTS_GET_PVT_KEY)
                # CUR_PROJECT_STATE = PROJECTS_STATES.GET_PVT_KEY
                thread.conv_state = PROJECTS_STATES.GET_PVT_KEY
                thread.save()

        # -------------------------------PROJECTS: Get Private Key------------------------------- #
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
            
        # # -------------------------WEBHOOK: Start webhook-------------------------- #
        elif (thread.conv_state == Commands.Gitlab.STATE_START and 
            message.text.strip() == Commands.Gitlab.CMD_GITLAB_WEBHOOK):
            
            if thread.webhook_token:
                token = thread.webhook_token
            else:
                token = secrets.token_hex(Consts.Gitlab.WH_TOKEN_BSIZE)
                thread.webhook_token = token
                thread.save()
            thread.conv_state = Commands.Gitlab.STATE_END
            thread.save()
            await message.reply_in_thread(Commands.Gitlab.TEXT_WEBHOOK_START.format(token= token, url= settings.WEBHOO_ADDRESS))
            
            
        # if we have a help command
        if message.text.startswith(Commands.Help.CMD_HELP):
            await message.reply_in_same_context(Commands.Help.HELP_TEXT)
        

async def main():
    async with aiohttp.ClientSession() as session:
        global ld, self
        
        
        ld = LimooDriver(settings.LIMOO_URL, settings.BOT_USERNAME, settings.BOT_PASSWORD)
        try:
            self = await ld.users.get()
            forever = asyncio.get_running_loop().create_future()
            ld.set_event_handler(lambda event: asyncio.create_task(gitlab_respond(event, session)))
            await forever
        finally:
            await ld.close()

asyncio.run(main())