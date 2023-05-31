import React from 'react';
import { NavLink } from 'react-router-dom';
import { Form, Input, Button, Row, Col } from 'antd';
import { connect } from 'react-redux';
import * as actions from '../../store/actions/auth';

const LoginForm = (props) => {

    const { getFieldDecorator } = props.form;

    const handleSubmit = e => {
        e.preventDefault();
        props.form.validateFields((err, values) => {
            if (!err) {
                props.onAuth(values.username, values.password);
            }
        });
    };

    let errorMessage = null;
    if (props.error) {
        if (props.error.non_field_errors) {
            errorMessage = (
                <p style={{ "color": "red" }}>{props.error.non_field_errors}</p>
            );
        };
    };

    return (
        <Form></Form>
        // <Form onSubmit={handleSubmit} className="login-form">
        //     <h1 style={{ textAlign: 'center', padding: 24 }}> Account Login</h1>

        //     <Form.Item>
        //         {getFieldDecorator('username', {
        //             rules: [{ required: true, message: 'Please input your username!' }],
        //         })(
        //             <Input
        //                 prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
        //                 placeholder="Username" size="large"
        //             />,
        //         )}
        //     </Form.Item>

        //     <Form.Item>
        //         {getFieldDecorator('password', {
        //             rules: [{ required: true, message: 'Please input your Password!' }],
        //         })(
        //             <Input
        //                 prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
        //                 type="password" placeholder="Password" size="large"
        //             />,
        //         )}
        //     </Form.Item>

        //     {errorMessage}

        //     <Form.Item>
        //         <Row style={{ fontSize: "1rem" }}>
        //             <Button size="large" type="primary" htmlType="submit" style={{ marginRight: '10px' }}>
        //                 Login
        //             </Button>
        //             Or {' '}
        //             <NavLink
        //                 style={{ marginRight: '10px' }}
        //                 to='/registration/signup'>  Sign Up
        //             </NavLink>
        //             <br />
        //             <Col span={12}>
        //                 <NavLink
        //                     style={{ marginRight: '10px' }}
        //                     to='/registration/forgot_password'> Forgot Password?
        //                                             </NavLink>
        //             </Col>
        //             <Col span={12} style={{ textAlign: 'right' }}>
        //                 <NavLink
        //                     style={{ marginRight: '10px' }}
        //                     to='/'> Return Home
        //                                             </NavLink>
        //             </Col>
        //         </Row>
        //     </Form.Item>
        // </Form>

    )
}

// const WrappedLoginForm = Form.create({ name: 'login_form' })(LoginForm);

const mapStateToProps = (state) => {
    return {
        loading: state.loading,
        error: state.error,
        token: state.token,
    }
};

const mapDispatchToProps = dispatch => {
    return {
        onAuth: (username, password) => dispatch(actions.authLogin(username, password)),
        logout: () => dispatch(actions.authLogout())
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(LoginForm);



