"""System configuration"""
import os
import click

class SystemConfig:#pylint: disable=R0903
    """System configuration class"""
    ENV = os.environ["ENV"] if "ENV" in os.environ else "DEVELOPMENT"
    CSRF_ENABLED = True
    SECRET_KEY = "this_is_a_secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(SystemConfig):#pylint: disable=R0903
    """Development configuration class"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://" + os.environ["DB_USERNAME"] + ":"  \
        + os.environ["DB_PASSWORD"] + "@" \
        + os.environ["DB_HOST"] + ":" \
        + os.environ["DB_PORT"] + "/" \
        + os.environ["DB_DATABASE"]
    )
    click.echo(SQLALCHEMY_DATABASE_URI)


class TestingConfig(SystemConfig):#pylint: disable=R0903
    """Testing cnfiguration class"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://" + os.environ["DB_USERNAME"] + ":" \
        + os.environ["DB_PASSWORD"] + "@" \
        + os.environ["DB_HOST"] + ":" \
        + os.environ["DB_PORT"] + "/" \
        + os.environ["DB_DATABASE"]
    )
