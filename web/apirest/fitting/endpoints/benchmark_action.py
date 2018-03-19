from apirest.fitting.serializers import benchmark as benchmark_serializer
from apirest.fitting.mixins import ListModelMixin
from apirest.fitting.mixins import CreateModelMixin
from apirest.fitting.mixins import RetrieveModelMixin
from apirest.fitting.mixins import DestroyModelMixin
from apirest.restplus import api

from data.models import Benchmark
from flask import request
from flask_restplus import Resource

ns = api.namespace('fitting_benchmarks', path='/fitting/benchmarks', description='Operations related to Benchmarks')

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('',)
class Benchmarks(Resource, ListModelMixin, CreateModelMixin):
    model = Benchmark
    serializer = benchmark_serializer

    def get(self):
        return super().get()

    @api.expect(benchmark_serializer)
    def post(self):
        """
        Api method to create benchmark.
        """
        return super().post()


@ns.route('/<string:id>')
class BenchmarkItem(Resource, RetrieveModelMixin, DestroyModelMixin):
    model = Benchmark
    serializer = benchmark_serializer

    def get(self, id):
        return super().get(id)

    @api.expect(benchmark_serializer)
    def put(self, id):
        """
        Api method to update benchmark.
        """
        benchmark_obj = Benchmark.update(id, request.json)
        return {'@rid': id}, 201

    def delete(self, id):
        return super().delete(id)
