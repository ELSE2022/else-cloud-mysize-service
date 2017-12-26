import React from 'react';
import { List, Edit, Create, Datagrid, ReferenceInput, SelectInput, BooleanInput, DateInput, BooleanField, DateField,
    ReferenceField, TextField, NumberInput, NumberField, EditButton, DisabledInput, SimpleForm, TextInput } from 'admin-on-rest';

export const ScanList = (props) => (
    <List {...props}>
        <Datagrid>
            <TextField source="id" />
            <ReferenceField label="User" source="user" reference="users">
                <TextField source="uuid" />
            </ReferenceField>
            <ReferenceField label="Scanner" source="scanner" reference="scanners">
                <TextField source="name" />
            </ReferenceField>
            <ReferenceField label="Model type" source="model_type" reference="modeltypes">
                <TextField source="name" />
            </ReferenceField>
            <BooleanField source="is_default" />
            <DateField source="creation_time" showTime />
            <TextField source="scan_id" />
            <NumberField source="num_id" />
            <TextField source="name" />
            <TextField source="sex" />
            <TextField source="stl_path" />
            <TextField source="img_path" />
            <EditButton />
        </Datagrid>
    </List>
);

const ScanTitle = ({ record }) => {
    return <span>Scan {record ? `"${record.name}"` : ''}</span>;
};

export const ScanEdit = (props) => (
    <Edit title={<ScanTitle />} {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <ReferenceInput label="User" source="user" reference="users" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="uuid" />
            </ReferenceInput>
            <ReferenceInput label="Scanner" source="scanner" reference="scanners" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <ReferenceInput label="Model type" source="model_type" reference="modeltypes" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <BooleanInput label="Is Default?" source="is_default" />
            <DateInput source="creation_time" />
            <TextInput source="scan_id" />
            <NumberInput source="num_id" />
            <TextInput source="name" />
            <TextInput source="sex" />
            <TextInput source="stl_path" />
            <TextInput source="img_path" />
        </SimpleForm>
    </Edit>
);

export const ScanCreate = (props) => (
    <Create {...props}>
        <SimpleForm>
            <ReferenceInput label="User" source="user" reference="users" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="uuid" />
            </ReferenceInput>
            <ReferenceInput label="Scanner" source="scanner" reference="scanners" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <ReferenceInput label="Model type" source="model_type" reference="modeltypes" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <BooleanInput label="Is Default?" source="is_default" />
            <DateInput source="creation_time" />
            <TextInput source="scan_id" />
            <NumberInput source="num_id" />
            <TextInput source="name" />
            <TextInput source="sex" />
            <TextInput source="stl_path" />
            <TextInput source="img_path" />
        </SimpleForm>
    </Create>
);
