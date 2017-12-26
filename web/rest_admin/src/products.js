import React from 'react';
import { List, Edit, FileInput, FileField, Create, ReferenceInput, SelectInput, Datagrid, ReferenceField, TextField, EditButton, DisabledInput, LongTextInput, SimpleForm, TextInput } from 'admin-on-rest';
import ProductEditActions from './ProductEditActions'

export const ProductList = (props) => (
    <List {...props}>
        <Datagrid>
            <TextField source="id" />
            <TextField source="uuid" />
            <ReferenceField label="Brand" source="brand" reference="brands">
                <TextField source="name" />
            </ReferenceField>
            <ReferenceField label="Comparison rule" source="brand" reference="brands">
                <TextField source="name" />
            </ReferenceField>
            <TextField source="sku" />
            <EditButton />
        </Datagrid>
    </List>
);

const ProductTitle = ({ record }) => {
    return <span>Product {record ? `"${record.name}"` : ''}</span>;
};

export const ProductEdit = (props) => (
    <Edit title={<ProductTitle />} {...props} actions={<ProductEditActions />} >
        <SimpleForm>
            <DisabledInput source="id" />
            <TextInput source="uuid" />
            <ReferenceInput label="Brand" source="brand" reference="brands" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <ReferenceInput label="Comparison rule" source="default_comparison_rule" reference="comparisonrules" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="sku" />
            <LongTextInput source="name" />
            <FileInput source="files" label="Csv files" accept=".csv">
                <FileField source="csv_file" title="CSV" />
            </FileInput>
        </SimpleForm>
    </Edit>
);

export const ProductCreate = (props) => (
    <Create {...props}>
        <SimpleForm>
            <TextInput source="uuid" />
            <ReferenceInput label="Brand" source="brand" reference="brands" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <ReferenceInput label="Comparison rule" source="default_comparison_rule" reference="comparisonrules" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="sku" />
            <TextInput source="name" />
        </SimpleForm>
    </Create>
);
