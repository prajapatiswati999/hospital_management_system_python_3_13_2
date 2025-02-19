from hospital_management_system_python_3_13_2.database.db import db 
from ..enums.domains import Domain 
from ..enums.user_types import UserType 
from ..tables.users import User 
import logging 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
class Doctor(db.Model): 
    __tablename__ = 'doctors' 
    idx = db.Column(db.String, db.ForeignKey('users.idx'), primary_key=True) 
    domain = db.Column(db.Enum(Domain)) 
    user = db.relationship('User', backref=db.backref('doctor', cascade="delete, delete-orphan"), lazy=True, 
                           single_parent=True) 
    @classmethod 
    def get(cls, pk): 
        logger.info("Fetching doctor with ID: %s", pk) 
        return cls.query.get(pk) 
    @classmethod 
    def get_by_uid(cls, idx: str): 
        logger.info("Fetching doctor by user ID: %s", idx) 
        user = cls.query.filter_by(idx=idx).first() 
        return user 
    @classmethod 
    def get_by_username(cls, username: str): 
        logger.info("Fetching doctor by username: %s", username) 
        user = cls.query.filter_by(username=username).first() 
        return user 
    @classmethod 
    def get_all_doctors(cls): 
        logger.info("Fetching all doctors") 
        doctors = cls.query.all() 
        return doctors 
    @classmethod 
    def create(cls, **kwargs): 
        logger.info("Creating doctor with data: %s", kwargs) 
        user = User(idx=kwargs.get('idx'), username=kwargs.get('username'), password=kwargs.get('password'), 
                    first_name=kwargs.get('first_name'), last_name=kwargs.get('last_name'), 
                    age=kwargs.get('age'), user_type=UserType(kwargs.get('user_type'))) 
        instance = cls(idx=kwargs.get('idx'), domain=Domain(kwargs.get('domain')), user=user) 
        return instance.save() 
    def save(self, commit=True): 
        logger.info("Saving doctor with ID: %s", self.idx) 
        db.session.add(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Doctor saved successfully.") 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error saving doctor: %s", e, exc_info=True) 
                raise 
        return self 
    def delete(self, commit=True): 
        logger.info("Deleting doctor with ID: %s", self.idx) 
        db.session.delete(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Doctor deleted successfully.") 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error deleting doctor: %s", e, exc_info=True) 
                raise 
        return self 