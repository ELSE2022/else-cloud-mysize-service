import io
import swiftclient
from flask import Blueprint, send_file, abort
from data import cloud_object_storage

get_file_action = Blueprint('get_file_action', __name__)

@get_file_action.route('/files/<container>/<filename>')
def get_file(container, filename):
    cont = cloud_object_storage.get_container(container)

    if cont is not None:
        try:
            obj = cont.get_object(filename)
        except swiftclient.exceptions.ClientException:
            abort(404, 'File not found')
        else:
            stream = io.BytesIO(obj[1])
            return send_file(stream,
                             attachment_filename=filename,
                             mimetype='application/octet-stream')

    abort(404, 'Container not found')
