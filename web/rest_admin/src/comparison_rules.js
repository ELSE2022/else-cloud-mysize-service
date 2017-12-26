import React from 'react';
import { List, Edit, Create, Datagrid, ReferenceArrayInput, SelectArrayInput, ReferenceArrayField, SingleFieldList, ChipField, TextField, ReferenceInput, EditButton, SelectInput, ReferenceField, DisabledInput, SimpleForm, TextInput } from 'admin-on-rest';

export const ComparisonRulesList = (props) => (
    <List {...props} title="List of comparison rules" perPage={10}>
        <Datagrid>
            <TextField source="id" />
            <ReferenceArrayField label="Model type"  source="model_types" reference="modeltypes">
                <SingleFieldList>
                    <ChipField source="name" />
                </SingleFieldList>
            </ReferenceArrayField>
            <ReferenceField label="Scanner model" source="scanner_model" reference="scannermodels">
                <TextField source="name" />
            </ReferenceField>
            <TextField source="name" />
            <EditButton />
        </Datagrid>
    </List>
);

const ComparisonRuleTitle = ({ record }) => {
    return <span>Comparison rule {record ? `"${record.name}"` : ''}</span>;
};

export const ComparisonRulesEdit = (props) => (
    <Edit title={<ComparisonRuleTitle />} {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <ReferenceArrayInput label="Model type" source="model_types" reference="modeltypes" allowEmpty validation={{ required: true }}>
                <SelectArrayInput optionText="name" />
            </ReferenceArrayInput>
            <ReferenceInput label="Scanner model" source="scanner_model" reference="scannermodels" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="name" />
        </SimpleForm>
    </Edit>
);

export const ComparisonRulesCreate = (props) => (
    <Create {...props}>
        <SimpleForm>
            <ReferenceArrayInput label="Model type" source="model_types" reference="modeltypes" allowEmpty validation={{ required: true }}>
                <SelectArrayInput optionText="name" optionValue="id" />
            </ReferenceArrayInput>
            <ReferenceInput label="Scanner model" source="scanner_model" reference="scannermodels" allowEmpty validation={{ required: true }}>
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="name" />
        </SimpleForm>
    </Create>
);
