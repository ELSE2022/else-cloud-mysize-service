import React from 'react';
import { List, Datagrid, TextField, ReferenceField } from 'admin-on-rest';

export const ModelMetricValueList = (props) => (
    <List {...props} >
        <Datagrid>
            <TextField source="id" />
            <ReferenceField label="Model" source="model" reference="models">
                <TextField source="name" />
            </ReferenceField>
            <ReferenceField label="Model metric" source="metric" reference="modelmetrics">
                <TextField source="name" />
            </ReferenceField>
            <TextField source="value" />
        </Datagrid>
    </List>
);
