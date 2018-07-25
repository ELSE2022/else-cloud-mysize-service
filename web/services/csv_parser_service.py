import tempfile
import petl as etl
import operator
from toolz import functoolz, itertoolz, dicttoolz
from functools import partial

from orientdb_data_layer import data_connection

from data.repositories import ProductRepository
from data.repositories import ModelRepository
from data.repositories import ModelTypeRepository
from data.repositories import SizeRepository
from data.repositories import BrandRepository
from data.repositories import ComparisonRuleRepository
from data.repositories import ComparisonRuleMetricRepository
from data.repositories import ModelTypeMetricRepository
from data.repositories import ScanMetricRepository
from data.repositories import ScannerModelRepository
from data.repositories import ModelMetricValueRepository
from data.repositories import ComparisonResultRepository

_productRep = ProductRepository()
_modelRep = ModelRepository()
_modelTypeRep = ModelTypeRepository()
_sizeRep = SizeRepository()
_brandRep = BrandRepository()
_compRuleRep = ComparisonRuleRepository()
_compRuleMetricRep = ComparisonRuleMetricRepository()
_modelTypeMetricRep = ModelTypeMetricRepository()
_scanMetricRep = ScanMetricRepository()
_scannerModelRep = ScannerModelRepository()
_modelMetricValueRep = ModelMetricValueRepository()
_comparisonResultRep = ComparisonResultRepository()


class CSVParserService:

    @classmethod
    def get_model_type_metrics(cls, model_types, metric_name):
        """
        Return metrics by models types and metric name

        Parameters
        ----------
        model_types: list of data.models.ModelType.ModelType
            Entity of model type model
        metric_name: str
            Metric name

        Returns
        -------
        tuple of data.models.ModelTypeMetric.ModelTypeMetric
        """
        return tuple(
            map(
                partial(_modelTypeMetricRep.get_by_name_and_scanner_model, metric_name=metric_name),
                model_types,
            )
        )

    @classmethod
    def divide_table(cls, fields, divide_fields, tbl, suffix):
        """
        Divide tables

        Parameters
        ----------
        fields: tuple of str
            Fields which should stay as is
        divide_fields: tuples of str
            Fields which should be divided
        tbl: petl table
            Petl table
        suffix: str
            String which should be added to each divided field

        Returns
        -------
        tuple of petl tables
        """
        return etl.cut(tbl, fields + tuple(map(partial(functoolz.flip, operator.add, suffix), divide_fields)))

    @classmethod
    def create_temp_file(cls, data):
        """
        Create temp file

        Parameters
        ----------
        data: bytes
            Binary content

        Returns
        -------
        file: tempfile.NamedTemporaryFile
            Temporary file
        """
        file = tempfile.NamedTemporaryFile(delete=False)
        file.write(data)
        file.close()
        return file

    @classmethod
    def parse_scan_csv(cls, data, scan):
        """
        Parse scan csv

        Parameters
        ----------
        data: bytes
            CSV content in binary string
        scan: data.models.Scan.Scan
            Scan model

        Returns
        -------
        dict with parsed csv
        """
        _graph = data_connection.get_graph()
        scanner_obj = _graph.element_from_link(scan.scanner)
        init_table = etl.fromcsv(cls.create_temp_file(data).name, delimiter=';')
        table = init_table.skip(1) if 'DOMESCAN' in init_table.header() else init_table
        return functoolz.pipe(
            itertoolz.first(table.dicts()),
            partial(dicttoolz.itemmap, reversed),
            partial(dicttoolz.valmap, partial(_scanMetricRep.get_by_name_and_scanner_model, scanner_obj.model)),
            operator.methodcaller('items'),
            partial(filter, operator.itemgetter(1)),
        )

    @classmethod
    def get_empty_model_data(cls):
        """
        Return empty parsed csv object

        Returns
        -------
        dict with empty etl object
        """
        return dict(metrics=etl.empty(), success=True, errors=etl.empty())

    @classmethod
    def parse_model_csv(cls, data, product_obj):
        """
        Parse model csv

        Parameters
        ----------
        data: bytes
            CSV content in binary string
        product_obj: data.models.Product.Product
            Product model

        Returns
        -------
        dict with parsed csv
        """
        _sizeRep.delete(dict())

        _graph = data_connection.get_graph()

        comparision_rule = _compRuleRep.get({'@rid': product_obj.default_comparison_rule})[0]
        model_types = comparision_rule.model_types
        scanner_model = comparision_rule.scanner_model
        float_columns = (
            'value',
            'f1_l',
            'shift_l',
            'f2_l',
            'f1_r',
            'shift_r',
            'f2_r',
        )
        str_columns = (
            'size',
            'model_metric',
            'scan_metric',
        )
        model_type_objects = list(map(_graph.element_from_link, model_types))
        rows_divider = partial(
            cls.divide_table,
            ('size', 'scan_metric', 'value',),
            ('model_metric', 'f1', 'shift', 'f2',),
        )
        table = etl.fromcsv(
            cls.create_temp_file(data).name,
            delimiter=',',
        ).setheader(
            header=str_columns + float_columns,
        ).convert(
            str_columns,
            'strip'
        ).convert(
            'scan_metric',
            partial(_scanMetricRep.get_by_name_and_scanner_model, scanner_model),
        ).convert(
            'model_metric',
            partial(cls.get_model_type_metrics, model_types),
        ).unpack(
            field='model_metric',
            newfields=['model_metric_l', 'model_metric_r'],
        ).convert(
            'size',
            partial(_sizeRep.get_model_types_size, model_type_objects),
        )
        constraints = list(map(
            lambda field: dict(
                name=f'{field} is not found',
                field=field,
                assertion=partial(functoolz.flip, operator.is_not, None)
            ),
            table.fieldnames()
        ))
        validation_table = table.validate(
            constraints=constraints,
            header=table.fieldnames(),
        )
        if validation_table.nrows() > 0:
            return dict(
                metrics=None,
                success=False,
                errors=validation_table
            )
        result_table = etl.stack(rows_divider(table, '_l'), rows_divider(table, '_r')).skip(1)

        return dict(metrics=result_table, success=True, errors=etl.empty())
