from flask import Blueprint, request, render_template, session, redirect, url_for, flash 
import logging 
import asyncio 
from database.models.tables.appointments import Appointment 
from managers.appointment import update_prescription 
DOCTORS_BLUEPRINT = Blueprint('doctors', __name__) 
USERS_LOGIN = 'users.login' 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
@DOCTORS_BLUEPRINT.route('', methods=['POST']) 
def index(): 
    logger.info("Doctor index accessed.") 
    return redirect(url_for('doctors.appointments')) 
@DOCTORS_BLUEPRINT.route('/appointments', methods=['GET']) 
async def appointments(): 
    logger.info("Fetching appointments for doctor.") 
    if session.get('user_type') == 'DOCTOR': 
        try: 
            all_appointments = await asyncio.to_thread(Appointment.get_by_doctor_id, session.get('user_idx')) 
            context = { 
                'all_appointments': all_appointments 
            } 
            return render_template('doctor_all_appointments.html', **context) 
        except Exception as e: 
            logger.error("Error fetching appointments: %s", e, exc_info=True) 
            flash('An error occurred while fetching appointments.') 
            return redirect(url_for('users.logout')) 
    else: 
        logger.warning("Unauthorized access attempt to doctor appointments view.") 
        return redirect(url_for('users.logout')) 
@DOCTORS_BLUEPRINT.route('/appointments/<idx>', methods=['POST']) 
async def prescription(idx): 
    logger.info("Updating prescription for appointment ID: %s", idx) 
    if session.get('user_type') == 'DOCTOR': 
        prescription_text = request.form.get('prescription') 
        try: 
            await asyncio.to_thread(update_prescription, idx, prescription_text) 
            logger.info("Prescription updated successfully for appointment ID: %s", idx) 
            return redirect(url_for('doctors.appointments')) 
        except Exception as e: 
            logger.error("Error updating prescription: %s", e, exc_info=True) 
            flash('An error occurred while updating the prescription.') 
            return redirect(url_for('doctors.appointments')) 
    else: 
        logger.warning("Unauthorized access attempt to update prescription.") 
        return redirect(url_for('users.logout'))