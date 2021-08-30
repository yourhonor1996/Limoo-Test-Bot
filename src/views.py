from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
# from src.bot_main import ld
from limoo import LimooDriver
from src.config import settings
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync, sync_to_async
from rest_framework.decorators import api_view
from rest_framework.response import Response
from src import models

@sync_to_async
def get_thread_info(webhook_token):
    # TODO create exception handling for when we can't the data
    thread = models.Thread.objects.get(webhook_token= webhook_token)
    thread_root_id = thread.thread_root_id
    conversation = thread.conversation
    conversation_id = conversation.conversation_id
    workspace_id = conversation.workspace.workspace_id
    return thread_root_id, conversation_id, workspace_id

# Create your views here.
@csrf_exempt
@async_to_sync
async def webhook(request:HttpRequest):
    ld = LimooDriver(settings.LIMOO_URL, settings.BOT_USERNAME, settings.BOT_PASSWORD)
    
    if request.method == "POST":
        webhook_token = request.headers.get(settings.Consts.Gitlab.HEADER_WEHBOOK_TOKEN)
        event_name = request.headers.get(settings.Consts.Gitlab.HEADER_GITLAB_EVENT)
        thread_root_id, conversation_id, workspace_id = await get_thread_info(webhook_token)
        text = settings.Consts.Gitlab.TEXT_EVENT_NOTIF.format(event_name= event_name)
        # send the data to limoo
        await ld.messages.create(
            workspace_id= workspace_id,
            conversation_id= conversation_id,
            thread_root_id= thread_root_id,
            text= text)
        ld.close()
        return HttpResponse("OK")
        

