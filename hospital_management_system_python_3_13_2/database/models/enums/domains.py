from enum import Enum 
import logging 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
class Domain(Enum): 
    CARDIO = 'CARDIO' 
    GENERAL = 'GENERAL' 
    EYE = 'EYE' 
    def __str__(self): 
        return self.value 
# Log the available domains 
logger.info("Available domains: %s", [domain.value for domain in Domain]) 