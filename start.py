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

import os
from flask import Flask, jsonify
import urllib
import data
import api
from orientdb_data_layer import data_connection
import posgresql_import

app = Flask(__name__)

# Connect database
initial_drop = False
data_connection.connect_database('plocal://5.153.55.125:2424/test', 'root', '68f90924-cd63-4df1-a945-47bcd18d45d3', initial_drop)
data_connection.refresh_models()

# Import data from postgress (if needed)
# posgresql_import.import_sql('postgresql://postgres:postgres@localhost:5432/else')

# Register API controllers (/api/)
api.register_controllers(app)


@app.route('/')
def get_all_routes():
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule.rule))
        output.append(line)

    return jsonify(sorted(output))


# local debug config
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
