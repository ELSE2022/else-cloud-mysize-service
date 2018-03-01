import React from 'react';
import { List, Filter, Datagrid, ReferenceInput, SelectInput, TextField, EditButton, ReferenceField} from 'admin-on-rest';

const UserFilter = (props) => (
    <Filter {...props}>
        <ReferenceInput label="User" source="user_id" reference="users" allowEmpty>
            <SelectInput optionText="uuid" optionValue="uuid"/>
        </ReferenceInput>
    </Filter>
);

export const ComparisonResultsList = (props) => (
    <List {...props} filters={<UserFilter />}>
        <Datagrid>
            <TextField source="id" />
            <ReferenceField label="Model" source="model" reference="models">
                <TextField source="name" />
            </ReferenceField>
            <ReferenceField label="Scan" source="scan" reference="scans">
                <TextField source="name" />
            </ReferenceField>
            <ReferenceField label="Size" source="size" reference="sizes">
                <TextField source="string_value" />
            </ReferenceField>
            <TextField source="value" />
            <EditButton />
        </Datagrid>
    </List>
);
