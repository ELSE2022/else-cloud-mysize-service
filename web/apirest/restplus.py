import logging
import traceback

from flask import url_for
from flask_restplus import Api
from flask import request
from flask import abort
import settings
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}


class CustomAPI(Api):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=False)

    def _register_doc(self, app_or_blueprint):
        if self._add_specs and self._doc:
            # Register documentation before root if enabled
            app_or_blueprint.add_url_rule(self._doc, 'doc', self.render_doc)
            app_or_blueprint.add_url_rule(self._doc + '/', 'doc', self.render_doc)
        app_or_blueprint.add_url_rule(self.prefix or '/', 'root', self.render_root)


api = CustomAPI(version='1.0', title='Fitting Service', doc='/docs')


def auth_required(func):
    func = api.doc(security='apikey')(func)

    def check_auth(*args, **kwargs):
        if 'X-API-KEY' not in request.headers:
            abort(401, 'API key required')
        request.headers['X-API-KEY']
        return func(*args, **kwargs)
    return check_auth


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
