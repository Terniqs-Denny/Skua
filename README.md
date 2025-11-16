# SKUA – Monitoring System

SKUA is a Django-based monitoring system designed to track, process, and manage real-time data efficiently.  
It provides a modular backend architecture suitable for production, development, and collaborative team workflows.

---

## Features

- **Django REST Framework**–based backend  
- Real-time monitoring logic  
- PostgreSQL database support  
- Modular apps for clean code separation  
- Token-based user authentication (JWT)  
- Environment-based settings (Local, Dev, Prod)  
- Docker-ready project structure  
- CI/CD–friendly deployment setup  

---

## Tech Stack

| Component          | Technology                     |
|--------------------|--------------------------------|
| **Backend**        | Django, Django REST Framework  |
| **Database**       | PostgreSQL                     |
| **Authentication** | JWT                            |
| **Environment**    | Python 3.x                     |
| **Platform**       | GitHub (Version Control)       |
| **Server (optional)** | Gunicorn / Nginx            |
| **Monitoring**     | Custom Django services         |

---

## Installation & Setup

Follow these steps to run SKUA locally or in development/production environments.

### 1. Clone the Repository

git clone https://github.com/Terniqs-Denny/Skua.git





cd skua

#### If using branches:

git checkout dev

### 2. Create Virtual Environment

python -m venv .venv

#### Activate:

**Windows:**

.venv\Scripts\activate

**Mac/Linux:**

source .venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Run Migrations

python manage.py makemigrations
python manage.py migrate

### 5. Run the Server

python manage.py runserver

Server will start at:  
http://127.0.0.1:8000

---

## Environment Setup

Use a `.env` file for configuration (DB, JWT, etc.).  
Example variables are referenced in settings but **not included in this README** for security.

### Database Configuration (PostgreSQL)

Update your environment variables with your PostgreSQL settings:

DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT

Then run:

python manage.py migrate

---

## Git Workflow (For Teams)

# Check current branch
git branch

# Switch to dev branch
git checkout dev

# Stage and commit code
git add .
git commit -m "your message"

# Push to GitHub
git push origin dev

# Pull latest code
git pull origin dev

---

## Deployment

**Production recommended stack:**

- Django + Gunicorn
- Nginx reverse proxy
- PostgreSQL
- Background worker if needed
- Supervisor / systemd for process management

### Basic run command:

gunicorn skua.wsgi --bind 0.0.0.0:8000

---

## Useful Management Commands

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

---

## Contributors & Team Workflow

- Use `dev` branch for working code
- Open Pull Requests to merge into `main` or `master`
- Use clear commit messages
- Follow Django coding standards

---

## Contact

For queries, reach out to the project maintainers:  
**leo Paulose, Abhinav P, Denisious K D**  
Email: terniqs.denny@gmail.com
