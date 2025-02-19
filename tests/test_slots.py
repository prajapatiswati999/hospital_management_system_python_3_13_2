import pytest 
import asyncio 
from hospital_management_system_python_3_13_2.managers.slot import create_slot, get_slot_by_doctor_id, book_slot 
from hospital_management_system_python_3_13_2.database.models.tables.slots import Slot 
import logging 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
@pytest.fixture 
def slot_data(): 
    return { 
        "doctor_id": "doctor123", 
        "date": "2023-10-10", 
        "slots": ["True", "False", "False", "False"] 
    } 
@pytest.mark.asyncio 
async def test_create_slot(slot_data): 
    logger.info("Testing slot creation with data: %s", slot_data) 
    try: 
        await create_slot(**slot_data) 
        slots = await get_slot_by_doctor_id(slot_data['doctor_id']) 
        assert len(slots) > 0 
        assert slots[0].doctor_id == slot_data['doctor_id'] 
        logger.info("Slot creation test passed for doctor ID: %s", slot_data['doctor_id']) 
    except Exception as e: 
        logger.error("Slot creation test failed: %s", e, exc_info=True) 
        raise 
@pytest.mark.asyncio 
async def test_book_slot(slot_data): 
    logger.info("Testing slot booking for doctor ID: %s", slot_data['doctor_id']) 
    try: 
        slots = await get_slot_by_doctor_id(slot_data['doctor_id']) 
        slot_id = slots[0].idx 
        await book_slot(slot_id, slot_data['doctor_id'], "patient123", "Slot1") 
        slot = Slot.get(slot_id) 
        assert slot.slot1 == "patient123" 
        logger.info("Slot booking test passed for slot ID: %s", slot_id) 
    except Exception as e: 
        logger.error("Slot booking test failed: %s", e, exc_info=True) 
        raise