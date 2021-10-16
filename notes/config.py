import os

class Config:
    """Set Flask configuration from environment variables."""

    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/sqlite.db'
    # updated to used MariaDB:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('JAWSDB_MARIA_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # WebApp Settings
    APP_WORKDAY_HOURS = 8
    APP_WORK_PERCENTAGE = 0.9
    # APP_ACCESS_KEY changed to environment variable, depricated
    # APP_ACCESS_KEY = "changeme"
    APP_ACCESS_KEY = os.environ.get('APP_ACCESS_KEY')


