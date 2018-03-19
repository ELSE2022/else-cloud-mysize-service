import React from 'react';
import Dashboard from './Dashboard';
import authClient from './authClient';
import { Admin, Resource, Delete } from 'admin-on-rest';
import ApiRestClient from './restClient';
import { ProductList, ProductCreate, ProductEdit } from './products';
import { BrandList, BrandCreate, BrandEdit } from './brands';
import { UserList, UserCreate, UserEdit } from './users';
import { ModelTypeList, ModelTypeCreate, ModelTypeEdit } from './model_types';
import { SizeList, SizeCreate, SizeEdit } from './sizes';
import { ModelList, ModelCreate, ModelEdit } from './models';
import { BenchmarkList, BenchmarkCreate, BenchmarkEdit } from './benchmarks';
import { ScannerModelList, ScannerModelCreate, ScannerModelEdit } from './scanner_models';
import { ScannerList, ScannerCreate, ScannerEdit } from './scanners';
import { ScanList, ScanCreate, ScanEdit } from './scans';
import { ScanMetricList, ScanMetricEdit, ScanMetricCreate } from './scan_metrics';
import { ModelMetricList, ModelMetricEdit, ModelMetricCreate } from './model_metrics';
import { ComparisonResultsList } from './comparison_results';
import { ComparisonRuleMetricList } from './comparison_rule_metric';
import { ModelMetricValueList } from './model_metric_value';
import { ComparisonRulesList, ComparisonRulesCreate, ComparisonRulesEdit } from './comparison_rules';
import addUploadFeature from './addUploadFeature';
// import addUploadFile from './addUploadFile';

const restClient = ApiRestClient;
const uploadCapableClient = addUploadFeature(restClient);

const App = () => (
    <Admin authClient={authClient} dashboard={Dashboard} restClient={uploadCapableClient}>
        <Resource name="products" list={ProductList} edit={ProductEdit} create={ProductCreate} />
        <Resource name="brands" options={{ label: 'Brands' }} list={BrandList} edit={BrandEdit} create={BrandCreate} />
        <Resource name="comparisonrules" options={{ label: 'Comparison rule' }} list={ComparisonRulesList} edit={ComparisonRulesEdit} create={ComparisonRulesCreate} />
        <Resource name="users" options={{ label: 'Users' }} list={UserList} edit={UserEdit} create={UserCreate} />
        <Resource name="modeltypes" options={{ label: 'Model types' }} list={ModelTypeList} edit={ModelTypeEdit} create={ModelTypeCreate} remove={Delete}/>
        <Resource name="sizes" options={{ label: 'Sizes' }} list={SizeList} edit={SizeEdit} create={SizeCreate} remove={Delete}/>
        <Resource name="models" options={{ label: 'Models' }} list={ModelList} edit={ModelEdit} create={ModelCreate} remove={Delete}/>
        <Resource name="modelmetrics" options={{ label: 'Model metrics' }} list={ModelMetricList} edit={ModelMetricEdit} create={ModelMetricCreate} remove={Delete}/>
        <Resource name="modelmetricvalues" options={{ label: 'Model metrics value' }} list={ModelMetricValueList} remove={Delete}/>
        <Resource name="scannermodels" options={{ label: 'Scanner models' }} list={ScannerModelList} edit={ScannerModelEdit} create={ScannerModelCreate} remove={Delete}/>
        <Resource name="scanners" options={{ label: 'Scanners' }} list={ScannerList} edit={ScannerEdit} create={ScannerCreate} remove={Delete}/>
        <Resource name="scans" options={{ label: 'Scans' }} list={ScanList} edit={ScanEdit} create={ScanCreate} remove={Delete}/>
        <Resource name="scanmetrics" options={{ label: 'Scan metrics' }} list={ScanMetricList} edit={ScanMetricEdit} create={ScanMetricCreate} remove={Delete}/>
        <Resource name="comparisonresults" options={{ label: 'Comparison results' }} list={ComparisonResultsList} remove={Delete}/>
        <Resource name="comparisonrulemetric" options={{ label: 'Comparison rule metric' }} list={ComparisonRuleMetricList} remove={Delete}/>
        <Resource name="benchmarks" options={{ label: 'Benchmarks' }} list={BenchmarkList} edit={BenchmarkEdit} create={BenchmarkCreate} remove={Delete}/>
    </Admin>
);

export default App;
