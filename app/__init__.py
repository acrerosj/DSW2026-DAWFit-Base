from flask import Flask, render_template
from app.config import Config
from app.models import db, login_manager, Actividad, Usuario


def create_app(config_class=Config):
    """Factoría de aplicaciones de DAW-Fit."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.blueprints.public import public_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.admin import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Manejador de error 403 (Acceso Prohibido)
    @app.errorhandler(403)
    def acceso_prohibido(e):
        return render_template("403.html"), 403

    # TODO (Bloque 1 - Ejercicio 1.3): Registrar el manejador global para el error 404
    # y renderizar la plantilla '404.html' devolviendo el código de estado 404.

    with app.app_context():
        db.create_all()

        # Semilla inicial de actividades deportivas
        if not Actividad.query.first():
            actividades_prueba = [
                Actividad(
                    nombre="Iniciación al Pádel",
                    deporte="Pádel",
                    cuota=32.50,
                    plazas_libres=6,
                ),
                Actividad(
                    nombre="Natación Terapéutica",
                    deporte="Natación",
                    cuota=28.00,
                    plazas_libres=12,
                ),
                Actividad(
                    nombre="Crossfit Nocturno RX",
                    deporte="Crossfit",
                    cuota=45.00,
                    plazas_libres=0,  # Cupo lleno para pruebas del examen
                ),
                Actividad(
                    nombre="Pádel Competición",
                    deporte="Pádel",
                    cuota=40.00,
                    plazas_libres=3,
                ),
            ]
            db.session.add_all(actividades_prueba)
            db.session.commit()

        # Semilla inicial de usuarios (Monitor y Socio)
        if not Usuario.query.first():
            monitor = Usuario(
                username="monitor_jefe",
                email="monitor@dawfit.com",
                edad=32,
                rol="monitor",
            )
            monitor.set_password("monitor123")

            socio = Usuario(
                username="socio_ana",
                email="socio@dawfit.com",
                edad=24,
                rol="socio",
            )
            socio.set_password("socio123")

            db.session.add_all([monitor, socio])
            db.session.commit()

    return app