from .user import user_page
from .teampage import team_page
from .player import player_page
import secrets

def create_app(app): 
    app.register_blueprint(user_page)
    app.register_blueprint(team_page)
    app.register_blueprint(player_page)
    app.secret_key = secrets.token_hex(16)  # 랜덤한 16바이트 키