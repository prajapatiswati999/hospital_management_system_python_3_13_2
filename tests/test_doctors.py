import pytest 
from database.models.tables.doctors import Doctor 
import logging 
import traceback 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
def test_get_all_doctors(): 
    try: 
        logger.info("Testing retrieval of all doctors.") 
        doctors = Doctor.get_all_doctors() 
        assert isinstance(doctors, list), "Expected a list of doctors" 
        logger.info("Test for getting all doctors passed.") 
    except Exception as e: 
        logger.error("Error in test_get_all_doctors: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise 
def test_doctor_creation(): 
    try: 
        logger.info("Testing doctor creation.") 
        doctor = Doctor.create(idx="test_id", username="doctor_user", password="password", first_name="Doctor", last_name="Test", age=40, domain="GENERAL", user_type="DOCTOR") 
        assert doctor.user.username == "doctor_user", "Doctor username should match" 
        logger.info("Doctor creation test passed.") 
    except Exception as e: 
        logger.error("Error in test_doctor_creation: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise