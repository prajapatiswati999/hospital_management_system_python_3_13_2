from hospital_management_system_python_3_13_2.database.db import db 
from hospital_management_system_python_3_13_2.database.models.enums.user_types import UserType 
import bcrypt 
import logging 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
class User(db.Model): 
    __tablename__ = 'users' 
    idx = db.Column(db.String, primary_key=True) 
    username = db.Column(db.String, unique=True) 
    first_name = db.Column(db.String) 
    last_name = db.Column(db.String) 
    age = db.Column(db.Integer, nullable=True) 
    _password_hash = db.Column(db.String) 
    user_type = db.Column(db.Enum(UserType)) 
    @property 
    def password(self): 
        raise AttributeError('Unreadable property password.') 
    @password.setter 
    def password(self, password): 
        if password: 
            self._password_hash = bcrypt.hashpw( 
                password.encode(), bcrypt.gensalt() 
            ).decode() 
            logger.info("Password hash set for user %s", self.username) 
    def check_password(self, password): 
        result = bcrypt.checkpw(password.encode(), self._password_hash.encode()) 
        logger.info("Password check for user %s: %s", self.username, result) 
        return result 
    @classmethod 
    def get(cls, pk): 
        logger.info("Fetching user with ID: %s", pk) 
        return cls.query.get(pk) 
    @classmethod 
    def get_by_uid(cls, idx: str): 
        logger.info("Fetching user by user ID: %s", idx) 
        user = cls.query.filter_by(idx=idx).first() 
        return user 
    @classmethod 
    def get_by_username(cls, username: str): 
        logger.info("Fetching user by username: %s", username) 
        user = cls.query.filter_by(username=username).first() 
        return user 
    @classmethod 
    def create(cls, **kwargs): 
        logger.info("Creating user with data: %s", kwargs) 
        instance = cls(**kwargs) 
        return instance.save() 
    def save(self, commit=True): 
        logger.info("Saving user with ID: %s", self.idx) 
        db.session.add(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("User saved successfully.") 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error saving user: %s", e, exc_info=True) 
                raise 
        return self 
    def delete(self, commit=True): 
        logger.info("Deleting user with ID: %s", self.idx) 
        db.session.delete(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("User deleted successfully.") 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error deleting user: %s", e, exc_info=True) 
                raise 
        return self 