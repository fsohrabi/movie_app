# Movie Management Application

## Description
This is a Flask-based Movie Management Application that allows users to add, update, delete, and review movies. The app features an admin dashboard for managing users and genres. Future improvements will include additional features and enhanced functionality.

## Getting Started

### Prerequisites
- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Other dependencies listed in `requirements.txt`

### Installation

1. **Clone the repository:**
   ```bash
   git clone <https://github.com/fsohrabi/movie_app
   cd <movie_app>
2. **Install the required packages:**
    ```bash
   pip install -r requirements.txt

3. **Set up environment variables:** Create a file named .env in the root directory of the project with the following content:
   ```
   FLASK_ENV=
   DEV_DATABASE_URL=sqlite:///example.db
   SECRET_KEY=super_secret_development_key
   ADMIN_EMAIL=admin@example.com
   ADMIN_PASSWORD=admin_password
### Database Migration

If you clone this repository and do not have existing migrations, you can initialize the database with the following steps:
1. **Create migrations:**
   ```bash
   flask db init

2. **Create the migration files:**
   ```bash
   flask db migrate -m "Initial migration"
   
3. **apply the migrations to the database:**
   ```bash
   flask db upgrade
   
### Usage
To run the application, use:
   ```bash
   flask run

