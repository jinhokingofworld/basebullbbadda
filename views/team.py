from flask import Blueprint

team_page = Blueprint('team', __name__, static_folder="static", template_folder="templates", url_prefix="/team")


@team_page.route('/')
def hello_pybo():
    return 'Hello, Pybo!'