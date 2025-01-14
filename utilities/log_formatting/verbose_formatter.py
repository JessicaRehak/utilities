import logging
from typing import Dict

from colorama import Fore, Style

class VerboseConsoleFormatter(logging.Formatter):
    _issue_format: str = '%(asctime)s {name} {{color}}{level:^10} {reset}%(message)s'.format( name='%(name)-10s', level='%(levelname)-7s', reset=Style.RESET_ALL,)
    _formats: Dict[int, str] = {logging.ERROR: _issue_format.format(color=Fore.RED), 
                                logging.WARNING: _issue_format.format(color=Fore.YELLOW), 
                                logging.DEBUG: _issue_format.format(color=Fore.CYAN), 
                                logging.INFO: _issue_format.format(color=Fore.WHITE), 
                                }
    default_time_format = '%H:%M:%S'
    default_msec_format = '%s.%03d'
   
    def __init__(self):
        super().__init__()
        
    def format(self, record) -> str:
        self._style._fmt = VerboseConsoleFormatter._formats[record.levelno]
        return logging.Formatter.format(self, record)
    