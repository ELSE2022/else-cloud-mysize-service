# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, urllib

import logging.config
from flask import Blueprint
from flask import Flask, jsonify
from flask import request
from flask import abort
from orientdb_data_layer import data_connection
import api
import settings
from data import cloud_object_storage
from api import authentication
from api.authentication import requires_auth
import posgresql_import
from apirest.fitting.endpoints.action import ns as fitting_namespace
from apirest.fitting.endpoints.product_action import ns as product_namespace
from apirest.fitting.endpoints.brand_action import ns as brand_namespace
from apirest.fitting.endpoints.model_type_action import ns as model_type_namespace
from apirest.fitting.endpoints.size_action import ns as size_namespace
from apirest.fitting.endpoints.model_action import ns as model_namespace
from apirest.fitting.endpoints.scanner_model_action import ns as scanner_model_namespace
from apirest.fitting.endpoints.scanner_action import ns as scanner_namespace
from apirest.fitting.endpoints.scan_action import ns as scan_namespace
from apirest.fitting.endpoints.comparison_result_action import ns as comparison_result_namespace
from apirest.fitting.endpoints.comparison_rule_action import ns as comparison_rule_namespace
from apirest.fitting.endpoints.modeltype_metric_action import ns as model_metric_namespace
from apirest.fitting.endpoints.scan_metric_action import ns as scan_metric_namespace
from apirest.fitting.endpoints.comparison_rule_metric_action import ns as comparison_rule_metric_namespace
from apirest.fitting.endpoints.model_metric_value_action import ns as model_metric_value_namespace
from apirest.fitting.endpoints.visual_action import ns as visual_namespace
from apirest.fitting.endpoints.benchmark_action import ns as benchmark_namespace
from apirest.restplus import api as api_rest


app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

# set web access credentials
authentication.set_credentials(username='else', password='4d84b8e4-7127-11e7-8cf7-a6006ad3dba0')

# connect cloud object-storage
cloud_object_storage.connect_to_storage(dict(key="MfRt~2TyK~nacEY6",
                                             authurl="https://lon-identity.open.softlayer.com/v3",
                                             auth_version='3',
                                             os_options={
                                                'project_id': "ba3612943bd34a1eac2d1e2630bd824b",
                                                'user_id': "a9ba56b9ad794a87aa93ee817890db2d",
                                                'region_name': "london"
                                                }))

# Connect database
initial_drop = False
# data_connection.connect_database('plocal://5.153.55.125:2424/test', 'root', '68f90924-cd63-4df1-a945-47bcd18d45d3', initial_drop)
data_connection.connect_database('plocal://orientdb:2424/test', 'root', 'test', initial_drop)
# data_connection.refresh_models()
data_connection.attach_models()

# Import data from postgress (if needed)
if settings.IMPORT_DATA_FROM_POSTGRES:
    posgresql_import.import_sql('postgresql://postgres:postgres@else-fitting-service.cloudapp.net:54321/else')

# Register API controllers (/api/)
api.register_controllers(app)


@app.route('/fitting/authenticate', methods=('POST',))
def index():
    username = request.json.get('username')
    password = request.json.get('password')
    if username == settings.REST_ADMIN_LOGIN and password == settings.REST_ADMIN_PASSWORD:
        return jsonify({'token': 'f150b933-09fd-461b-b181-4b393ce58cce'})
    return abort(401)
# @app.route('/')
# @requires_auth
# def get_all_routes():
#     output = []
#     for rule in app.url_map.iter_rules():
#
#         options = {}
#         for arg in rule.arguments:
#             options[arg] = "[{0}]".format(arg)
#
#         methods = ','.join(rule.methods)
#         line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule.rule))
#         output.append(line)
#
#     return jsonify(sorted(output))


def configure_app(flask_app):
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('apirest', __name__)
    api_rest.init_app(blueprint)
    api_rest.add_namespace(fitting_namespace)
    api_rest.add_namespace(product_namespace)
    api_rest.add_namespace(brand_namespace)
    api_rest.add_namespace(model_type_namespace)
    api_rest.add_namespace(size_namespace)
    api_rest.add_namespace(model_namespace)
    api_rest.add_namespace(scanner_model_namespace)
    api_rest.add_namespace(scanner_namespace)
    api_rest.add_namespace(scan_namespace)
    api_rest.add_namespace(comparison_result_namespace)
    api_rest.add_namespace(comparison_rule_namespace)
    api_rest.add_namespace(model_metric_namespace)
    api_rest.add_namespace(scan_metric_namespace)
    api_rest.add_namespace(comparison_rule_metric_namespace)
    api_rest.add_namespace(model_metric_value_namespace)
    api_rest.add_namespace(visual_namespace)
    api_rest.add_namespace(benchmark_namespace)
    flask_app.register_blueprint(blueprint)


# local debug config
initialize_app(app)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    log.debug('START APP 111')
    app.run(host='0.0.0.0', port=int(port), debug=settings.FLASK_DEBUG)
