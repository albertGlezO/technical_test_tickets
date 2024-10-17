
from config import SystemConfig

def get_connection():
    if SystemConfig.ENV == "TESTING":
       return "config.TestingConfig"
    elif SystemConfig.ENV == "DEVELOPMENT":
       return "config.DevelopmentConfig"
