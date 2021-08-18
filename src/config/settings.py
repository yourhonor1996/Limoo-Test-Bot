from pathlib import Path

# this is the src folder 
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)

TOKEN = '15g1MjRw9iyHJypTDxwz'

GITLAB_PRIVATE_TOKEN_KEY = 'PRIVATE-TOKEN'

GITLAB_API_V4 = "https://gitlab.com/api/v4"

BOTMAIN_FILENAME = 'bot_main'

VENV_FOLDERNAME = '.venv'

VENV_PYTHON_PATH = (BASE_DIR.parent / VENV_FOLDERNAME / "Scripts" / "python.exe")