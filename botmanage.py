from src.config.settings import VENV_PYTHON_PATH, BOTMAIN_FILENAME
import subprocess
import sys, os

import subprocess
from src.config import settings
import logging



def main():
    '''
    Run commands from the commandline using this file and the relative commands.
        For running files inside the src folder, use the -m command in order for the 
        absolute and relative imports to work.
    This file can run files inside the "src" folder and can also start the bot using the "runbot" command.
        In order to run files inside the src folder just write file as a module, the src folder is a given as a 
        module parent directory without the .py in the end.
    Example:
        python botmanage.py runfile utility.somefile
    '''
    platform  = sys.platform
    arguments = sys.argv
    length = len(arguments)
    if length == 2:
        if arguments[1] == 'runbot':
            if platform == 'linux':
                subprocess.check_call(['python3', '-m', f"src.{BOTMAIN_FILENAME}" ])
            else:
                subprocess.check_call([VENV_PYTHON_PATH, '-m', f"src.{BOTMAIN_FILENAME}" ])
        elif arguments[1] == 'install':
            # this install process is only configured for windows not linux, in linux installation is done through dockerfile
            venv_path = str(settings.VENV_PYTHON_PATH)
            subprocess.check_call(['py', '-m', 'venv', settings.VENV_FOLDERNAME])
            subprocess.check_call([venv_path, '-m', 'pip', 'install', '--upgrade', 'pip'])
            subprocess.check_call([venv_path,'-m','pip', 'install','-r', settings.REQ_FILENAME])
            input("\n\nPress Enter to exit")
        else:
            print('Command not liested.')

    elif length == 3:
        if arguments[1] == 'runfile':
            if platform == 'linux':
            # this install process is only configured for windows not linux, in linux installation is done through dockerfile
                subprocess.check_call(['python3', '-m', f"src.{arguments[2]}"])
            else:
                subprocess.check_call([VENV_PYTHON_PATH, '-m', f"src.{arguments[2]}"])
                
        else:
            print('Command not supported.')
    else:
        print('Command not supported.')

        
if __name__ == '__main__':
    main()