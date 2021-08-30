from pathlib import Path
import sys
from requests import get as GET

# this is the src folder 
BASE_DIR = Path(__file__).resolve().parent.parent

TOKEN = '15g1MjRw9iyHJypTDxwz'

BOTMAIN_FILENAME = 'bot_main'

VENV_FOLDERNAME = '.venv'

LIMOO_URL = 'web.limoo.im'

BOT_USERNAME = 'test-bot1'

BOT_PASSWORD = 'tyz2jsps2xo9ba2ck3ok'

REQ_FILENAME = 'requirements.txt'

HOST_EXT_IP = str(GET("https://api.ipify.org/").content, "utf-8")

WEBHOO_ADDRESS = f"http://{HOST_EXT_IP}/webhook"

def get_python_path(platform):
    if platform == 'linux':
        return BASE_DIR.parent / VENV_FOLDERNAME / "bin" / "python3"
    else:
        return BASE_DIR.parent / VENV_FOLDERNAME / "Scripts" / "python.exe"

VENV_PYTHON_PATH = get_python_path(sys.platform)


    
class Consts():
    class Gitlab():
        # API_V4 = "https://gitlab.com/api/v4"
        API_V4 = "http://185.206.92.17/api/v4"
        PROJECTS_FIELD_FILTERS = ['id', 'name','web_url', 'visibility']
        VALID_VISIBILITIES = ['public', 'private', 'internal', 'all']
        PRIVATE_TOKEN_TITLE = 'PRIVATE-TOKEN'
        WH_TOKEN_BSIZE = 16
        # headers
        HEADER_WEHBOOK_TOKEN = "X-Gitlab-Token"
        HEADER_GITLAB_EVENT = "X-Gitlab-Event"
        # texts
        TEXT_EVENT_NOTIF = "You have a new event in gitlab.\n- Event Name: {event_name}"
        


class Commands():
    class Gitlab():
        # commands
        CMD_START = "/gitlab"
        CMD_GITLAB_PROJECTS = "projects"
        CMD_GITLAB_WEBHOOK = "events"
        
        # command messages
        TEXT_INVALID_COMMAND = "دستور وارد شده به شکل صحیح نمیباشد. برای اطلاع از نحوه نوشتن دستورات دستور /help را اجرا کنید."
        TEXT_START = f"""سلام. من بات گیت لب هستم و از دوتا دستور پشتیبانی میکنم:
({CMD_GITLAB_PROJECTS}) - ({CMD_GITLAB_WEBHOOK})
- دستور projects: این دستور لیست پروژه های خصوصی شما رو از گیت لب میگیره و بهتون نمایش میده.

- دستور events: این دستور رویدادهایی که در یک پروژه از گیت لب رخ میدن رو توی همین گروه بهتون اطلاع میده.
لطفا یکی از این دو دستور رو وارد کنید:"""
        TEXT_PROJECTS_GET_PVT_KEY = "لطفا رمز دسترسی شخصی خود را در گیت لب وارد کنید:"
        TEXT_WEBHOOK_START = """لطفا این URL و Token را در تنظیمات WebHook مورد نظر در گیت لب وارد کنید:
- URL: {url}
- Token: {token}"""

        # states 
        STATE_START = 0
        STATE_END = -1
        # other
        class PROJETS_STATES():
            GET_PVT_KEY, SHOW_RESULTS = range(1, 3) 
        class WEBHOOK_STATES():
            CMD_EVENTS, SHOW_WEBHOOK = range(3, 5) 
            
    
    class Help():
        CMD_HELP = "/help"
        HELP_TEXT = """سلام. من بات گیت لب هستم. لطفا برای شروع دستور /gitlab رو وارد کنید."""