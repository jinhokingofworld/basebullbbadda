from flask import Blueprint

team_page = Blueprint('team', __name__, static_folder="static", template_folder="templates", url_prefix="/team")

#팀 페이지 동적 라우팅
@team_page.route('/<teamName>')
def routing_myPage(teamName):
    return '<h1>' + teamName +'의 teamPage입니다</h1>'

@team_page.route('/')
def hello_pybo():
    return 'Hello, Pybo!'