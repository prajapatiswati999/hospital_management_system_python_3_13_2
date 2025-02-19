from hospital_management_system_python_3_13_2.database.db import db 
import logging 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
class Slot(db.Model): 
    __tablename__ = 'slots' 
    idx = db.Column(db.String, primary_key=True) 
    doctor_id = db.Column(db.String) 
    slot1 = db.Column(db.String) 
    slot2 = db.Column(db.String) 
    slot3 = db.Column(db.String) 
    slot4 = db.Column(db.String) 
    date = db.Column(db.Date) 
    @classmethod 
    def get(cls, pk): 
        logger.info("Fetching slot with ID: %s", pk) 
        return cls.query.get(pk) 
    @classmethod 
    def get_all(cls): 
        logger.info("Fetching all slots") 
        return cls.query.all() 
    @classmethod 
    def get_by_doctor_id(cls, idx: str): 
        logger.info("Fetching slots for doctor ID: %s", idx) 
        slot = cls.query.filter_by(doctor_id=idx).all() 
        return slot 
    @classmethod 
    def get_by_patient_id(cls, idx: str): 
        logger.info("Fetching slots for patient ID: %s", idx) 
        user = cls.query.filter_by(idx=idx) 
        return user 
    @classmethod 
    def create(cls, **kwargs): 
        logger.info("Creating slot with data: %s", kwargs) 
        instance = cls(**kwargs) 
        return instance.save() 
    def save(self, commit=True): 
        logger.info("Saving slot with ID: %s", self.idx) 
        db.session.add(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Slot saved successfully.") 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error saving slot: %s", e, exc_info=True) 
                raise 
        return self 
    def delete(self, commit=True): 
        logger.info("Deleting slot with ID: %s", self.idx) 
        db.session.delete(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Slot deleted successfully.") 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error deleting slot: %s", e, exc_info=True) 
                raise 
        return self 