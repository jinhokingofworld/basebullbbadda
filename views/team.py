from flask import Blueprint,render_template

team_page = Blueprint('team', __name__, static_folder="static", template_folder="templates", url_prefix="/team")


@team_page.route('/')
def teamddd():
    return render_template('teampage.html')