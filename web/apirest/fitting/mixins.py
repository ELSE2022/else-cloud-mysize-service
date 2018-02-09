import ast

from flask import request
from flask_restplus import marshal

from apirest.restplus import api


class ListModelMixin(object):
    """
    List of objects.
    """
    model = None
    serializer = None
    filter_field = ''

    def get_objects(self):
        return self.model.objects.query()

    def get(self):
        search_query = ast.literal_eval(request.args.get('filter', '{}'))
        if search_query and self.filter_field:
            query_string = search_query.get('q', None)
            objects = self.get_objects().filter(getattr(self.model, self.filter_field if query_string else '_id').like(
                '%{}%'.format(query_string if query_string else search_query.get('id', ''))))
        else:
            objects = self.get_objects()
        if request.args.get('sort_field', None) != 'id' and request.args.get('sort_field', None):
            objects = objects.order_by(getattr(self.model, request.args.get('sort_field')), reverse=request.args['order'] == 'DESC')
        all_objects = [x for x in objects.slice(int(request.args.get('_start', 0)), int(request.args.get('_end', 0))).all()]
        return marshal(all_objects, self.serializer), 200, {'X-Total-Count': len(objects)}
