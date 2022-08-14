from flask import Blueprint

bp = Blueprint('lower', __name__, url_prefix='/lower')


@bp.route('/')
def lower_get():
    return 'lower'