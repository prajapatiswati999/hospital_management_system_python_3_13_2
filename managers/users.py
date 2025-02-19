from database.models.tables.users import User 
from database.models.tables.doctors import Doctor 
from database.models.enums.user_types import UserType 
from database.models.enums.domains import Domain 
from uuid import uuid4 
from typing import Optional 
import logging 
import traceback 
from functools import lru_cache 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
def create_user(username: str, password: str, first_name: str, last_name: str, age: int, domain: str, user_type: str) -> None: 
    try: 
        logger.info("Creating user with username: %s, first_name: %s, last_name: %s, age: %d, domain: %s, user_type: %s", username, first_name, last_name, age, domain, user_type) 
        idx = str(uuid4()) 
        if user_type == 'DOCTOR': 
            Doctor.create(idx=idx, username=username, password=password, first_name=first_name, 
                          last_name=last_name, domain=Domain(domain), 
                          age=age, user_type=UserType(user_type)) 
        else: 
            User.create(idx=idx, username=username, password=password, first_name=first_name, last_name=last_name, 
                        age=age, user_type=UserType(user_type)) 
        logger.info("User created successfully.") 
    except Exception as e: 
        logger.error("Error creating user: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise 
@lru_cache(maxsize=128) 
def get_user(username: str, password: str) -> Optional[User]: 
    try: 
        logger.info("Retrieving user with username: %s", username) 
        user = User.get_by_username(username) 
        if user and user.check_password(password): 
            logger.info("User retrieved successfully.") 
            return user 
        logger.warning("User not found or password mismatch.") 
        return None 
    except Exception as e: 
        logger.error("Error retrieving user: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise 
def delete_user(idx: str) -> None: 
    try: 
        logger.info("Deleting user with idx: %s", idx) 
        user = User.get(idx) 
        user.delete() 
        logger.info("User deleted successfully.") 
    except Exception as e: 
        logger.error("Error deleting user: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise