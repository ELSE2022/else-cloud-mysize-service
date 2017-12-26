import React from 'react';
import { List, Edit, Create, Datagrid, ReferenceInput, TextField, ReferenceField, EditButton, DisabledInput,
    SimpleForm, SelectInput, TextInput } from 'admin-on-rest';

export const ModelList = (props) => (
    <List {...props}>
        <Datagrid>
            <TextField source="id" />
            <TextField source="name" />
            <ReferenceField label="Model type" source="model_type" reference="modeltypes">
                <TextField source="name" />
            </ReferenceField>
            <ReferenceField label="Product" source="product" reference="products">
                <TextField source="id" />
            </ReferenceField>
            <ReferenceField label="Size" source="size" reference="sizes">
                <TextField source="string_value" />
            </ReferenceField>
            <EditButton />
        </Datagrid>
    </List>
);

const ModelTitle = ({ record }) => {
    return <span>Model {record ? `"${record.name}"` : ''}</span>;
};

export const ModelEdit = (props) => (
    <Edit title={<ModelTitle />} {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <TextInput source="name" />
            <ReferenceInput label="Model type" source="model_type" reference="modeltypes" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <ReferenceInput label="Product" source="product" reference="products" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="id" />
            </ReferenceInput>
            <ReferenceInput label="Size" source="size" reference="sizes" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="string_value" />
            </ReferenceInput>
        </SimpleForm>
    </Edit>
);

export const ModelCreate = (props) => (
    <Create {...props}>
        <SimpleForm>
            <TextInput source="name" />
            <ReferenceInput label="Model type" source="model_type" reference="modeltypes" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <ReferenceInput label="Product" source="product" reference="products" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="id" />
            </ReferenceInput>
            <ReferenceInput label="Size" source="size" reference="sizes" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="string_value" />
            </ReferenceInput>
        </SimpleForm>
    </Create>
);
