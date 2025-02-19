import logging 
from sqlalchemy.exc import SQLAlchemyError 
from database.db import db 
# Set up logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
def create_tables(): 
    """ 
    Create all database tables. 
    """ 
    try: 
        db.create_all() 
        logger.info("Database tables created successfully.") 
    except SQLAlchemyError as e: 
        logger.error(f"Error creating database tables: {e}", exc_info=True) 
        raise 
def drop_tables(): 
    """ 
    Drop all database tables. 
    """ 
    try: 
        db.drop_all() 
        logger.info("Database tables dropped successfully.") 
    except SQLAlchemyError as e: 
        logger.error(f"Error dropping database tables: {e}", exc_info=True) 
        raise 