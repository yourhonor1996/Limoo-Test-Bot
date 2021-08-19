from pathlib import Path

# this is the src folder 
BASE_DIR = Path(__file__).resolve().parent.parent

TOKEN = '15g1MjRw9iyHJypTDxwz'

GITLAB_PRIVATE_TOKEN_KEY = 'PRIVATE-TOKEN'

GITLAB_API_V4 = "https://gitlab.com/api/v4"

BOTMAIN_FILENAME = 'bot_main'

VENV_FOLDERNAME = '.venv'

VENV_PYTHON_PATH = (BASE_DIR.parent / VENV_FOLDERNAME / "Scripts" / "python.exe")

BOT_USERNAME = 'test-bot1'

BOT_PASSWORD = 'tyz2jsps2xo9ba2ck3ok'



REQ_FILENAME = 'requirements.txt'

class Commands():
    GITLAB_PROJECTS = "/gitlab-projects"
    HELP = "/help"
    HELP_TEXT = """سلام این یک بات تست هست.
با استفاده از دستوری های زیر میتونید از این بات استفاده بکنید:
/gitlab-projects : 
بعد از نوشتن این دستور باید نوع پروژه هایی که میخواید مشاهده بکنید رو بنویسید.
یعنی یکی از سه عبارت "private" – "public" – "internal" و یا "all".
هر کدوم از سه عبارت بالا باعث میشن انواع پروژه های مربوط با این visibility ها برای شما نشون داده بشه و عبارت all هم تمام پروژه های شما رو براتون لیست میکنه.
بعد از نوشتن نوع پروژه ها باید gitlab private access token خودتون رو وارد کنید.
برای مثال:
/gitlab-pojects private <<your token>>
"""

class GitlabSettings:
    PROJECTS_FIELD_FILTERS = ['id', 'name','web_url', 'visibility']
    VALID_VISIBILITIES = ['public', 'private', 'internal', 'all']
    TEXT_INVALID_COMMAND = "دستور وارد شده به شکل صحیح نمیباشد. برای اطلاع از نحوه نوشتن دستورات دستور /help را اجرا کنید."