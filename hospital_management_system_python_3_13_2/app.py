from flask import Flask, redirect, url_for 
from database.db import db 
from blueprints.users import USERS_BLUEPRINT 
from blueprints.doctor import DOCTORS_BLUEPRINT 
from blueprints.admin import ADMIN_BLUEPRINT 
from blueprints.patient import PATIENTS_BLUEPRINT 
app = Flask(__name__) 
app.config.from_pyfile('config/settings.staging.cfg') 
db.init_app(app) 
app.register_blueprint(USERS_BLUEPRINT, url_prefix='/users') 
app.register_blueprint(DOCTORS_BLUEPRINT, url_prefix='/doctors') 
app.register_blueprint(ADMIN_BLUEPRINT, url_prefix='/admin') 
app.register_blueprint(PATIENTS_BLUEPRINT, url_prefix='/patients') 
@app.before_first_request 
def create_tables(): 
    try: 
        db.create_all() 
        app.logger.info("Database tables created successfully.") 
    except Exception as e: 
        app.logger.error("Error creating database tables: %s", e, exc_info=True) 
@app.route('/') 
def index(): 
    return redirect(url_for('users.register_user')) 
if __name__ == '__main__': 
    try: 
        app.run(debug=True) 
        app.logger.info("Flask application started successfully.") 
    except Exception as e: 
        app.logger.error("Error starting Flask application: %s", e, exc_info=True)