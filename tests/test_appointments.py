import pytest 
from hospital_management_system_python_3_13_2.managers.appointment import create_appointment, update_prescription 
from hospital_management_system_python_3_13_2.database.models.tables.appointments import Appointment 
import logging 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
@pytest.fixture 
def appointment_data(): 
    return { 
        "doctor_id": "doctor123", 
        "patient_id": "patient123", 
        "slot_number": "Slot1", 
        "date": "2023-10-10" 
    } 
def test_create_appointment(appointment_data): 
    logger.info("Testing appointment creation with data: %s", appointment_data) 
    try: 
        create_appointment(**appointment_data) 
        appointment = Appointment.get_by_doctor_id(appointment_data['doctor_id']) 
        assert appointment is not None 
        assert appointment[0].doctor_id == appointment_data['doctor_id'] 
        logger.info("Appointment creation test passed for doctor ID: %s", appointment_data['doctor_id']) 
    except Exception as e: 
        logger.error("Appointment creation test failed: %s", e, exc_info=True) 
        raise 
def test_update_prescription(appointment_data): 
    logger.info("Testing prescription update for doctor ID: %s", appointment_data['doctor_id']) 
    try: 
        appointment = Appointment.get_by_doctor_id(appointment_data['doctor_id'])[0] 
        update_prescription(appointment.idx, "New Prescription") 
        assert appointment.prescription_text == "New Prescription" 
        logger.info("Prescription update test passed for appointment ID: %s", appointment.idx) 
    except Exception as e: 
        logger.error("Prescription update test failed: %s", e, exc_info=True) 
        raise 