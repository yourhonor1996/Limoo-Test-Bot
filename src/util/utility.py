from limoo import LimooDriver
import os
from django import setup

def filter_dict(dictionary:dict, filters:list):
    '''Filters the dictionary and returns a new dictionary based on the filterd keys'''
    results = {}
    for filter in filters:
        results.update({filter : dictionary[filter]})
    return results

def format_dict_to_text(dictionary:dict, filters= None):
    '''Returns a readable formatted text containing the elements of the dictionary.
    You can also filter the results in the dictionary by asigning the filters variable.
    Make sure that all the keys in the dictionary are strings or have a proper string representation.'''

    if filters:
        dictionary = filter_dict(dictionary, filters)
    result = ''
    for key, value in dictionary.items():
        result += f"   - {str(key).title()}: {value}\n"
    return result

def validate_gitlab_token(token:str):
    # TODO implement this function or create a django ModelForm to validate the data
    return True

def config_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'limoo_bot.settings')
    # TODO make the code run without making django async unsafe
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    # from django.core.asgi import get_asgi_application
    # application = get_asgi_application()
    setup()  


class LimooMessage():
    """Creates an instance of limoo message which can be used to get message data or reply 
    to messages.
    """

    def __init__(self, event, ld:LimooDriver):
        # event and conversation and workspace data
        self.event = event
        self.ld = ld
        self.event_text = event['event']
        self.type = event['data']['message']['type']
        self.workspace_id = event['data']['workspace_id']
        self.conversation_id = event['data']['message']['conversation_id']
        self.event_data = event['data']
        self.user_id = event['data']['message']['user_id']
        # message data
        self.text = event['data']['message']['text']
        self.id = event['data']['message']['id']
        self.thread_root_id = event['data']['message']['thread_root_id']
        
        
    async def reply_in_conversation(self, text):
        """Replies to the message in the same conversation but doesn't directly reply to it"""
        await self.ld.messages.create(
            workspace_id= self.workspace_id,
            conversation_id= self.conversation_id,
            text= text)

    # TODO create a function that responds to a message in a conversation and directly replies to it

    async def reply_in_thread(self, text):
        """Replies to the message in a thread but doesn't directly reply to it.
        If the message is in a conversation it will create a thread"""
        await self.ld.messages.create(
            workspace_id= self.workspace_id,
            conversation_id= self.conversation_id,
            text= text,
            thread_root_id= self.thread_root_id or self.id)

    async def reply_in_thread_direct(self, text):
        """Replies to the message in a thread and directly replies to it.
        If the message is in a conversation it will create a thread"""
        await self.ld.messages.create(
            workspace_id= self.workspace_id,
            conversation_id= self.conversation_id,
            text= text,
            thread_root_id= self.thread_root_id or self.id,
            direct_reply_message_id= self.thread_root_id and self.id)

    async def reply_in_same_context(self, text):
        """Replies to the message in the same context; 
        meaning that if it is in a conversation it will respond in a conversation,
        and if it is in a thread it will respond in the same thread"""
        if self.is_in_conversation:
            await self.reply_in_conversation(text)
        if self.is_in_thread:
            await self.reply_in_thread(text)
            
    @property
    def is_in_conversation(self):
        """Is the message in a conversation?"""
        return self.thread_root_id is None

    @property
    def is_in_thread(self):
        """Is the message in a thread?"""
        return (self.id is not None) and (self.thread_root_id is not None)
    
