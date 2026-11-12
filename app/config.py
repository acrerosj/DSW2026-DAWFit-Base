import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración centralizada del Club Deportivo DAW-Fit."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-desarrollo-examen")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///base_datos_por_defecto.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Carpeta para carteles de actividades deportivas y límite de 2 MB
    UPLOAD_FOLDER = os.path.join("app", "static", "img", "uploads")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    # Duración de la sesión permanente para reservas de actividades
    PERMANENT_SESSION_LIFETIME = timedelta(days=2)