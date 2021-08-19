import subprocess
from src.config import settings

try:
    subprocess.check_call(['py', '-m', 'venv', settings.VENV_FOLDERNAME])
    subprocess.check_call(['py', '-m', 'pip', 'install', '--upgrade', 'pip'])
except:
    subprocess.check_call(['py', '-m', 'venv', settings.VENV_FOLDERNAME])
    subprocess.check_call(['py', '-m', 'pip', 'install', '--upgrade', 'pip'])
    
subprocess.check_call([str(settings.VENV_PYTHON_PATH),'-m','pip', 'install','-r', settings.REQ_FILENAME])