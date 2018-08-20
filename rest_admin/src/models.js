import React from 'react';
import { List, Edit, Create, Datagrid, ReferenceInput, TextField, ReferenceField, EditButton, DisabledInput,
    SimpleForm, SelectInput, TextInput, FileInput, FileField } from 'admin-on-rest';
import UrlField from './components/UrlField'

export const ModelList = (props) => (
    <List {...props} title="List of Lasts">
        <Datagrid>
            <TextField source="id" />
            <TextField source="name" />
            <ReferenceField label="Model type" source="model_type" reference="modeltypes">
                <TextField source="name" />
            </ReferenceField>
            <ReferenceField label="Product" source="product" reference="products">
                <TextField source="uuid" />
            </ReferenceField>
            <ReferenceField label="Size" source="size" reference="sizes">
                <TextField source="string_value" />
            </ReferenceField>
            <TextField source="stl_path" />
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
            <TextInput source="name" allowEmpty validation={{ required: true }}/>
            <ReferenceInput label="Model type" source="model_type" reference="modeltypes" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <ReferenceInput label="Product" source="product" reference="products" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="uuid" />
            </ReferenceInput>
            <ReferenceInput label="Size" source="size" reference="sizes" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="string_value" />
            </ReferenceInput>
            <FileInput source="files" label="STL" accept=".stl" >
                <FileField source="stl_path" title="name" />
            </FileInput>
            <UrlField label="STL file" source="stl_path" defaultValue=""/>
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
                <SelectInput optionText="name" />
            </ReferenceInput>
            <ReferenceInput label="Size" source="size" reference="sizes" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="string_value" />
            </ReferenceInput>
            <FileInput source="files" label="STL" accept=".stl">
                <FileField source="stl_path" title="name" />
            </FileInput>
        </SimpleForm>
    </Create>
);
