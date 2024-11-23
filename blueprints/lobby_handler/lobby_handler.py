from flask import Blueprint

lobby_handler_blueprint = Blueprint('lobby_handler', __name__)

@lobby_handler_blueprint.route('/')
def home():
    return f'This is the lobby_handler home page.'
