# Hospital Management System 
Welcome to the Hospital Management System. This application is designed to manage hospital operations, including user management, doctor scheduling, and patient appointments. 
## Python Version 
This project has been migrated to Python 3.13.2. Ensure that your development environment is set up with Python 3.13.2 to run the application. 
For detailed information on the migration process and changes, refer to the [Migration Guide](MIGRATION_GUIDE.md). 
## Project Structure 
- **app.py**: The main application file that sets up the Flask app and registers blueprints. 
- **blueprints/**: Contains the different blueprints for user roles such as admin, doctor, and patient. 
- **database/**: Manages database models and connections. 
- **managers/**: Contains business logic for managing users, appointments, and slots. 
- **static/**: Holds static files like CSS for styling. 
- **templates/**: HTML templates for rendering views. 
- **tests/**: Contains test cases for the application. 
## Setup Instructions 
1. **Clone the Repository**: 
   ```bash 
   git clone <repository-url> 
   cd hospital_management_system_python_3_13_2 
   ``` 
2. **Create a Virtual Environment**: 
   ```bash 
   python3.13 -m venv venv 
   source venv/bin/activate 
   ``` 
3. **Install Dependencies**: 
   ```bash 
   pip install -r requirements.txt 
   ``` 
4. **Set Up the Database**: 
   - Ensure the database configuration in `config/settings.staging.cfg` is correct. 
   - Initialize the database: 
     ```bash 
     flask db init 
     flask db migrate 
     flask db upgrade 
     ``` 
5. **Run the Application**: 
   ```bash 
   flask run 
   ``` 
6. **Access the Application**: 
   - Open your web browser and go to `http://localhost:5000`. 
## Features 
- **User Management**: Register, login, and manage different user roles (Admin, Doctor, Patient). 
- **Doctor Scheduling**: Admins can add doctors and manage their available slots. 
- **Patient Appointments**: Patients can view doctors and book appointments. 
## Contributing 
We welcome contributions to improve the Hospital Management System. Please follow the standard GitHub flow for contributions: 
1. Fork the repository. 
2. Create a new branch for your feature or bug fix. 
3. Commit your changes and push to your fork. 
4. Submit a pull request with a description of your changes. 
## License 
This project is licensed under the MIT License. See the LICENSE file for more details. 