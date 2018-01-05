import React from 'react';
import { List, Edit, Create, Datagrid, TextField, ReferenceInput, EditButton, SelectInput, ReferenceField, DisabledInput, SimpleForm, TextInput } from 'admin-on-rest';

export const ScannerList = (props) => (
    <List {...props}>
        <Datagrid>
            <TextField source="id" />
            <ReferenceField label="Scanner model" source="model" reference="scannermodels">
                <TextField source="name" />
            </ReferenceField>
            <TextField source="name" />
            <EditButton />
        </Datagrid>
    </List>
);

const ScannerTitle = ({ record }) => {
    return <span>Scanner {record ? `"${record.name}"` : ''}</span>;
};

export const ScannerEdit = (props) => (
    <Edit title={<ScannerTitle />} {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <ReferenceInput label="Scanner model" source="model" reference="scannermodels" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="name" />
        </SimpleForm>
    </Edit>
);

export const ScannerCreate = (props) => (
    <Create {...props}>
        <SimpleForm>
            <ReferenceInput label="Scanner model" source="model" reference="scannermodels" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="name" />
        </SimpleForm>
    </Create>
);
