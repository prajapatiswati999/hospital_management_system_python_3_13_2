import pytest 
from hospital_management_system_python_3_13_2.managers.users import create_user, get_user, delete_user 
from hospital_management_system_python_3_13_2.database.models.tables.users import User 
import logging 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
@pytest.fixture 
def user_data(): 
    return { 
        "username": "testuser", 
        "password": "testpassword", 
        "first_name": "Test", 
        "last_name": "User", 
        "age": 30, 
        "domain": "GENERAL", 
        "user_type": "PATIENT" 
    } 
def test_create_user(user_data): 
    logger.info("Testing user creation with data: %s", user_data) 
    try: 
        create_user(**user_data) 
        user = User.get_by_username(user_data['username']) 
        assert user is not None 
        assert user.username == user_data['username'] 
        logger.info("User creation test passed for username: %s", user_data['username']) 
    except Exception as e: 
        logger.error("User creation test failed: %s", e, exc_info=True) 
        raise 
def test_get_user(user_data): 
    logger.info("Testing user retrieval with username: %s", user_data['username']) 
    try: 
        user = get_user(user_data['username'], user_data['password']) 
        assert user is not None 
        assert user.username == user_data['username'] 
        logger.info("User retrieval test passed for username: %s", user_data['username']) 
    except Exception as e: 
        logger.error("User retrieval test failed: %s", e, exc_info=True) 
        raise 
def test_delete_user(user_data): 
    logger.info("Testing user deletion with username: %s", user_data['username']) 
    try: 
        user = User.get_by_username(user_data['username']) 
        delete_user(user.idx) 
        user = User.get_by_username(user_data['username']) 
        assert user is None 
        logger.info("User deletion test passed for username: %s", user_data['username']) 
    except Exception as e: 
        logger.error("User deletion test failed: %s", e, exc_info=True) 
        raise 