import pytest 
from database.models.tables.appointments import Appointment 
from managers.appointment import create_appointment, update_prescription 
from datetime import date 
import logging 
import traceback 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
@pytest.fixture 
def appointment_data(): 
    return { 
        "doctor_id": "doctor_id", 
        "patient_id": "patient_id", 
        "slot_number": "Slot1", 
        "date": date.today() 
    } 
def test_create_appointment(appointment_data): 
    try: 
        logger.info("Testing appointment creation with data: %s", appointment_data) 
        create_appointment(**appointment_data) 
        appointments = Appointment.get_by_doctor_id(appointment_data["doctor_id"]) 
        assert len(appointments) > 0, "There should be at least one appointment for the doctor" 
        logger.info("Appointment creation test passed.") 
    except Exception as e: 
        logger.error("Error in test_create_appointment: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise 
def test_update_prescription(): 
    try: 
        logger.info("Testing prescription update.") 
        appointment = Appointment.create(doctor_id="doctor_id", patient_id="patient_id", slot_number="Slot1", date=date.today()) 
        update_prescription(appointment.idx, "New prescription") 
        assert appointment.prescription_text == "New prescription", "Prescription text should be updated" 
        logger.info("Prescription update test passed.") 
    except Exception as e: 
        logger.error("Error in test_update_prescription: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise