import React from 'react';
import { List, Edit, Create, Datagrid, ReferenceArrayInput, SelectArrayInput, ReferenceArrayField, SingleFieldList, ChipField, TextField, EditButton, DisabledInput, SimpleForm, TextInput } from 'admin-on-rest';

export const SizeList = (props) => (
    <List {...props} perPage={10}>
        <Datagrid>
            <TextField source="id" sortable="False"/>
            <ReferenceArrayField label="Model type" reference="modeltypes" source="model_types">
                <SingleFieldList>
                    <ChipField source="name" />
                </SingleFieldList>
            </ReferenceArrayField>
            <TextField source="string_value" />
            <EditButton />
        </Datagrid>
    </List>
);

const SizeTitle = ({ record }) => {
    return <span>Size {record ? `"${record.string_value}"` : ''}</span>;
};

export const SizeEdit = (props) => (
    <Edit title={<SizeTitle />} {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <ReferenceArrayInput label="Model type" source="model_types" reference="modeltypes" allowEmpty validation={{ required: true }}>
                <SelectArrayInput optionText="name" />
            </ReferenceArrayInput>
            <TextInput source="string_value" />
        </SimpleForm>
    </Edit>
);

export const SizeCreate = (props) => (
    <Create {...props}>
        <SimpleForm>
            <ReferenceArrayInput label="Model type" source="model_types" reference="modeltypes" allowEmpty validation={{ required: true }}>
                <SelectArrayInput optionText="name" optionValue="id" />
            </ReferenceArrayInput>
            <TextInput source="string_value" />
        </SimpleForm>
    </Create>
);
