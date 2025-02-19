from flask import Blueprint 
import logging 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
# Initialize the blueprint for the hospital management system 
HOSPITAL_MANAGEMENT_BLUEPRINT = Blueprint('hospital_management', __name__) 
logger.info("Hospital management blueprint initialized.") 
# Import and register all the blueprints for different modules 
try: 
    from .admin import ADMIN_BLUEPRINT 
    from .doctor import DOCTORS_BLUEPRINT 
    from .patient import PATIENTS_BLUEPRINT 
    from .users import USERS_BLUEPRINT 
    # Register the blueprints with the main hospital management blueprint 
    HOSPITAL_MANAGEMENT_BLUEPRINT.register_blueprint(ADMIN_BLUEPRINT, url_prefix='/admin') 
    HOSPITAL_MANAGEMENT_BLUEPRINT.register_blueprint(DOCTORS_BLUEPRINT, url_prefix='/doctors') 
    HOSPITAL_MANAGEMENT_BLUEPRINT.register_blueprint(PATIENTS_BLUEPRINT, url_prefix='/patients') 
    HOSPITAL_MANAGEMENT_BLUEPRINT.register_blueprint(USERS_BLUEPRINT, url_prefix='/users') 
    logger.info("All blueprints registered successfully.") 
except Exception as e: 
    logger.error("Error importing or registering blueprints: %s", e, exc_info=True)