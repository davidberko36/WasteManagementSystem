
### Waste Management System

## Overview

The Waste Management System is a web application designed to facilitate efficient waste collection and management services. The system allows clients to schedule waste pickups, manage subscriptions, and handle payments seamlessly.

# Features

	•	User Registration and Authentication: Secure user registration and login system.
	•	Scheduling: Clients can choose the start date for waste collection and set up recurring schedules.
	•	Payment Integration: Integrated with Paystack for handling payments. (Disabled for security reasons)
	•	Email Notifications: Automated email notifications for scheduling and payment confirmations.
	•	Admin Dashboard: Admin interface for managing collections, users, and payments.

# Tech Stack

	•	Backend: Django, Django REST Framework
	•	Frontend: HTML, CSS, JavaScript
	•	Database: SQLite (for development), PostgreSQL (for production)
	•	Payment Gateway: Paystack
	•	Email Service: Django Email Backend

# Installation

	1.	Clone the repository:

git clone https://github.com/davidberko36/WasteManagementSystem.git


	2.	Navigate to the project directory:

cd WasteManagementSystem


	3.	Create a virtual environment:

python -m venv env


	4.	Activate the virtual environment:
	•	On Windows:

.\env\Scripts\activate

	4.	
	•	On macOS/Linux:

source env/bin/activate


	5.	Install dependencies:

pip install -r requirements.txt


	6.	Set up environment variables:
	•	Create a .env file in the project root directory.
	•	Add the following variables (replace with your own values):

SECRET_KEY=your_secret_key
PAYSTACK_PUBLIC_KEY=your_paystack_public_key
PAYSTACK_SECRET_KEY=your_paystack_secret_key
EMAIL_HOST_USER=your_email_host_user
EMAIL_HOST_PASSWORD=your_email_host_password


	7.	Run migrations:

python manage.py migrate


	8.	Create a superuser:

python manage.py createsuperuser


	9.	Start the development server:

python manage.py runserver



# Usage

	•	Access the application at http://127.0.0.1:8000.
	•	Admin Dashboard: http://127.0.0.1:8000/admin.

# Contributing

	1.	Fork the repository.
	2.	Create a new branch:

git checkout -b feature-name


	3.	Make your changes and commit:

git commit -m "Add feature"


	4.	Push to the branch:

git push origin feature-name


	5.	Create a pull request.
