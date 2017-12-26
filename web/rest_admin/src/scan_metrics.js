import React from 'react';
import { List, Edit, Create, Datagrid, ReferenceInput, SelectInput, ReferenceField, TextField, EditButton, DisabledInput, SimpleForm, TextInput } from 'admin-on-rest';

export const ScanMetricList = (props) => (
    <List {...props}>
        <Datagrid>
            <TextField source="id" />
            <ReferenceField label="Scanner model" source="scanner_model" reference="scannermodels">
                <TextField source="name" />
            </ReferenceField>
            <TextField source="name" />
            <EditButton />
        </Datagrid>
    </List>
);

const ScanMetricTitle = ({ record }) => {
    return <span>Scan metric {record ? `"${record.name}"` : ''}</span>;
};

export const ScanMetricEdit = (props) => (
    <Edit title={<ScanMetricTitle />} {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <ReferenceInput label="Scanner model" source="scanner_model" reference="scannermodels" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="name" />
        </SimpleForm>
    </Edit>
);

export const ScanMetricCreate = (props) => (
    <Create {...props}>
        <SimpleForm>
            <ReferenceInput label="Scanner model" source="scanner_model" reference="scannermodels" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="name" />
        </SimpleForm>
    </Create>
);
