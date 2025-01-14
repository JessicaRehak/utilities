from logging.config import dictConfig
from typing import Dict

INFO_CONSOLE = { 
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout', 
                }

DEBUG_CONSOLE = { 
                 'level': 'DEBUG', 
                 'formatter': 'verbose_console', 
                 'class': 'logging.StreamHandler',
                 'stream': 'ext://sys.stdout',
                 }

ROTATING_FILE_HANDLER = { 
                         'level': 'INFO', 
                         'formatter': 'verbose', 
                         'class': 'logging.handlers.RotatingFileHandler', 
                         'filename': 'info.log', 
                         'mode': 'a', 
                         'maxBytes': 1048576, 
                         'backupCount': 100,
}

ERROR_FILE_HANDLER = { 
                      'level': 'WARNING', 
                      'formatter': 'verbose', 
                      'class': 'logging.FileHandler', 
                      'filename': 'error.log', 
                      'mode': 'a', 
                      }

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            '()': 'utilities.log_formatting.simple_formatter.SimpleConsoleFormatter',
        },
        'verbose': {
            '()': 'utilities.log_formatting.verbose_formatter.VerboseFormatter'
        },
        'verbose_console': {
            '()': 'utilities.log_formatting.verbose_formatter.VerboseConsoleFormatter'
        }
    },
    'handlers': {}
}


def configure_logging(caller_name: str = '',
                      debug_console: bool = False,
                      error_log_to_file: bool = True,
                      full_log_to_file: bool = False) -> None:
    logger_configuration = {caller_name: {'propagate': False, 'level': 'NOTSET', 'handlers':[]}}

    def _add_handler(handler_name: str, handler: Dict):
        logger_configuration[caller_name]['handlers'].append(handler_name)
        LOGGING_CONFIG['handlers'][handler_name] = handler
    
    if debug_console:
        _add_handler('debug_console', DEBUG_CONSOLE)
    else:
        _add_handler('info_console', INFO_CONSOLE)

    if error_log_to_file:
        _add_handler('error_file', ERROR_FILE_HANDLER)
    if full_log_to_file:
        _add_handler('log_to_file', ROTATING_FILE_HANDLER)

    LOGGING_CONFIG['loggers'] = logger_configuration
    dictConfig(LOGGING_CONFIG)