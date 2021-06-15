import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_POSTGRESQL")


class DevelopmentConfig(Config):
    """Development configuration"""
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    hostname = os.environ["POSTGRES_HOSTNAME"]
    port = os.environ["POSTGRES_PORT"]
    database = os.environ["APPLICATION_DB"]

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{user}:{password}@{hostname}:{port}/{database}"
    )
    """Production configuration"""


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True