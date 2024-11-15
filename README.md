# Secure File Storage System

This project is a Flask-based web application that provides a secure environment for file storage and management. It features user authentication, encrypted file storage, and role-based access control.

## Features

- User authentication (login, logout, and registration)
- Secure file upload and download
- Encryption and decryption of files using `cryptography`
- Database integration with SQLAlchemy
- Role-based access control
- Secure access to files with Flask-Login

## Technologies Used

- **Backend**: Flask
- **Database**: SQLite (via SQLAlchemy)
- **Encryption**: `cryptography` (Fernet encryption)
- **Frontend**: HTML and Flask templates
- **Other Libraries**: Flask-Login for user session management

## Prerequisites

- Python 3.7 or above
- Flask and related libraries
- SQLAlchemy
- Cryptography library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/secure-file-storage.git
   cd secure-file-storage
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
3. Set up the database:
   ```bash
   python app.py
4. Run the application:
   ```bash
   python app.py
5. Open your browser and navigate to:
   ```bash
   http://127.0.0.1:5000/
## Project Structure
secure-file-storage/
├── app.py                # Main application file
├── templates/            # HTML templates for the app
├── static/               # Static assets (CSS, JS, images)
├── models.py             # Database models
├── routes/               # Routes and API endpoints
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation

