import logging 
import os 
# Define the logging configuration 
LOGGING_CONFIG = { 
    'version': 1, 
    'disable_existing_loggers': False, 
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s' 
        }, 
    }, 
    'handlers': { 
        'console': { 
            'level': 'DEBUG', 
            'class': 'logging.StreamHandler', 
            'formatter': 'standard' 
        }, 
        'file': { 
            'level': 'INFO', 
            'class': 'logging.FileHandler', 
            'filename': os.path.join('logs', 'app.log'), 
            'formatter': 'standard', 
            'mode': 'a', 
        }, 
    }, 
    'loggers': { 
        '': {  # root logger 
            'handlers': ['console', 'file'], 
            'level': 'DEBUG', 
            'propagate': False 
        }, 
        'app': {  # app logger 
            'handlers': ['console', 'file'], 
            'level': 'DEBUG', 
            'propagate': False 
        }, 
    } 
} 
# Apply the logging configuration 
logging.config.dictConfig(LOGGING_CONFIG) 
logger = logging.getLogger('app') 
logger.info("Logging is configured.") 