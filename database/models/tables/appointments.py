from dataclasses import dataclass, field 
from datetime import date 
from typing import Optional 
from uuid import uuid4 
from database.db import db 
import logging 
import traceback 
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
        try: 
            logger.info("Retrieving appointment with idx: %s", pk) 
            appointment = cls.query.get(pk) 
            if appointment: 
                logger.info("Appointment retrieved successfully.") 
            else: 
                logger.warning("Appointment not found.") 
            return appointment 
        except Exception as e: 
            logger.error("Error retrieving appointment: %s", e) 
            logger.debug(traceback.format_exc()) 
            raise 
    @classmethod 
    def get_by_doctor_id(cls, idx: str): 
        try: 
            logger.info("Retrieving appointments for doctor_id: %s", idx) 
            appointments = cls.query.filter_by(doctor_id=idx).all() 
            logger.info("Appointments retrieved successfully.") 
            return appointments 
        except Exception as e: 
            logger.error("Error retrieving appointments: %s", e) 
            logger.debug(traceback.format_exc()) 
            raise 
    @classmethod 
    def get_by_patient_id(cls, idx: str): 
        try: 
            logger.info("Retrieving appointments for patient_id: %s", idx) 
            appointments = cls.query.filter_by(patient_id=idx).all() 
            logger.info("Appointments retrieved successfully.") 
            return appointments 
        except Exception as e: 
            logger.error("Error retrieving appointments: %s", e) 
            logger.debug(traceback.format_exc()) 
            raise 
    @classmethod 
    def create(cls, **kwargs): 
        try: 
            logger.info("Creating appointment with data: %s", kwargs) 
            instance = cls(**kwargs) 
            return instance.save() 
        except Exception as e: 
            logger.error("Error creating appointment: %s", e) 
            logger.debug(traceback.format_exc()) 
            raise 
    def save(self, commit=True): 
        db.session.add(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Appointment saved successfully.") 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error saving appointment: %s", e) 
                logger.debug(traceback.format_exc()) 
                raise 
        return self 
    def delete(self, commit=True): 
        try: 
            logger.info("Deleting appointment with idx: %s", self.idx) 
            db.session.delete(self) 
            if commit: 
                db.session.commit() 
                logger.info("Appointment deleted successfully.") 
            return True 
        except Exception as e: 
            db.session.rollback() 
            logger.error("Error deleting appointment: %s", e) 
            logger.debug(traceback.format_exc()) 
            raise