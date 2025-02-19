import asyncio 
from uuid import uuid4 
from database.models.tables.appointments import Appointment 
from datetime import date 
import logging 
import traceback 
from functools import lru_cache 
from concurrent.futures import ThreadPoolExecutor 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
@lru_cache(maxsize=128) 
async def get_appointment_by_doctor_id(doctor_id: str) -> list: 
    try: 
        logger.info("Retrieving appointments for doctor_id: %s", doctor_id) 
        appointments = await asyncio.to_thread(Appointment.get_by_doctor_id, doctor_id) 
        logger.info("Appointments retrieved successfully.") 
        return appointments 
    except Exception as e: 
        logger.error("Error retrieving appointments: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise 
async def create_appointment(doctor_id: str, patient_id: str, slot_number: str, date: date) -> None: 
    try: 
        logger.info("Creating appointment for doctor_id: %s, patient_id: %s, slot_number: %s, date: %s", doctor_id, patient_id, slot_number, date) 
        await asyncio.to_thread(Appointment.create, idx=str(uuid4()), doctor_id=doctor_id, patient_id=patient_id, 
                                slot_number=slot_number, date=date) 
        logger.info("Appointment created successfully.") 
    except Exception as e: 
        logger.error("Error creating appointment: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise 
async def update_prescription(appointment_idx: str, prescription_text: str) -> None: 
    try: 
        logger.info("Updating prescription for appointment_idx: %s", appointment_idx) 
        appointment = await asyncio.to_thread(Appointment.get, appointment_idx) 
        appointment.prescription_text = prescription_text 
        await asyncio.to_thread(appointment.save) 
        logger.info("Prescription updated successfully.") 
    except Exception as e: 
        logger.error("Error updating prescription: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise 
async def create_appointments_concurrently(appointments_data: list) -> None: 
    try: 
        logger.info("Creating appointments concurrently.") 
        with ThreadPoolExecutor() as executor: 
            await asyncio.gather(*[ 
                asyncio.to_thread(executor.submit, create_appointment, data['doctor_id'], data['patient_id'], data['slot_number'], data['date']) 
                for data in appointments_data 
            ]) 
        logger.info("All appointments created successfully.") 
    except Exception as e: 
        logger.error("Error creating appointments concurrently: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise