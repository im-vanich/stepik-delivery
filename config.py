class Configuration:
    DEBUG = True
    SECRET_KEY = "secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///delivery.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False