from datetime import datetime 
from uuid import uuid4 
import logging 
from typing import List 
from hospital_management_system_python_3_13_2.database.models.tables.doctors import Doctor 
from hospital_management_system_python_3_13_2.database.models.tables.slots import Slot 
from hospital_management_system_python_3_13_2.managers.appointment import create_appointment 
from hospital_management_system_python_3_13_2.database.db import db 
import asyncio 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
DATE_FORMAT = '%Y-%m-%d' 
async def create_slot(doctor_id: str, date: str, slots: List[str]) -> None: 
    logger.info("Creating slot for doctor ID: %s on date: %s", doctor_id, date) 
    try: 
        with db.session.begin(): 
            Slot.create(idx=str(uuid4()), doctor_id=doctor_id, date=datetime.strptime(date, DATE_FORMAT), 
                        slot1=slots[0] or 'False', slot2=slots[1] or 'False', 
                        slot3=slots[2] or 'False', slot4=slots[3] or 'False') 
        logger.info("Slot created successfully for doctor ID: %s", doctor_id) 
    except Exception as e: 
        logger.error("Error creating slot for doctor ID: %s", doctor_id, exc_info=True) 
        raise 
async def get_slot_by_doctor_id(doctor_id: str) -> List[Slot]: 
    logger.info("Fetching slots for doctor ID: %s", doctor_id) 
    try: 
        slots = Slot.get_by_doctor_id(doctor_id) 
        logger.info("Successfully fetched slots for doctor ID: %s", doctor_id) 
        return slots 
    except Exception as e: 
        logger.error("Error fetching slots for doctor ID: %s", doctor_id, exc_info=True) 
        raise 
async def book_slot(slot_id: str, doctor_id: str, patient_id: str, slot_number: str) -> None: 
    logger.info("Booking slot %s for doctor ID: %s by patient ID: %s", slot_number, doctor_id, patient_id) 
    try: 
        with db.session.begin(): 
            slot = Slot.get(slot_id) 
            match slot_number: 
                case 'Slot1': 
                    slot.slot1 = patient_id 
                case 'Slot2': 
                    slot.slot2 = patient_id 
                case 'Slot3': 
                    slot.slot3 = patient_id 
                case 'Slot4': 
                    slot.slot4 = patient_id 
                case _: 
                    logger.warning("Invalid slot number: %s", slot_number) 
                    return 
            slot.save() 
            create_appointment(doctor_id=doctor_id, patient_id=patient_id, slot_number=slot_number, date=slot.date) 
        logger.info("Slot %s booked successfully for doctor ID: %s by patient ID: %s", slot_number, doctor_id, patient_id) 
    except Exception as e: 
        logger.error("Error booking slot %s for doctor ID: %s by patient ID: %s", slot_number, doctor_id, patient_id, exc_info=True) 
        raise 
def get_doctor_name(doc_idx: str) -> str: 
    logger.info("Fetching name for doctor ID: %s", doc_idx) 
    try: 
        doctor = Doctor.get(doc_idx) 
        doc_first_name, doc_last_name = doctor.user.first_name, doctor.user.last_name 
        doc_name = f'{doc_first_name} {doc_last_name}' 
        logger.info("Successfully fetched name for doctor ID: %s", doc_idx) 
        return doc_name 
    except Exception as e: 
        logger.error("Error fetching name for doctor ID: %s", doc_idx, exc_info=True) 
        raise