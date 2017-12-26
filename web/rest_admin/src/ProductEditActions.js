import React from 'react';
import { CardActions } from 'material-ui/Card';
import { ListButton, DeleteButton } from 'admin-on-rest';
import GetCsvButton from './components/GetCsvButton';

const cardActionStyle = {
    zIndex: 2,
    display: 'inline-block',
    float: 'right',
};

const ProductEditActions = ({ basePath, data }) => (
    <CardActions style={cardActionStyle}>
        <GetCsvButton basePath={basePath} record={data} />
        <ListButton basePath={basePath} />
        <DeleteButton basePath={basePath} record={data} />
    </CardActions>
);

export default ProductEditActions;
