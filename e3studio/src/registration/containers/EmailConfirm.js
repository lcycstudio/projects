import React from 'react';
import axios from 'axios';
import { connect } from 'react-redux';
import CustomLayout from './Layout';


class EmailConfirm extends React.Component {

    state = {
        articles: []
    }

    componentWillReceiveProps(newProps) {
        if (newProps.token) {
            axios.defaults.headers = {
                "Content-Type": "application/json",
                Authorization: newProps.token
            }
            axios.get(`/registration/confirm-email/`)
                .then(res => {

                });
            this.forceUpdate();
        }
    }


    render() {
        return (
            <CustomLayout>
                <div>
                    {/* <Articles data={this.state.articles} /> */}
                    {/* <br /> */}
                    <h1 style={{ textAlign: 'center' }}> Account Email Confirmation</h1>
                    {/* <CustomForm 
                    requestType="POST"
                    articleID={null}
                    btnText="Create"/> */}
                </div>
            </CustomLayout>
        )
    }
}

const mapStateToProps = state => {
    return {
        token: state.token
    }
}

export default connect(mapStateToProps)(EmailConfirm);