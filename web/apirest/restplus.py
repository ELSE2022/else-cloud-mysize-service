import logging
import traceback
import os

from flask_restplus import Api
from flask import request
from flask import abort
from flask import url_for
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
print('HTTPS', os.environ.get('HTTPS'))
@property
def specs_url(self):
    """Monkey patch for HTTPS"""
    return url_for(self.endpoint('specs'), _external=True, _scheme='https')

Api.specs_url = specs_url
api = Api(version='1.0', title='Fitting Service', doc='/docs/')


def auth_required(func):
    func = api.doc(security='apikey')(func)

    def check_auth(*args, **kwargs):
        if 'X-API-KEY' not in request.headers:
            abort(401, 'API key required')
        key = request.headers['X-API-KEY']
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
