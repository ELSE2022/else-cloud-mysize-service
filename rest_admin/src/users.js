import React from 'react';
import { List, Edit, Create, Datagrid, TextField, EditButton, SelectInput, ReferenceInput, DisabledInput, SimpleForm, TextInput } from 'admin-on-rest';
import UserEditActions from './UserEditActions'

export const UserList = (props) => (
    <List {...props} >
        <Datagrid>
            <TextField source="id" />
            <TextField source="uuid" />
            <TextField source="base_url" />
            <EditButton />
        </Datagrid>
    </List>
);

const UserTitle = ({ record }) => {
    return <span>User {record ? `"${record.uuid}"` : ''}</span>;
};

export const c = {
    pushProduct: () => {}
};

export const UserEdit = (props) => (
    <Edit title={<UserTitle />} {...props} actions={<UserEditActions />} >
        <SimpleForm>
            <DisabledInput source="id" />
            <TextInput source="uuid" />
            <TextInput source="base_url" />
            <ReferenceInput label="Product" onChange={(v, productUuid) => c.pushProduct(productUuid)} source="product_id" reference="products" allowEmpty>
                <SelectInput optionText="uuid" optionValue="uuid"/>
            </ReferenceInput>
        </SimpleForm>
    </Edit>
);

export const UserCreate = (props) => (
    <Create {...props}>
        <SimpleForm>
            <TextInput source="uuid" />
            <TextInput source="base_url" />
        </SimpleForm>
    </Create>
);
