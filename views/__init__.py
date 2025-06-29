from .user import user_page
from .team import team_page
from .player import player_page
import secrets

def create_app(app): 
    app.register_blueprint(user_page)
    app.register_blueprint(team_page)
    app.register_blueprint(player_page)
    app.secret_key = str(secrets.SystemRandom)