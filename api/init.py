from .data_controller import data_controller


def register_controllers(app):
    app.register_blueprint(data_controller)
