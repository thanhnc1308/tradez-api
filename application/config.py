import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_POSTGRESQL")


class DevelopmentConfig(Config):
    """Development configuration"""
    # user = os.environ["POSTGRES_USER"]
    # password = os.environ["POSTGRES_PASSWORD"]
    # hostname = os.environ["POSTGRES_HOSTNAME"]
    # port = os.environ["POSTGRES_PORT"]
    # database = os.environ["APPLICATION_DB"]

    # SQLALCHEMY_DATABASE_URI = (
    #     f"postgresql+psycopg2://{user}:{password}@{hostname}:{port}/{database}"
    # )

    # SQLALCHEMY_DATABASE_URI = (
    #     f"postgresql+psycopg2://ogwsmojrynkhmc:5e3f5b888472b53141e050ea3e366765203feab53b43a13248b65f718e477e63@ec2-52-86-2-228.compute-1.amazonaws.com:5432/dg0q8kfl0thi4"
    # )

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_POSTGRESQL")

class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True