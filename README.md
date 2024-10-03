# Strategic_Crime_Monitoring

## Project Overview
This is a Flask-based web application designed to manage a police station's operations, including user registration, complaint management, and case tracking.

## Features
- User registration and login system
- Complaint management system for users
- Case tracking system for police station administrators
- Advocate registration and management system
- Station administrator dashboard for managing employees and cases

## Requirements
- Python 3.8+
- Flask 2.0+
- MySQL 8.0+
- Flask-MySQL 1.5+
- Flask-Mail 0.9+
- Flask-Cors 3.0+

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a MySQL database and update the `app.config` settings accordingly.

4. Run the application:
   ```bash
   py run.py
   ```

## Endpoints

### User Endpoints
- `/login`: User login endpoint
- `/user_registration`: User registration endpoint
- `/user_add_complaint`: User complaint submission endpoint
- `/user_add_spot_complaint`: User spot complaint submission endpoint
- `/user_personalized_complaint`: User personalized complaint submission endpoint
- `/user_view_case_request`: User case request viewing endpoint

### Station Administrator Endpoints
- `/station_admin_home`: Station administrator dashboard endpoint
- `/station_admin_add_employee`: Station administrator employee addition endpoint
- `/station_admin_manage_employee`: Station administrator employee management endpoint
- `/station_admin_view_spot_complaints`: Station administrator spot complaint viewing endpoint
- `/station_admin_view_complaints`: Station administrator complaint viewing endpoint
- `/station_admin_view_normal_complaint`: Station administrator normal complaint viewing endpoint
- `/station_admin_view_personalize_complaint`: Station administrator personalized complaint viewing endpoint

### Advocate Endpoints
- `/advocate_registration`: Advocate registration endpoint
- `/advocate_admin_view_advocate`: Advocate administrator advocate viewing endpoint
- `/advocate_admin_view_advocate_rating`: Advocate administrator advocate rating viewing endpoint
- `/advocate_admin_accept_advocate`: Advocate administrator advocate acceptance endpoint
- `/advocate_admin_delete_advocate`: Advocate administrator advocate deletion endpoint

### Admin Endpoints
- `/admin`: Admin dashboard endpoint
- `/admin_add_station`: Admin station addition endpoint
- `/admin_add_station_employee`: Admin station employee addition endpoint
- `/admin_view_station`: Admin station viewing endpoint
- `/admin_view_employee`: Admin employee viewing endpoint
- `/admin_add_advocate_admin`: Admin advocate administrator addition endpoint
- `/view_manage_advocate`: Admin advocate management endpoint

## Database Schema
The database schema is designed to support the application's features and is divided into the following tables:
- `login`: Stores user login information
- `registration`: Stores user registration information
- `station`: Stores police station information
- `station_user_map`: Maps users to police stations
- `advocate_info`: Stores advocate information
- `complaint_against_advocate`: Stores complaints against advocates
- `quick_complaint`: Stores quick complaints
- `normal_complaints`: Stores normal complaints
- `personalised_complaints`: Stores personalized complaints
- `cases`: Stores case information
- `advocate_request`: Stores advocate requests

> **Note:** The database schema is not included in this README, but it can be found in the `db.sql` file.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.
