import logging
from typing import Dict

from colorama import Fore, Style

class VerboseConsoleFormatter(logging.Formatter):
    """A verbose formatter that includes ASCII escape characters for coloring."""
    _issue_format: str = '%(asctime)s {name} {{color}}{level:^10} %(message)s{{reset}}'.format( name='%(name)-20s', level='%(levelname)-10s')
    default_time_format = '%H:%M:%S'
    default_msec_format = '%s.%03d'

    def _get_color(self, logging_level: int) -> str:
        color_dictionary = {logging.ERROR: Fore.RED, 
                logging.WARNING: Fore.YELLOW, 
                logging.DEBUG: Fore.CYAN, 
                logging.INFO: Fore.WHITE}
        return color_dictionary[logging_level]

    def _get_reset(self) -> str:
        return Fore.RESET
   
    def __init__(self):
        super().__init__()
        
    def format(self, record) -> str:
        self._style._fmt = self._issue_format.format(color=self._get_color(record.levelno), reset=self._get_reset())
        return logging.Formatter.format(self, record)
    

class VerboseFormatter(VerboseConsoleFormatter):
    def _get_color(self, logging_level):
        return ''

    def _get_reset(self):
        return ''
