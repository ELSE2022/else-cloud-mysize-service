import React from 'react';
import { List, Edit, Create, Datagrid, TextField, EditButton, DisabledInput, SimpleForm, TextInput } from 'admin-on-rest';

export const BrandList = (props) => (
    <List {...props}>
        <Datagrid>
            <TextField source="id"/>
            <TextField source="uuid" />
            <TextField source="name"/>
            <EditButton />
        </Datagrid>
    </List>
);

const BrandTitle = ({ record }) => {
    return <span>Brand {record ? `"${record.name}"` : ''}</span>;
};

export const BrandEdit = (props) => (
    <Edit title={<BrandTitle />} {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <TextInput source="uuid" />
            <TextInput source="name" />
        </SimpleForm>
    </Edit>
);

export const BrandCreate = (props) => (
    <Create {...props}>
        <SimpleForm>
            <TextInput source="uuid" />
            <TextInput source="name" />
        </SimpleForm>
    </Create>
);
