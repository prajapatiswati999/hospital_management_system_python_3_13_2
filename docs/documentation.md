# Hospital Management System Documentation 
## Overview 
The Hospital Management System is a web-based application designed to manage hospital operations, including user management, appointment scheduling, and slot booking. This document provides an overview of the system's architecture, functionality, and setup instructions. 
## Table of Contents 
1. [Introduction](#introduction) 
2. [Architecture](#architecture) 
3. [Functional Overview](#functional-overview) 
4. [Dependencies](#dependencies) 
5. [Configuration](#configuration) 
6. [Environment Setup](#environment-setup) 
7. [Testing](#testing) 
8. [Deployment](#deployment) 
9. [Logging and Monitoring](#logging-and-monitoring) 
## Introduction 
The Hospital Management System is built using Flask, a lightweight WSGI web application framework in Python. It leverages SQLAlchemy for database interactions and supports user roles such as Admin, Doctor, and Patient. 
## Architecture 
- **Flask Application**: The core of the application, handling HTTP requests and responses. 
- **Blueprints**: Modular components for different user roles (Admin, Doctor, Patient, Users). 
- **Database**: Managed using SQLAlchemy, with models for Users, Doctors, Appointments, and Slots. 
- **Asynchronous Operations**: Utilizes Python's `asyncio` for non-blocking operations, enhancing performance. 
## Functional Overview 
- **User Management**: Registration, login, and role-based access control. 
- **Appointment Scheduling**: Doctors can manage their slots, and patients can book appointments. 
- **Prescription Management**: Doctors can update prescriptions for appointments. 
## Dependencies 
Ensure the following dependencies are installed: 
- **Python 3.13.2**: The application is compatible with Python 3.13.2. 
- **Flask**: Web framework for building the application. 
- **Flask-SQLAlchemy**: ORM for database interactions. 
- **Gunicorn**: WSGI server for running the application in production. 
Refer to `requirements.txt` for a complete list of dependencies. 
## Configuration 
- **Database URI**: Set the `SQLALCHEMY_DATABASE_URI` in `config/settings.staging.cfg` to point to your database. 
- **Secret Keys**: Ensure `SECRET_KEY` and other sensitive configurations are set appropriately. 
## Environment Setup 
1. **Install Python 3.13.2**: Follow the official Python documentation to install Python 3.13.2. 
2. **Set Up Virtual Environment**: 
   ```bash 
   python3.13 -m venv venv 
   source venv/bin/activate  # On Windows use `venv\Scripts\activate` 
   ``` 
3. **Install Dependencies**: 
   ```bash 
   pip install -r requirements.txt 
   ``` 
4. **Database Initialization**: Initialize the SQLite database by running the Flask application: 
   ```bash 
   flask run 
   ``` 
## Testing 
Run unit tests to ensure the application functions correctly: 
```bash 
pytest tests/ 
``` 
## Deployment 
- **Gunicorn**: Use Gunicorn to run the application in a production environment. 
- **Procfile**: Verify deployment settings in the `Procfile`. 
## Logging and Monitoring 
Set up logging and monitoring to track application performance and identify issues. The application uses Python's `logging` module for logging. 
## Conclusion 
This documentation provides a comprehensive overview of the Hospital Management System, including its architecture, functionality, and setup instructions. For migration details to Python 3.13.2, refer to the `migration_guide.md`. 