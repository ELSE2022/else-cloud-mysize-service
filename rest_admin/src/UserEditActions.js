import React, {Component} from 'react';
import { CardActions } from 'material-ui/Card';
import { ListButton, DeleteButton} from 'admin-on-rest';
import GetStyleButton from './components/GetStyleButton';
import GetSizeButton from './components/GetSizeButton';
import {c} from './users';

const cardActionStyle = {
    zIndex: 2,
    display: 'inline-block',
    float: 'right',
};

class UserEditActions extends Component {
    constructor(props) {
        super(props);
        this.state = {
            productUuid: null
        };

        c.pushProduct = uuid => {
            this.setState({productUuid: uuid});
        };
    }
    render() {
        return <div>
            <CardActions style={cardActionStyle}>
                <GetSizeButton basePath={this.props.basePath} record={this.props.data} product={this.state.productUuid}/>
                <GetStyleButton basePath={this.props.basePath} record={this.props.data} product={this.state.productUuid}/>
                <ListButton basePath={this.props.basePath} />
                <DeleteButton basePath={this.props.basePath} record={this.props.data} />
            </CardActions>
        </div>;
    }
}

export default UserEditActions;
