from .model_controllers.users_controller import users_controller
from .data_controller import data_controller


def register_controllers(app):
    app.register_blueprint(data_controller)
    app.register_blueprint(users_controller)
