import logging 
from flask_sqlalchemy import SQLAlchemy 
# Initialize the SQLAlchemy database instance 
db = SQLAlchemy() 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
def init_db(app): 
    """ 
    Initialize the database with the Flask app context. 
    """ 
    try: 
        db.init_app(app) 
        logger.info("Database initialized successfully.") 
    except Exception as e: 
        logger.error("Error initializing database: %s", e, exc_info=True) 
def create_all_tables(): 
    """ 
    Create all database tables. 
    """ 
    try: 
        db.create_all() 
        logger.info("All database tables created successfully.") 
    except Exception as e: 
        logger.error("Error creating database tables: %s", e, exc_info=True) 