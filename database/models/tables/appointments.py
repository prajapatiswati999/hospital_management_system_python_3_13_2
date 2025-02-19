from dataclasses import dataclass, field 
from datetime import date 
from uuid import uuid4 
from  ...db import db
import logging 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
@dataclass 
class Appointment(db.Model): 
    __tablename__ = 'appointments' 
    idx: str = field(default_factory=lambda: str(uuid4()), init=False) 
    doctor_id: str 
    patient_id: str 
    slot_number: str 
    date: date 
    prescription_text: str = '' 
    doctor = db.relationship('User', backref=db.backref('appointment_doctor', cascade="delete, delete-orphan"), 
                             lazy=True, single_parent=True, foreign_keys='Appointment.doctor_id') 
    patient = db.relationship('User', backref=db.backref('appointment_patient', cascade="delete, delete-orphan"), 
                              lazy=True, single_parent=True, foreign_keys='Appointment.patient_id') 
    @classmethod 
    def get(cls, pk): 
        logger.info("Fetching appointment with ID: %s", pk) 
        return cls.query.get(pk) 
    @classmethod 
    def get_by_doctor_id(cls, idx: str): 
        logger.info("Fetching appointments for doctor ID: %s", idx) 
        appointment = cls.query.filter_by(doctor_id=idx).all() 
        return appointment 
    @classmethod 
    def get_by_patient_id(cls, idx: str): 
        logger.info("Fetching appointments for patient ID: %s", idx) 
        appointments = cls.query.filter_by(patient_id=idx).all() 
        return appointments 
    @classmethod 
    def create(cls, **kwargs): 
        logger.info("Creating new appointment with data: %s", kwargs) 
        instance = cls(**kwargs) 
        return instance.save() 
    def save(self, commit=True): 
        logger.info("Saving appointment with ID: %s", self.idx) 
        db.session.add(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Appointment saved successfully.") 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error saving appointment: %s", e, exc_info=True) 
                raise 
        return self 
    def delete(self, commit=True): 
        logger.info("Deleting appointment with ID: %s", self.idx) 
        db.session.delete(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Appointment deleted successfully.") 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error deleting appointment: %s", e, exc_info=True) 
                raise 
        return self