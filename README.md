# IVS Network Configuration Management System

A Django-based web application for managing and storing configuration data for the International VLBI Service for Geodesy and Astrometry (IVS) network. This project is developed as part of a university initiative at the Technical University of Munich (TUM).

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Credits and Acknowledgments](#credits-and-acknowledgments)
- [License](#license)

---

## Project Overview

The **IVS Network Configuration Management System** is a comprehensive web-based platform designed to facilitate the collection, storage, and management of technical configuration data within the International VLBI Service for Geodesy and Astrometry (IVS) network.

This application provides a structured interface for managing:
- **Antenna Information**: Site descriptions, DOMES identifiers, approximate positions, and instrument details
- **Configuration Data**: Detailed technical specifications including receiver information, data acquisition systems, meteorological instrumentation, and field system computers
- **Logbook Entries**: technical modifications, and operational events
- **Summary Views**: Consolidated reports and historical data tracking

### Project Status

This project is currently in **Phase 1 (Part 1)**, focusing on:
- Creating structured, user-friendly forms with comprehensive validation
- Establishing database connections using Django ORM
- Implementing a clean, modern, and responsive front-end layout with uniformly sized fields and proper alignment
- Setting up user authentication and session management
- Implementing audit logging for tracking changes

### Scope and Purpose

The system serves as a centralized repository for:
- VLBI station metadata and technical specifications
- Equipment configuration and maintenance records
- Contact information for site operators and responsible agencies
- Historical tracking of configuration changes through audit logs

---

## Features

### Current Features (Phase 1)

#### 1. **User Management**
- User registration and authentication system
- Secure login/logout functionality
- Session-based user tracking
- One-to-one relationship between users and their configuration entries

#### 2. **Antenna Information Management**
- **Request Form**: Capture requester details (name, agency, email, date)
- **Site Description**: Site name, location (city/town, state/province, country), point description, and optional images
- **DOMES Information**: DOMES number, local number, and 4-character site code
- **Approximate Position**: X/Y/Z coordinates, latitude/longitude, elevation, tectonic plate, and position source
- **Instrument Details**: Instrument name and installation date
- **Operation Contact**: Primary and secondary operation contacts with email addresses
- **Site Contact**: Site contact information and additional notes

#### 3. **Configuration Information Management**
Comprehensive multi-section forms covering:
- **Contact Information**: Prepared by details, report type, and update dates
- **Site Identification**: Site codes (8-letter, 2-letter), IERS DOMES number, IGS/ILRS codes, and operation dates
- **Local Survey Network**: Marker types, survey frequency, methods, instruments, and accuracy
- **Site Descriptive Information**: File uploads for site maps, diagrams, horizon masks, monument descriptions, and photographs (with URL alternatives)
- **Antenna Details**: Antenna type, diameter, axis information, slew rates, limits, and horizon mask data
- **Receiver Information**: Feed location/type, amplifiers, bandwidth, system temperatures, SEFD, aperture efficiency, and LO frequencies
- **Cables and Backend**: Cable types, lengths, frequency bandpasses, and cable measurement systems
- **Data Acquisition System**: Video converters, formatters, decoders, IF distributors, converters, recorders, and configuration types
- **Meteorological Instrumentation**: Humidity, pressure, and temperature sensor specifications
- **Time and Frequency Standards**: Standard types, manufacturers, and installation dates
- **Auxiliary Equipment**: Two equipment slots with detailed specifications
- **Co-location Information**: Instrument types, names, status, and survey inclusion
- **Field System Computer**: System vendor, CPU, memory, disk, OS, and network information
- **On-site Contact Information**: Agency details, addresses, telephone/fax numbers, and email contacts
- **Responsible Agency**: Primary and alternative agency information with full contact details

#### 4. **Logbook System**
- **Event Logging**: Record entry time, event time, technician/editor, and participants
- **Component Tracking**: Predefined dropdown menu for radio telescope components (e.g., servosystem, antenna control, frontend, backend, calibration systems, etc.) with the ability to add custom components
- **Detailed Information**: Text fields for comprehensive event descriptions
- **File Attachments**: Upload diagrams, quality plots, PDFs, and other supporting documentation

#### 5. **Summary and Reporting**
- User-specific log summaries
- Historical data views
- Audit trail tracking via `django-auditlog`

#### 6. **Modern UI/UX Design**
- Clean, professional interface
- Tidy, aligned form layouts
- Uniformly sized input fields
- Responsive design for different screen sizes
- Navigation with sub-navigation for complex forms
- Success confirmation pages after form submissions

#### 7. **Audit Logging**
- Automatic tracking of all changes to Antenna and Configuration records
- Historical data retention
- User attribution for all modifications

---

## Installation

### Prerequisites

Before you begin, ensure you have the following installed on your system:
- **Python 3.9** or higher
- **pip** (Python package installer)
- **Git** (for cloning the repository)
- **virtualenv** (optional but recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ivs-network-config.git
cd ivs-network-config
```

### Step 2: Create and Activate a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

**On macOS/Linux:**
```bash
python3 -m venv django_tum
source django_tum/bin/activate
```

**On Windows:**
```bash
python -m venv django_tum
django_tum\Scripts\activate
```

### Step 3: Install Dependencies

Install the required Python packages:

```bash
pip install django==5.1
pip install django-auditlog
pip install Pillow  # For image handling
```

Alternatively, if a `requirements.txt` file is provided:

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables (Optional)

For production deployment, consider setting environment variables for sensitive information such as the Django `SECRET_KEY`. For development purposes, the default settings in `seperated_apps_project/settings.py` will work.

---

## Database Setup

This project uses **SQLite** as the default database for local development.

### Step 1: Apply Database Migrations

Run the following commands to create the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create a `db.sqlite3` file in the project root directory.

### Step 2: Create a Superuser (Admin Account)

To access the Django admin interface and manage data:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your admin username, email, and password.

### Step 3: (Optional) Load Initial Data

If you have initial data fixtures, you can load them using:

```bash
python manage.py loaddata initial_data.json
```

---

## Project Structure

```
django_project/
│
├── manage.py                      # Django management script
├── db.sqlite3                     # SQLite database file
├── README.md                      # This file
│
├── seperated_apps_project/        # Main project configuration
│   ├── __init__.py
│   ├── settings.py                # Project settings and configuration
│   ├── urls.py                    # Root URL routing
│   ├── wsgi.py                    # WSGI configuration for deployment
│   └── asgi.py                    # ASGI configuration for async support
│
├── antenna/                       # Antenna information management app
│   ├── models.py                  # AntennaInfo model with audit logging
│   ├── forms.py                   # Django forms for antenna data entry
│   ├── views.py                   # Views for handling requests and rendering templates
│   ├── urls.py                    # URL routing for antenna app
│   ├── admin.py                   # Django admin configuration
│   ├── migrations/                # Database migration files
│   └── templates/antenna/         # HTML templates for antenna forms
│       ├── request_form.html
│       ├── site_description.html
│       ├── domes_info.html
│       ├── approximate_position.html
│       ├── instrument.html
│       ├── operation_contact.html
│       ├── site_contact.html
│       ├── summary.html
│       └── success.html
│
├── configuration/                 # Configuration information management app
│   ├── models.py                  # ConfigurationInfo model with extensive fields
│   ├── forms.py                   # Forms for configuration data entry
│   ├── views.py                   # Views for configuration workflows
│   ├── urls.py                    # URL routing for configuration app
│   ├── admin.py                   # Django admin configuration
│   ├── migrations/                # Database migration files
│   └── templates/configuration/   # HTML templates for configuration forms
│       └── [18 HTML form templates]
│
├── logbook/                       # Logbook entries management app
│   ├── models.py                  # LogbookInfo model with component choices
│   ├── forms.py                   # Forms for logbook entries
│   ├── views.py                   # Views for logbook functionality
│   ├── urls.py                    # URL routing for logbook app
│   ├── migrations/                # Database migration files
│   └── templates/logbook/         # HTML templates for logbook
│       ├── form.html
│       ├── logbook.html
│       ├── summary.html
│       └── success.html
│
├── summary/                       # Summary and reporting app
│   ├── models.py                  # Models for summary views
│   ├── views.py                   # Views for generating summaries
│   ├── urls.py                    # URL routing for summary app
│   └── templates/summary/         # HTML templates for summaries
│       ├── summary.html
│       └── user_logs.html
│
├── welcome/                       # Welcome/landing page app
│   ├── views.py                   # Welcome page view
│   ├── urls.py                    # URL routing
│   └── templates/welcome/
│       └── welcome.html
│
├── login/                         # User authentication app
│   ├── forms.py                   # Login forms
│   ├── views.py                   # Authentication views
│   ├── urls.py                    # URL routing for login
│   └── templates/login/
│       └── login.html
│
├── registeration/                 # User registration app (note: spelling)
│   ├── forms.py                   # Registration forms
│   ├── views.py                   # Registration views
│   ├── urls.py                    # URL routing for registration
│   └── templates/registeration/
│       └── registeration.html
│
├── impressum/                     # Imprint/legal information app
│   ├── views.py                   # Imprint page view
│   ├── urls.py                    # URL routing
│   └── templates/imprint/
│       └── imprint.html
│
├── templates/                     # Shared templates directory
│   ├── base.html                  # Base template with common layout
│   └── includes/
│       ├── antenna_subnav.html    # Sub-navigation for antenna forms
│       └── configuration_subnav.html  # Sub-navigation for config forms
│
├── static/                        # Static files (CSS, JS, images)
│   ├── style.css                  # Custom stylesheet
│   └── images/
│       └── logo.png               # Project logo
│
├── staticfiles/                   # Collected static files for production
│   └── [Django admin static files and collected static assets]
│
└── django_tum/                    # Virtual environment directory
    └── [Python virtual environment files]
```

### Key Directories and Files

- **`manage.py`**: Command-line utility for Django administrative tasks
- **`settings.py`**: Contains all project settings (database, installed apps, middleware, static files, etc.)
- **`models.py`**: Defines database schema using Django ORM
- **`forms.py`**: Django forms for data validation and rendering
- **`views.py`**: Request handlers and business logic
- **`urls.py`**: URL routing configuration
- **`templates/`**: HTML templates for rendering pages
- **`static/`**: CSS, JavaScript, and image files
- **`migrations/`**: Database schema version control

---

## Usage

### Step 1: Start the Development Server

Run the Django development server:

```bash
python manage.py runserver
```

By default, the server will run on `http://127.0.0.1:8000/`.

### Step 2: Access the Application

Open your web browser and navigate to:

```
http://127.0.0.1:8000/
```

You will be greeted with the welcome page.

### Step 3: Register a New User

1. Click on the **Register** link or navigate to `http://127.0.0.1:8000/registeration/`
2. Fill in the registration form with your details (username, email, password)
3. Submit the form to create your account

### Step 4: Log In

1. Navigate to the **Login** page at `http://127.0.0.1:8000/login/`
2. Enter your credentials
3. Upon successful login, you'll be redirected to the main application

### Step 5: Navigate the Application

The application consists of several main sections accessible via the navigation menu:

#### **Antenna Section**
Navigate to the Antenna tab to enter antenna-related information. The form is divided into multiple sub-sections:
1. **Request Form**: Enter your name, agency, email, and date
2. **Site Description**: Provide site details and location information
3. **DOMES Info**: Enter DOMES number and site codes
4. **Approximate Position**: Input coordinates and elevation data
5. **Instrument**: Specify installed instruments
6. **Operation Contact**: Add operation contact details
7. **Site Contact**: Add site contact information
8. **Summary**: Review all entered data before submission

#### **Configuration Section**
Navigate to the Configuration tab for detailed technical specifications. This section includes 18 different sub-forms covering:
- Contact information
- Site identification
- Local survey network details
- Site descriptive information (with file uploads)
- Antenna details and specifications
- Receiver information
- Cable and backend configurations
- Data acquisition system specifications
- Meteorological instrumentation
- Time and frequency standards
- Auxiliary equipment
- Co-location information
- Field system computer details
- On-site contact information
- Responsible agency information

#### **Logbook Section**
Navigate to the Logbook tab to:
1. Record maintenance events and technical modifications
2. Select the affected component from the dropdown menu
3. Add detailed descriptions
4. Upload supporting documentation (diagrams, plots, PDFs)
5. View historical logbook entries

#### **Summary Section**
View consolidated reports and historical data for your entries.

#### **Imprint**
Access legal and institutional information.

### Step 6: Django Admin Interface

To manage data directly through the Django admin interface:

1. Navigate to `http://127.0.0.1:8000/admin/`
2. Log in with your superuser credentials
3. Access and manage all database records

### Step 7: Logging Out

Click the **Logout** button in the navigation menu to end your session.

---

## Technologies Used

- **Backend Framework**: Django 5.1
- **Database**: SQLite (default for development)
- **ORM**: Django ORM
- **Authentication**: Django's built-in authentication system
- **Audit Logging**: django-auditlog
- **File Handling**: Django's FileField and ImageField with Pillow
- **Frontend**: HTML5, CSS3 (custom stylesheets)
- **Template Engine**: Django Template Language (DTL)
- **Version Control**: Git

### Python Packages

- `Django==5.1`: Web framework
- `django-auditlog`: Audit logging for model changes
- `Pillow`: Python Imaging Library for image handling
- `sqlparse`: SQL parsing library (Django dependency)

---

### Related Resources

- [Technical University of Munich](https://www.tum.de/)
- [Django Documentation](https://docs.djangoproject.com/)

---

## License


---

**Last Updated**: October 2025   
**Django Version**: 5.1  
**Python Version**: 3.9+

