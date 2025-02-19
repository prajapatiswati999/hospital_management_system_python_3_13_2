import logging 
from uuid import uuid4 
from functools import wraps 
from database.models.tables.appointments import Appointment 
from database.db import db 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
def log_function_call(func): 
    @wraps(func) 
    def wrapper(*args, **kwargs): 
        logger.info("Calling function: %s", func.__name__) 
        result = func(*args, **kwargs) 
        logger.info("Function %s completed", func.__name__) 
        return result 
    return wrapper 
@log_function_call 
def create_appointment(doctor_id, patient_id, slot_number, date): 
    logger.info("Creating appointment for doctor ID: %s, patient ID: %s, slot number: %s, date: %s", doctor_id, patient_id, slot_number, date) 
    try: 
        with db.session.begin(): 
            Appointment.create(idx=str(uuid4()), doctor_id=doctor_id, patient_id=patient_id, 
                               slot_number=slot_number, date=date) 
        logger.info("Appointment created successfully.") 
    except Exception as e: 
        logger.error("Error creating appointment: %s", e, exc_info=True) 
        raise 
@log_function_call 
def update_prescription(appointment_idx, prescription_text): 
    logger.info("Updating prescription for appointment ID: %s", appointment_idx) 
    try: 
        with db.session.begin(): 
            appointment = Appointment.get(appointment_idx) 
            appointment.prescription_text = prescription_text 
            appointment.save() 
        logger.info("Prescription updated successfully for appointment ID: %s", appointment_idx) 
    except Exception as e: 
        logger.error("Error updating prescription: %s", e, exc_info=True) 
        raise