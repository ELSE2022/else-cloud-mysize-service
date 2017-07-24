from flask import Blueprint, jsonify
from data import data_connection


data_controller = Blueprint('data_controller', __name__)


@data_controller.route('/api/data/checkdb')
def check_db():
    size = data_connection.get_dbsize()
    return jsonify({
        'db_size': size
    })