from flask import Blueprint

bp = Blueprint('app', __name__, url_prefix='/team')


@bp.route('/')
def hello_pybo():
    return 'Hello, Pybo!'