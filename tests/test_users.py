import pytest 
from database.models.tables.users import User 
from managers.users import create_user, get_user, delete_user 
import logging 
import traceback 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
@pytest.fixture 
def user_data(): 
    return { 
        "username": "test_user", 
        "password": "password123", 
        "first_name": "Test", 
        "last_name": "User", 
        "age": 30, 
        "domain": "GENERAL", 
        "user_type": "PATIENT" 
    } 
def test_create_user(user_data): 
    try: 
        logger.info("Testing user creation with data: %s", user_data) 
        create_user(**user_data) 
        user = get_user(user_data["username"], user_data["password"]) 
        assert user is not None, "User should be created and retrievable" 
        assert user.username == user_data["username"], "Usernames should match" 
        logger.info("User creation test passed.") 
    except Exception as e: 
        logger.error("Error in test_create_user: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise 
def test_delete_user(user_data): 
    try: 
        logger.info("Testing user deletion for user: %s", user_data["username"]) 
        user = get_user(user_data["username"], user_data["password"]) 
        if user is None: 
            logger.info("User not found, creating user for deletion test.") 
            create_user(**user_data) 
            user = get_user(user_data["username"], user_data["password"]) 
        delete_user(user.idx) 
        assert get_user(user_data["username"], user_data["password"]) is None, "User should be deleted" 
        logger.info("User deletion test passed.") 
    except Exception as e: 
        logger.error("Error in test_delete_user: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise