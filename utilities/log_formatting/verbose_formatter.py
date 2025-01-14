import logging
from typing import Dict

from colorama import Fore, Style

class VerboseConsoleFormatter(logging.Formatter):
    """A verbose formatter that includes ASCII escape characters for coloring."""
    _issue_format: str = '%(asctime)s {name} {{color}}{level:^10} {reset}%(message)s'.format( name='%(name)-20s', level='%(levelname)-10s', reset=Style.RESET_ALL,)
    default_time_format = '%H:%M:%S'
    default_msec_format = '%s.%03d'

    def _get_color(self, logging_level: int) -> str:
        color_dictionary = {logging.ERROR: Fore.RED, 
                logging.WARNING: Fore.YELLOW, 
                logging.DEBUG: Fore.CYAN, 
                logging.INFO: Fore.WHITE}
        return color_dictionary[logging_level]
   
    def __init__(self):
        super().__init__()
        
    def format(self, record) -> str:
        self._style._fmt = self._issue_format.format(color=self._get_color(record.levelno))
        return logging.Formatter.format(self, record)
    

class VerboseFormatter(VerboseConsoleFormatter):
    def _get_color(logging_level):
        return Fore.WHITE
