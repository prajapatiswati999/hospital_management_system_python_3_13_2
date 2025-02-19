import logging 
from ..database.models.tables.appointments import Appointment
from ..database.models.tables.doctors import Doctor
from slot import get_slot_by_doctor_id, book_slot, get_doctor_name 
import asyncio 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
async def get_all_doctors(): 
    """ 
    Retrieve all doctors from the database asynchronously. 
    """ 
    logger.info("Fetching all doctors.") 
    await asyncio.sleep(0)  # Simulate I/O-bound operation 
    try: 
        doctors = Doctor.get_all_doctors() 
        logger.info("Successfully fetched all doctors.") 
        return doctors 
    except Exception as e: 
        logger.error("Error fetching all doctors: %s", e, exc_info=True) 
        raise 
async def view_doctor_slots(doctor_id): 
    """ 
    View available slots for a specific doctor asynchronously. 
    """ 
    logger.info("Viewing slots for doctor with ID: %s", doctor_id) 
    await asyncio.sleep(0)  # Simulate I/O-bound operation 
    try: 
        slots = get_slot_by_doctor_id(doctor_id) 
        doc_name = get_doctor_name(doctor_id) 
        logger.info("Successfully fetched slots for doctor with ID: %s", doctor_id) 
        return slots, doc_name 
    except Exception as e: 
        logger.error("Error fetching slots for doctor with ID: %s", doctor_id, exc_info=True) 
        raise 
async def book_appointment(doctor_id, patient_id, slot_id, slot_number): 
    """ 
    Book an appointment for a patient with a specific doctor asynchronously. 
    """ 
    logger.info("Booking appointment for patient ID: %s with doctor ID: %s for slot number: %s", patient_id, doctor_id, slot_number) 
    await asyncio.sleep(0)  # Simulate I/O-bound operation 
    try: 
        book_slot(slot_id, doctor_id, patient_id, slot_number) 
        logger.info("Successfully booked appointment for patient ID: %s with doctor ID: %s", patient_id, doctor_id) 
    except Exception as e: 
        logger.error("Error booking appointment for patient ID: %s with doctor ID: %s", patient_id, doctor_id, exc_info=True) 
        raise 
async def get_appointments_by_patient(patient_id): 
    """ 
    Retrieve all appointments for a specific patient asynchronously. 
    """ 
    logger.info("Fetching appointments for patient ID: %s", patient_id) 
    await asyncio.sleep(0)  # Simulate I/O-bound operation 
    try: 
        appointments = Appointment.get_by_patient_id(patient_id) 
        logger.info("Successfully fetched appointments for patient ID: %s", patient_id) 
        return appointments 
    except Exception as e: 
        logger.error("Error fetching appointments for patient ID: %s", patient_id, exc_info=True) 
        raise