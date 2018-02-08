from flask import request
from flask_restplus import marshal

from apirest.restplus import api


class ListModelMixin(object):
    """
    List of objects.
    """
    model = None
    serializer = None

    def get_objects(self):
        return self.model.objects.query()

    def get(self):
        objects = self.get_objects()
        if request.args.get('sort_field', None) != 'id' and request.args.get('sort_field', None):
            objects = objects.order_by(getattr(self.model, request.args.get('sort_field')), reverse=request.args['order'] == 'DESC')
        all_objects = [x for x in objects.slice(request.args.get('_start', 0), request.args.get('_end', 0)).all()]
        return marshal(all_objects, self.serializer), 200, {'X-Total-Count': len(objects)}
