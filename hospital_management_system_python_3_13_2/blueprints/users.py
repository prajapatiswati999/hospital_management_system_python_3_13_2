from flask import Blueprint, request, render_template, session, redirect, url_for, flash 
import logging 
from managers.users import create_user, get_user 
USERS_BLUEPRINT = Blueprint('users', __name__) 
TASKS_INDEX = 'tasks.index' 
USERS_LOGIN = 'users.login' 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
@USERS_BLUEPRINT.route('', methods=['POST']) 
def index(): 
    logger.info("User index accessed.") 
    return redirect(url_for('users.register_user')) 
@USERS_BLUEPRINT.route('/register', methods=['GET', 'POST']) 
def register_user(): 
    logger.info("Accessing user registration page.") 
    if request.method == 'GET': 
        return render_template('register.html') 
    else: 
        username = request.form.get('username') 
        password = request.form.get('psw') 
        password_repeat = request.form.get('psw-repeat') 
        user_type = request.form.get('user-type') 
        first_name = request.form.get('first-name') 
        last_name = request.form.get('last-name') 
        age = request.form.get('age') 
        domain = request.form.get('domain') or 'GENERAL' 
        if password == password_repeat: 
            try: 
                create_user(username=username, password=password, first_name=first_name, last_name=last_name, age=age, 
                            domain=domain, user_type=user_type) 
                logger.info("User %s registered successfully.", username) 
            except Exception as err: 
                logger.error("Error registering user: %s", err, exc_info=True) 
                flash('Username already exists, please try with a different one') 
                return redirect(url_for('users.register_user')) 
            user = get_user(username, password) 
            session['user_idx'] = user.idx 
            session['username'] = user.username 
            session['user_type'] = user.user_type.value 
            logger.info("User %s logged in successfully.", username) 
            if session.get('user_type') == 'DOCTOR': 
                return redirect(url_for('doctors.appointments')) 
            elif session.get('user_type') == 'ADMIN': 
                return redirect(url_for('admin.doctors')) 
            elif session.get('user_type') == 'PATIENT': 
                return redirect(url_for('patients.doctors')) 
        else: 
            logger.warning("Password mismatch during registration for user %s.", username) 
            flash('Passwords do not match') 
            return redirect(url_for('users.register_user')) 
@USERS_BLUEPRINT.route('/login', methods=['GET', 'POST']) 
def login(): 
    logger.info("Accessing user login page.") 
    if 'user_idx' in session: 
        logger.info("User %s already logged in.", session.get('username')) 
        if session.get('user_type') == 'DOCTOR': 
            return redirect(url_for('doctors.appointments')) 
    if request.method == 'GET': 
        return render_template('login.html') 
    else: 
        username = request.form.get('username') 
        password = request.form.get('psw') 
        try: 
            user = get_user(username, password) 
            if user: 
                session['user_idx'] = user.idx 
                session['username'] = user.username 
                session['user_type'] = user.user_type.value 
                logger.info("User %s logged in successfully.", username) 
                if session.get('user_type') == 'DOCTOR': 
                    return redirect(url_for('doctors.appointments')) 
                elif session.get('user_type') == 'ADMIN': 
                    return redirect(url_for('admin.doctors')) 
                elif session.get('user_type') == 'PATIENT': 
                    return redirect(url_for('patients.doctors')) 
            else: 
                logger.warning("Failed login attempt for user %s.", username) 
                flash('Wrong username or password') 
                return redirect(url_for(USERS_LOGIN)) 
        except AttributeError as e: 
            logger.error("Error during login for user %s: %s", username, e, exc_info=True) 
            flash('Wrong username or password') 
            return redirect(url_for(USERS_LOGIN)) 
@USERS_BLUEPRINT.route('/logout', methods=['GET', 'POST']) 
def logout(): 
    logger.info("User %s logging out.", session.get('username')) 
    try: 
        if 'user_type' in session: 
            del session['user_type'] 
        if 'user_idx' in session: 
            del session['user_idx'] 
        if 'username' in session: 
            del session['username'] 
        logger.info("User logged out successfully.") 
    except KeyError as e: 
        logger.error("Error during logout: %s", e, exc_info=True) 
        return redirect(url_for(USERS_LOGIN)) 
    return redirect(url_for(USERS_LOGIN)) 