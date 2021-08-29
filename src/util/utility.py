from limoo import LimooDriver


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
    

class LimooMessage():
    """Creates an instance of limoo message which can be used to get message data or reply 
    to messages.
    """

    def __init__(self, event, ld:LimooDriver):
        # event and conversation and workspace data
        self.event = event
        self.ld = ld
        self.event_text = event['event']
        self.message_type = event['data']['message']['type']
        self.workspace_id = event['data']['workspace_id']
        self.conversation_id = event['data']['message']['conversation_id']
        self.event_data = event['data']

        # message data
        self.text = event['data']['message']['text']
        self.message_id = event['data']['message']['id']
        self.thread_root_id = event['data']['message']['thread_root_id']
        self.message_user_id = event['data']['message']['user_id']
        
        
    async def reply_in_conversation(self, text):
        """Replies to the message in the same conversation but doesn't directly reply to it"""
        response = await self.ld.messages.create(
            workspace_id= self.workspace_id,
            conversation_id= self.conversation_id,
            text= text)

    # TODO create a function that responds to a message in a conversation and directly replies to it

    async def reply_in_thread(self, text):
        """Replies to the message in a thread but doesn't directly reply to it"""
        response = await self.ld.messages.create(
            workspace_id= self.workspace_id,
            conversation_id= self.conversation_id,
            text= text,
            thread_root_id= self.thread_root_id or self.message_id)

    async def reply_in_thread_direct(self, text):
        """Replies to the message in a thread and directly replies to it"""
        response = await self.ld.messages.create(
            workspace_id= self.workspace_id,
            conversation_id= self.conversation_id,
            text= text,
            thread_root_id= self.thread_root_id or self.message_id,
            direct_reply_message_id= self.thread_root_id and self.message_id)

    @property
    def is_in_conversation(self):
        """Is the message in a conversation?"""
        return self.thread_root_id is None

    @property
    def is_in_thread(self):
        """Is the message in a thread?"""
        return (self.message_id is not None) and (self.thread_root_id is not None)