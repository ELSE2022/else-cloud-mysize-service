import React from 'react';
import { List, Edit, Create, Datagrid, ReferenceInput, TextField, ReferenceField, EditButton, DisabledInput,
    SimpleForm, SelectInput } from 'admin-on-rest';

export const BenchmarkList = (props) => (
    <List {...props} title="List of Benchmarks">
        <Datagrid>
            <TextField source="id" />
            <ReferenceField label="Product" source="product" reference="products">
                <TextField source="uuid" />
            </ReferenceField>
            <ReferenceField label="Scan" source="scan" reference="scans">
                <TextField source="scan_id" />
            </ReferenceField>
            <ReferenceField label="Size" source="size" reference="sizes">
                <TextField source="string_value" />
            </ReferenceField>
            <ReferenceField label="User" source="user" reference="users">
                <TextField source="uuid" />
            </ReferenceField>
            <EditButton />
        </Datagrid>
    </List>
);

const BenchmarkTitle = ({ record }) => {
    return <span>Benchmark {record ? `"${record.id}"` : ''}</span>;
};

export const BenchmarkEdit = (props) => (
    <Edit title={<BenchmarkTitle />} {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <ReferenceInput label="Product" source="product" reference="products" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="uuid" />
            </ReferenceInput>
            <ReferenceInput label="Size" source="size" reference="sizes" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="string_value" />
            </ReferenceInput>
            <ReferenceInput label="User" source="user" reference="users" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="uuid" />
            </ReferenceInput>
            <ReferenceInput label="Scan" source="scan" reference="scans" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="scan_id" />
            </ReferenceInput>
        </SimpleForm>
    </Edit>
);

export const BenchmarkCreate = (props) => (
    <Create {...props}>
        <SimpleForm>
            <ReferenceInput label="Product" source="product" reference="products" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <ReferenceInput label="Size" source="size" reference="sizes" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="string_value" />
            </ReferenceInput>
            <ReferenceInput label="User" source="user" reference="users" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="uuid" />
            </ReferenceInput>
            <ReferenceInput label="Scan" source="scan" reference="scans" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="scan_id" />
            </ReferenceInput>
        </SimpleForm>
    </Create>
);
