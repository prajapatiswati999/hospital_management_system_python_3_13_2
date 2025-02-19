from enum import Enum 
import logging 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
class UserType(Enum): 
    ADMIN = 'ADMIN' 
    DOCTOR = 'DOCTOR' 
    PATIENT = 'PATIENT' 
    def __str__(self): 
        return self.value 
# Log the available user types 
logger.info("Available user types: %s", [user_type.value for user_type in UserType]) 