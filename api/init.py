from .data_controller import data_controller
from .web_actions.best_scan import best_scan_action


def register_controllers(app):
    app.register_blueprint(data_controller)
    app.register_blueprint(best_scan_action)

