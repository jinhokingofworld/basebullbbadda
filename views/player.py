from flask import Blueprint


player_page = Blueprint('player', __name__, static_folder="static", template_folder="templates", url_prefix="/player")



@player_page.route('/')
def hello_pybo():
    return ' <h1> player page 입니다 </h1>'