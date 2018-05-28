import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import FlatButton from 'material-ui/FlatButton';
import { showNotification as showNotificationAction } from 'admin-on-rest';
import { push as pushAction } from 'react-router-redux';

class GetCsvButton extends Component {
    handleClick = () => {
        console.log(this.props);
        const { record } = this.props;
        window.open(`/fitting/products/${record.uuid}/get_metrics`);
        // fetch(`/fitting/products/${record.uuid}/get_metrics`, { method: 'GET' })
        //     .then((response) => {
        //         showNotification('Download...');
        //         return response.blob();
        //     })
        //     .catch((e) => {
        //         console.error(e);
        //         showNotification('Error: download not finished', 'warning')
        //     });
    };

    render() {
        return <FlatButton label="Download .csv" style={{ color: 'green' }} onClick={this.handleClick} />;
    }
}

GetCsvButton.propTypes = {
    push: PropTypes.func,
    record: PropTypes.object,
    showNotification: PropTypes.func,
};

export default connect(null, {
    showNotification: showNotificationAction,
    push: pushAction,
})(GetCsvButton);
