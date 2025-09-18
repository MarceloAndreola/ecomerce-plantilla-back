import os
from dotenv import load_dotenv
from datetime import timedelta

# Carga automatica de .env en desarrollo
load_dotenv()

class Config:
    #Clave secreta desde la variable de entorno 
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "clave_dev_insegura")
    
    #Configuraciones de tiempo
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_EXPIRES_MINUTES", 60))
    )

    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days = int(os.getenv("JWT_REFRESH_EXPIRES_DAYS", 30))
    )

    #Base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False