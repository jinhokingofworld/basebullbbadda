from .user import user_page
from .teampage import team_page
# from .player import player_page
import secrets
from db_config import get_secret_key

def create_app(app): 
    app.register_blueprint(user_page)
    app.register_blueprint(team_page)
    # app.register_blueprint(player_page)
    app.secret_key = get_secret_key() or secrets.token_hex(16)
