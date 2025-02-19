from flask import Blueprint, request, render_template, redirect, url_for, flash, session 
import logging 
from database.models.tables.doctors import Doctor 
from managers.slot import get_slot_by_doctor_id, create_slot, get_doctor_name 
from managers.users import create_user, delete_user 
ADMIN_BLUEPRINT = Blueprint('admin', __name__) 
USERS_LOGIN = 'users.login' 
logger = logging.getLogger(__name__) 
@ADMIN_BLUEPRINT.route('', methods=['POST']) 
def index(): 
    logger.info("Admin index accessed.") 
    return redirect(url_for('admin.doctors')) 
@ADMIN_BLUEPRINT.route('/doctors', methods=['GET']) 
def doctors(): 
    logger.info("Fetching all doctors for admin view.") 
    if session.get('user_type') == 'ADMIN': 
        try: 
            all_doctors = Doctor.get_all_doctors() 
            context = { 
                'all_doctors': all_doctors 
            } 
            return render_template('admin_all_doctors.html', **context) 
        except Exception as e: 
            logger.error("Error fetching doctors: %s", e, exc_info=True) 
            flash('An error occurred while fetching doctors.') 
            return redirect(url_for('users.logout')) 
    else: 
        logger.warning("Unauthorized access attempt to admin doctors view.") 
        return redirect(url_for('users.logout')) 
@ADMIN_BLUEPRINT.route('/doctors/add', methods=['GET', 'POST']) 
def add_doctor(): 
    logger.info("Accessing add doctor page.") 
    if session.get('user_type') == 'ADMIN': 
        if request.method == 'GET': 
            return render_template('admin_add_doctor.html') 
        else: 
            username = request.form.get('username') 
            password = request.form.get('psw') 
            password_repeat = request.form.get('psw-repeat') 
            user_type = 'DOCTOR' 
            first_name = request.form.get('first-name') 
            last_name = request.form.get('last-name') 
            age = request.form.get('age') 
            domain = request.form.get('domain') or 'GENERAL' 
            if password == password_repeat: 
                try: 
                    create_user(username=username, password=password, first_name=first_name, last_name=last_name, 
                                age=age, domain=domain, user_type=user_type) 
                    logger.info("Doctor %s created successfully.", username) 
                    return redirect(url_for('admin.doctors')) 
                except Exception as err: 
                    logger.error("Error creating doctor: %s", err, exc_info=True) 
                    flash('Username already exists, please try with a different one') 
                    return redirect(url_for('admin.add_doctor')) 
            else: 
                logger.warning("Password mismatch for new doctor registration.") 
                flash('Passwords do not match') 
                return redirect(url_for('users.register_user')) 
    else: 
        logger.warning("Unauthorized access attempt to add doctor page.") 
        return redirect(url_for('users.logout')) 
@ADMIN_BLUEPRINT.route('/delete/<idx>', methods=['GET']) 
def delete(idx): 
    logger.info("Attempting to delete user with ID: %s", idx) 
    if session.get('user_type') == 'ADMIN': 
        try: 
            delete_user(idx) 
            logger.info("User with ID %s deleted successfully.", idx) 
            return redirect(url_for('admin.doctors')) 
        except Exception as e: 
            logger.error("Error deleting user: %s", e, exc_info=True) 
            flash('An error occurred while deleting the user.') 
            return redirect(url_for('admin.doctors')) 
    else: 
        logger.warning("Unauthorized access attempt to delete user.") 
        return redirect(url_for('users.logout')) 
@ADMIN_BLUEPRINT.route('/doctors/<idx>', methods=['GET']) 
def view_doctor_slots(idx): 
    logger.info("Viewing slots for doctor with ID: %s", idx) 
    if session.get('user_type') == 'ADMIN': 
        try: 
            slots = get_slot_by_doctor_id(idx) 
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
            return redirect(url_for('admin.doctors')) 
    else: 
        logger.warning("Unauthorized access attempt to view doctor slots.") 
        return redirect(url_for('users.logout')) 
@ADMIN_BLUEPRINT.route('/doctors/<idx>/add_slot', methods=['GET', 'POST']) 
def add_slot(idx=None): 
    logger.info("Accessing add slot page for doctor with ID: %s", idx) 
    if session.get('user_type') == 'ADMIN': 
        if request.method == 'GET': 
            try: 
                doc_name = get_doctor_name(idx) 
                return render_template('doctor_add_slot.html', **{'idx': idx, 'doc_name': doc_name}) 
            except Exception as e: 
                logger.error("Error fetching doctor name: %s", e, exc_info=True) 
                flash('An error occurred while fetching doctor details.') 
                return redirect(url_for('admin.doctors')) 
        else: 
            date = request.form.get('date') 
            slot1, slot2, slot3, slot4 = request.form.get('slot1'), request.form.get('slot2'), request.form.get('slot3'), request.form.get('slot4') 
            try: 
                create_slot(doctor_id=idx, date=date, slots=[slot1, slot2, slot3, slot4]) 
                logger.info("Slots added successfully for doctor with ID: %s", idx) 
                return redirect(url_for('admin.view_doctor_slots', idx=idx)) 
            except Exception as e: 
                logger.error("Error adding slots: %s", e, exc_info=True) 
                flash('An error occurred while adding slots.') 
                return redirect(url_for('admin.view_doctor_slots', idx=idx)) 
    else: 
        logger.warning("Unauthorized access attempt to add slot page.") 
        return redirect(url_for('users.logout'))