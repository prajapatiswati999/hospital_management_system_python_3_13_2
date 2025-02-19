import asyncio 
from datetime import datetime 
from uuid import uuid4 
from typing import List 
from contextlib import asynccontextmanager 
from functools import lru_cache 
from concurrent.futures import ThreadPoolExecutor 
from database.models.tables.doctors import Doctor 
from database.models.tables.slots import Slot 
from managers.appointment import create_appointment 
import logging 
import traceback 
from sqlalchemy.exc import SQLAlchemyError 
from database.db import db 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
DATE_FORMAT = '%Y-%m-%d' 
@asynccontextmanager 
async def async_session_scope(): 
    """Provide a transactional scope around a series of operations asynchronously.""" 
    session = db.session 
    try: 
        yield session 
        await asyncio.to_thread(session.commit) 
    except SQLAlchemyError as e: 
        await asyncio.to_thread(session.rollback) 
        logger.error("Session rollback due to error: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise 
    finally: 
        await asyncio.to_thread(session.close) 
@lru_cache(maxsize=128) 
async def get_slot_by_doctor_id(doctor_id: str) -> List[Slot]: 
    try: 
        logger.info("Retrieving slots for doctor_id: %s", doctor_id) 
        slots = await asyncio.to_thread(Slot.get_by_doctor_id, doctor_id) 
        logger.info("Slots retrieved successfully.") 
        return slots 
    except Exception as e: 
        logger.error("Error retrieving slots: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise 
async def create_slot(doctor_id: str, date: str, slots: List[str]) -> None: 
    try: 
        logger.info("Creating slot for doctor_id: %s on date: %s with slots: %s", doctor_id, date, slots) 
        async with async_session_scope() as session: 
            with ThreadPoolExecutor() as executor: 
                await asyncio.to_thread(executor.submit, Slot.create, idx=str(uuid4()), doctor_id=doctor_id, date=datetime.strptime(date, DATE_FORMAT), 
                                        slot1=slots[0] or 'False', slot2=slots[1] or 'False', 
                                        slot3=slots[2] or 'False', slot4=slots[3] or 'False') 
        logger.info("Slot created successfully.") 
    except Exception as e: 
        logger.error("Error creating slot: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise 
async def book_slot(slot_id: str, doctor_id: str, patient_id: str, slot_number: str) -> None: 
    try: 
        logger.info("Booking slot_id: %s for doctor_id: %s, patient_id: %s, slot_number: %s", slot_id, doctor_id, patient_id, slot_number) 
        slot = await asyncio.to_thread(Slot.get, slot_id) 
        match slot_number: 
            case 'Slot1': 
                slot.slot1 = patient_id 
            case 'Slot2': 
                slot.slot2 = patient_id 
            case 'Slot3': 
                slot.slot3 = patient_id 
            case 'Slot4': 
                slot.slot4 = patient_id 
        await asyncio.to_thread(slot.save) 
        await create_appointment(doctor_id=doctor_id, patient_id=patient_id, slot_number=slot_number, date=slot.date) 
        logger.info("Slot booked and appointment created successfully.") 
    except Exception as e: 
        logger.error("Error booking slot: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise 
async def get_doctor_name(doc_idx: str) -> str: 
    try: 
        logger.info("Retrieving doctor name for doc_idx: %s", doc_idx) 
        doctor = await asyncio.to_thread(Doctor.get, doc_idx) 
        doc_first_name, doc_last_name = doctor.user.first_name, doctor.user.last_name 
        doc_name = f'{doc_first_name} {doc_last_name}' 
        logger.info("Doctor name retrieved successfully: %s", doc_name) 
        return doc_name 
    except Exception as e: 
        logger.error("Error retrieving doctor name: %s", e) 
        logger.debug(traceback.format_exc()) 
        raise