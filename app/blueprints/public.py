from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_required
from app.models import db, Actividad

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    return redirect(url_for("public.mostrar_actividades"))


@public_bp.route("/actividades")
def mostrar_actividades():
    consulta = Actividad.query
    palabra = request.args.get("busqueda", "")

    consultaCheck = request.args.get("solo_con_plazas", "")

    if palabra:
        consulta = consulta.filter(Actividad.nombre.contains(palabra))
        print(f"estoy filtrando {palabra}")
    if consultaCheck:
        consulta = consulta.filter(Actividad.plazas_libres > 0)
    actividades = consulta.all()

    deporte_fav = request.cookies.get("deporte_fav")

    return render_template(
        "catalogo.html",
        lista_actividades=actividades,
        deporte_fav=deporte_fav,
    )


@public_bp.route("/actividad/<int:act_id>")
def ver_actividad(act_id):
    actividad = db.get_or_404(Actividad, act_id)
    return render_template("actividad_detalle.html", actividad=actividad)


@public_bp.route("/preferencia/<string:deporte>")
def guardar_preferencia(deporte):
    respuesta = make_response(redirect(url_for("public.mostrar_actividades")))
    respuesta.set_cookie(
        "deporte_fav",
        deporte,
        max_age=15 * 24 * 60 * 60,
        httponly=True,
        samesite="Lax",
    )
    return respuesta


@public_bp.route("/limpiar-preferencia")
def limpiar_preferencia():
    respuesta = make_response(redirect(url_for("public.mostrar_actividades")))
    respuesta.delete_cookie("deporte_fav")
    return respuesta


@public_bp.route("/reservas/apuntar/<int:act_id>", methods=["POST"])
@login_required
def apuntar_actividad(act_id):
    flash("Funcionalidad de inscripción pendiente de implementar.", "info")
    return redirect(url_for("public.mostrar_actividades"))


@public_bp.route("/reservas")
@login_required
def ver_reservas():
    return render_template(
        "reservas.html",
        actividades=[],
        total_sin_descuento=0.0,
        descuento_aplicado=False,
        total_final=0.0,
    )


@public_bp.route("/reservas/cancelar/<int:act_id>", methods=["POST"])
@login_required
def cancelar_reserva(act_id):
    return redirect(url_for("public.ver_reservas"))


@public_bp.route("/reservas/confirmar", methods=["POST"])
@login_required
def confirmar_reservas():
    return redirect(url_for("public.mostrar_actividades"))
