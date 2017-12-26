from .web_actions.best_scan import best_scan_action
from .web_actions.get_user_scans import get_user_scans_action
from .web_actions.generate_comparison_config import generate_comparison_config_action
from .web_actions.best_size import best_size_action, best_style_action
from .web_actions.create_user import create_user_action
from .web_actions.get_user_profile import get_user_profile_action
from .web_actions.set_default_size import set_default_size_action
from .web_actions.set_default_scan import set_default_scan_action
from .web_actions.get_file import get_file_action


def register_controllers(app):
    app.register_blueprint(best_scan_action)
    app.register_blueprint(get_user_scans_action)
    app.register_blueprint(generate_comparison_config_action)
    app.register_blueprint(best_size_action)
    app.register_blueprint(best_style_action)
    app.register_blueprint(create_user_action)
    app.register_blueprint(get_user_profile_action)
    app.register_blueprint(set_default_size_action)
    app.register_blueprint(set_default_scan_action)
    app.register_blueprint(get_file_action)
