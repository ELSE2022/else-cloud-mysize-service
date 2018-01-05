import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import FlatButton from 'material-ui/FlatButton';
import { showNotification as showNotificationAction } from 'admin-on-rest';
import { push as pushAction } from 'react-router-redux';

class GetStyleButton extends Component {
    handleClick = () => {
        const { push, record, showNotification, product } = this.props;
        fetch(`http://127.0.0.1:5000/fitting/users/${record.uuid}/products/${product}/best_style`, { method: 'GET' })
            .then(() => {
                showNotification('Comparison...');
                push('/comparisonresults', 'filter={"user_id":"148254db-539d-4329-8450-184c9ac0a0ef"}');
            })
            .catch((e) => {
                console.error(e);
                showNotification('Error: comparison not finished', 'warning')
            });
    };

    render() {
        return <FlatButton label="Best style" style={{ color: 'green' }} onClick={this.handleClick} />;
    }
}

GetStyleButton.propTypes = {
    push: PropTypes.func,
    record: PropTypes.object,
    showNotification: PropTypes.func,
};

export default connect(null, {
    showNotification: showNotificationAction,
    push: pushAction,
})(GetStyleButton);
