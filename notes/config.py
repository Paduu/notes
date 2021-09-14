class Config:
    """Set Flask configuration from environment variables."""

    # Flask
    SECRET_KEY = 'rd3pcOkVyj5wFDf02QDr'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/sqlite.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # WebApp Settings
    APP_WORKDAY_HOURS = 8
    APP_WORK_PERCENTAGE = 0.9
    APP_ACCESS_KEY = "changeme"