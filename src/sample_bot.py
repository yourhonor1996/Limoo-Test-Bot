import asyncio
from limoo import LimooDriver
from src.config import settings

async def respond(event):
    data = event['data']
    message = data['message']
    if (event['event'] == 'message_created'
        and not (message['type'] or message['user_id'] == self['id'])):
        message_id = message['id']
        thread_root_id = message['thread_root_id']
        direct_reply_message_id = message['thread_root_id'] and message['id']
        response = await ld.messages.create(
	    data['workspace_id'],
	    message['conversation_id'],
	    message['text'],
	    thread_root_id=thread_root_id or message_id,
	    direct_reply_message_id=thread_root_id and message_id)

async def main():
    global ld, self
    ld = LimooDriver('web.limoo.im', settings.BOT_USERNAME, settings.BOT_PASSWORD)
    try:
        self = await ld.users.get()
        forever = asyncio.get_running_loop().create_future()
        ld.set_event_handler(lambda event: asyncio.create_task(respond(event)))
        await forever
    finally:
        await ld.close()

asyncio.run(main())