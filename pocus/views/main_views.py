from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def hello_pocus():
    return 'Hello, Pocus! Yeah'
