from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.models import db, Usuario
from app.forms import LoginForm, RegistroForm, CambiarPasswordForm

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Ruta de Login 100 % funcional para pruebas independientes."""
    if current_user.is_authenticated:
        return redirect(url_for("public.mostrar_actividades"))

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.check_password(form.password.data):
            login_user(usuario, remember=form.remember.data)
            flash(f"¡Hola de nuevo, {usuario.username}!", "exito")

            siguiente_pagina = request.args.get("next")
            if siguiente_pagina and siguiente_pagina.startswith("/"):
                return redirect(siguiente_pagina)
            return redirect(url_for("public.mostrar_actividades"))
        else:
            flash("Correo electrónico o contraseña incorrectos.", "error")

    return render_template("login.html", form=form)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("public.mostrar_actividades"))

    form = RegistroForm()

    return render_template("registro.html", form=form)


@auth_bp.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    form = CambiarPasswordForm()

    return render_template("perfil.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()

    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for("public.mostrar_actividades"))
