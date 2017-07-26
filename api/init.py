from .data_controller import data_controller
from .web_actions.best_scan import best_scan_action
from .web_actions.get_user_scans import get_user_scans_action
from .web_actions.generate_comparison_config import generate_comparison_config_action


def register_controllers(app):
    app.register_blueprint(data_controller)
    app.register_blueprint(best_scan_action)
    app.register_blueprint(get_user_scans_action)
    app.register_blueprint(generate_comparison_config_action)
