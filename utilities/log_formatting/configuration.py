from logging.config import dictConfig

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(message)s',
        },
        'verbose': {
            '()': 'utilities.log_formatting.verbose_formatter.VerboseConsoleFormatter'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'debug_console': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'rotating_file_handler': {
            'level': 'INFO',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'info.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 100,
        },
        'file_handler': {
            'level': 'WARNING',
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': 'error.log',
            'mode': 'a',
        }

    },
}

def configure_logging(caller_name: str = '',
                      debug_console: bool = False,
                      log_to_file: bool = False) -> None:
    logger_configuration = {caller_name: {'propagate': False, 'level': 'INFO'}}
    
    if debug_console:
        logger_configuration[caller_name]['handlers'] = ['debug_console']
    else:
        logger_configuration[caller_name]['handlers'] = ['console']
    if log_to_file:
        logger_configuration[caller_name]['handlers'].extend(['rotating_file_handler', 'file_handler'])
    LOGGING_CONFIG['loggers'] = logger_configuration
    dictConfig(LOGGING_CONFIG)