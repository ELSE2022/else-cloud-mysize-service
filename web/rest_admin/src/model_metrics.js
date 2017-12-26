import React from 'react';
import { List, Edit, Create, Datagrid, ReferenceInput, SelectInput, ReferenceField, TextField, EditButton, DisabledInput, SimpleForm, TextInput } from 'admin-on-rest';

export const ModelMetricList = (props) => (
    <List {...props}>
        <Datagrid>
            <TextField source="id" />
            <ReferenceField label="Model type" source="model_type" reference="modeltypes">
                <TextField source="name" />
            </ReferenceField>
            <TextField source="name" />
            <EditButton />
        </Datagrid>
    </List>
);

const ModelMetricTitle = ({ record }) => {
    return <span>Scan metric {record ? `"${record.name}"` : ''}</span>;
};

export const ModelMetricEdit = (props) => (
    <Edit title={<ModelMetricTitle />} {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <ReferenceInput label="Model type" source="model_type" reference="modeltypes" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="name" />
        </SimpleForm>
    </Edit>
);

export const ModelMetricCreate = (props) => (
    <Create {...props}>
        <SimpleForm>
            <ReferenceInput label="Model type" source="model_type" reference="modeltypes" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="name" />
        </SimpleForm>
    </Create>
);
