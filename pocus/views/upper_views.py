from flask import Blueprint

bp = Blueprint('upper', __name__, url_prefix='/upper')


@bp.route('/')
def upper_get():
    return 'Upper'