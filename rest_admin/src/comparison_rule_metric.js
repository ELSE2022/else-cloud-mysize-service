import React from 'react';
import { List, Datagrid, TextField, ReferenceField } from 'admin-on-rest';

export const ComparisonRuleMetricList = (props) => (
    <List {...props} >
        <Datagrid>
            <TextField source="id" />
            <ReferenceField label="Comparison rule" source="rule" reference="comparisonrules">
                <TextField source="name" />
            </ReferenceField>
            <ReferenceField label="Model" source="model" reference="models">
                <TextField source="name" />
            </ReferenceField>
            <ReferenceField label="Model metric" source="model_metric" reference="modelmetrics">
                <TextField source="name" />
            </ReferenceField>
            <ReferenceField label="Scan metric" source="scan_metric" reference="scanmetrics">
                <TextField source="name" />
            </ReferenceField>
            <TextField source="f1" />
            <TextField source="shift" />
            <TextField source="f2" />
        </Datagrid>
    </List>
);
