import subprocess
from src.config import settings

venv_path = str(settings.VENV_PYTHON_PATH)
subprocess.run([venv_path, 'botmanage.py', 'runbot'])
