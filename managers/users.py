from ..database.models.tables.users import User 
from ..database.models.tables.doctors import Doctor 
from ..database.models.enums.user_types import UserType 
from ..database.models.enums.domains import Domain 
from uuid import uuid4 
import logging 
from typing import Optional 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
def create_user(username: str, password: str, first_name: str, last_name: str, age: int, domain: str, user_type: str) -> None: 
    idx = str(uuid4()) 
    logger.info("Creating user with username: %s", username) 
    try: 
        match user_type: 
            case 'DOCTOR': 
                Doctor.create(idx=idx, username=username, password=password, first_name=first_name, 
                              last_name=last_name, domain=Domain(domain), 
                              age=age, user_type=UserType(user_type)) 
                logger.info("Doctor user created successfully with username: %s", username) 
            case _: 
                User.create(idx=idx, username=username, password=password, first_name=first_name, last_name=last_name, 
                            age=age, user_type=UserType(user_type)) 
                logger.info("User created successfully with username: %s", username) 
    except Exception as e: 
        logger.error("Error creating user with username: %s, error: %s", username, e, exc_info=True) 
        raise 
def get_user(username: str, password: str) -> Optional[User]: 
    logger.info("Fetching user with username: %s", username) 
    try: 
        user = User.get_by_username(username) 
        if user and user.check_password(password): 
            logger.info("User authenticated successfully with username: %s", username) 
            return user 
        else: 
            logger.warning("Authentication failed for user with username: %s", username) 
    except Exception as e: 
        logger.error("Error fetching user with username: %s, error: %s", username, e, exc_info=True) 
        raise 
def delete_user(idx: str) -> None: 
    logger.info("Deleting user with ID: %s", idx) 
    try: 
        user = User.get(idx) 
        if user: 
            user.delete() 
            logger.info("User deleted successfully with ID: %s", idx) 
        else: 
            logger.warning("User not found with ID: %s", idx) 
    except Exception as e: 
        logger.error("Error deleting user with ID: %s, error: %s", idx, e, exc_info=True) 
        raise