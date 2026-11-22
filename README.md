# ArtisTrack – Secure Artist Management System

A Django web application for managing dance artists, trainings, attendance, performances and injury records. Built for the Secure Design and Development module of my M.Sc. in Cybersecurity (Coventry University).

## User roles
- **Admin** – manages users and views audit logs; creates Director and Coach accounts
- **Director**, **Coach** – staff roles created by the Admin
- **Artist** – the only role available through public registration

Admin accounts cannot be created through the application.

## Security features
- Role-based access control (4 roles) with a custom user model and role-checking decorators
- Admin two-factor authentication: 6-digit email OTP, valid for 5 minutes, with resend option
- Brute-force protection with django-axes (lockout after 5 failed attempts, 15-minute cool-off)
- CAPTCHA on login, registration, password change and forgot-password forms
- Strong password policy (minimum 12 characters with uppercase, lowercase, number and special character)
- Secure password reset using Django's token generator
- Session timeout after 15 minutes of inactivity
- Custom SQL injection protection middleware
- CSRF protection, HttpOnly cookies, clickjacking protection (X-Frame-Options: DENY) and MIME-sniffing protection
- Audit logging of logins, registrations, account creation and password changes
- Secrets stored in environment variables (.env), not in code

## Tech stack
Python, Django, SQLite, Bootstrap

## Run locally
1. Create and activate a virtual environment:
   `python -m venv venv` then `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file in the project root containing: `DJANGO_SECRET_KEY=your-secret-key`
4. Apply migrations: `python manage.py migrate`
5. Create an admin account: `python manage.py createsuperuser`, then set its role to `admin` in the Django admin
6. Start the server: `python manage.py runserver`, then open http://127.0.0.1:8000

In development, OTP and password-reset emails are printed to the terminal (Django console email backend).

## Note
This is an academic project configured for local development (DEBUG = True). It is not intended for production deployment.
