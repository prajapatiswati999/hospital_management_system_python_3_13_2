from flask import Blueprint, render_template, session, redirect, url_for, flash, request 
import logging 
import asyncio 
from database.models.tables.appointments import Appointment 
from database.models.tables.doctors import Doctor 
from managers.slot import get_slot_by_doctor_id, book_slot, get_doctor_name 
PATIENTS_BLUEPRINT = Blueprint('patients', __name__) 
USERS_LOGIN = 'users.login' 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
@PATIENTS_BLUEPRINT.route('', methods=['POST']) 
def index(): 
    logger.info("Patient index accessed.") 
    return redirect(url_for('patients.doctors')) 
@PATIENTS_BLUEPRINT.route('/doctors', methods=['GET']) 
async def doctors(): 
    logger.info("Fetching all doctors for patient view.") 
    try: 
        all_doctors = await asyncio.to_thread(Doctor.get_all_doctors) 
        context = { 
            'all_doctors': all_doctors 
        } 
        return render_template('patient_all_doctors.html', **context) 
    except Exception as e: 
        logger.error("Error fetching doctors: %s", e, exc_info=True) 
        flash('An error occurred while fetching doctors.') 
        return redirect(url_for('users.logout')) 
@PATIENTS_BLUEPRINT.route('/doctors/<idx>', methods=['GET']) 
async def view_doctor_slots(idx): 
    logger.info("Viewing slots for doctor with ID: %s", idx) 
    try: 
        slots = await get_slot_by_doctor_id(idx) 
        doc_name = get_doctor_name(idx) 
        context = { 
            'slots': slots, 
            'doctor_id': idx, 
            'doc_name': doc_name 
        } 
        return render_template('doctor_all_slots.html', **context) 
    except Exception as e: 
        logger.error("Error fetching slots for doctor: %s", e, exc_info=True) 
        flash('An error occurred while fetching slots.') 
        return redirect(url_for('patients.doctors')) 
@PATIENTS_BLUEPRINT.route('/doctors/<doctor_id>/<patient_id>/book/<slot_id>/<slot_number>', methods=['GET']) 
async def book(doctor_id, patient_id, slot_id, slot_number): 
    logger.info("Booking slot %s for doctor ID: %s by patient ID: %s", slot_number, doctor_id, patient_id) 
    try: 
        await book_slot(slot_id, doctor_id, patient_id, slot_number) 
        slots = await get_slot_by_doctor_id(doctor_id) 
        context = { 
            'slots': slots, 
            'doctor_id': doctor_id 
        } 
        return render_template('doctor_all_slots.html', **context) 
    except Exception as e: 
        logger.error("Error booking slot: %s", e, exc_info=True) 
        flash('An error occurred while booking the slot.') 
        return redirect(url_for('patients.view_doctor_slots', idx=doctor_id)) 
@PATIENTS_BLUEPRINT.route('/appointments', methods=['GET']) 
async def appointments(): 
    logger.info("Fetching appointments for patient.") 
    try: 
        all_appointments = await asyncio.to_thread(Appointment.get_by_patient_id, session.get('user_idx')) 
        context = { 
            'all_appointments': all_appointments 
        } 
        return render_template('doctor_all_appointments.html', **context) 
    except Exception as e: 
        logger.error("Error fetching appointments: %s", e, exc_info=True) 
        flash('An error occurred while fetching appointments.') 
        return redirect(url_for('users.logout')) 
@PATIENTS_BLUEPRINT.route('/appointments/<idx>', methods=['GET']) 
async def view_appointment(idx): 
    logger.info("Viewing appointment with ID: %s", idx) 
    try: 
        prescription_text = await asyncio.to_thread(Appointment.get, idx).prescription_text 
        context = { 
            'prescription_text': prescription_text, 
            'appointment_idx': idx 
        } 
        return render_template('view_prescription.html', **context) 
    except Exception as e: 
        logger.error("Error fetching appointment details: %s", e, exc_info=True) 
        flash('An error occurred while fetching appointment details.') 
        return redirect(url_for('patients.appointments'))