import functools 
import logging 
# Configure logging 
logging.basicConfig( 
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    handlers=[ 
        logging.FileHandler("app.log"), 
        logging.StreamHandler() 
    ] 
) 
logger = logging.getLogger(__name__) 
def log_execution(func): 
    """Decorator to log the execution of a function.""" 
    @functools.wraps(func) 
    def wrapper(*args, **kwargs): 
        logger.info("Executing %s with args: %s, kwargs: %s", func.__name__, args, kwargs) 
        try: 
            result = func(*args, **kwargs) 
            logger.info("Finished executing %s", func.__name__) 
            return result 
        except Exception as e: 
            logger.error("Error in %s: %s", func.__name__, e) 
            logger.debug("Exception occurred", exc_info=True) 
            raise 
    return wrapper