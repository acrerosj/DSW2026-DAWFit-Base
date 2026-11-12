from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Inicia sesión como socio o monitor para acceder a esta zona."
login_manager.login_message_category = "info"


class Actividad(db.Model):
    __tablename__ = "actividades"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(db.String(100), nullable=False)
    deporte: Mapped[str] = mapped_column(db.String(50), nullable=False)
    cuota: Mapped[float] = mapped_column(db.Float, nullable=False)
    plazas_libres: Mapped[int] = mapped_column(db.Integer, default=10, nullable=False)
    imagen: Mapped[str | None] = mapped_column(db.String(200), nullable=True)

    def __repr__(self) -> str:
        return f"Actividad id={self.id}: {self.nombre} ({self.deporte} - {self.cuota}€)"


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    edad: Mapped[int] = mapped_column(db.Integer, default=18, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(256), nullable=False)
    rol: Mapped[str] = mapped_column(db.String(20), default="socio", nullable=False)

    def set_password(self, password: str) -> None:
        """Genera y almacena el hash seguro de la contraseña."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Comprueba si la contraseña coincide con el hash almacenado."""
        return check_password_hash(self.password_hash, password)

    @property
    def es_monitor(self) -> bool:
        """Devuelve True si el usuario tiene el rol 'monitor'."""
        return self.rol == "monitor"

    def __repr__(self) -> str:
        return f"Usuario id={self.id}: {self.username} ({self.rol})"


@login_manager.user_loader
def cargar_usuario(user_id: str):
    return db.session.get(Usuario, int(user_id))