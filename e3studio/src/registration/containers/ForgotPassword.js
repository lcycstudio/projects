import React, { useState } from 'react';
import CustomLayout from './Layout';
import { connect } from 'react-redux';
import axios from "axios";
import { Form, Input, Button, Row, Col, } from 'antd';
import { NavLink } from 'react-router-dom';

import { LoadingOutlined } from '@ant-design/icons';

const ForgotPasswordForm = (props) => {

    const [sent, setSent] = useState(null);

    const handleSubmit = event => {
        event.preventDefault();
        props.form.validateFieldsAndScroll((err, values) => {
            if (!err) {
                axios.post(`/rest-auth/password/reset/`, {
                    email: values.email,
                })
                    .then(res => {
                        setSent(res.data.detail);
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        });
    };

    let errorMessage = null;

    const { getFieldDecorator } = props.form;

    return (
        <CustomLayout>
            {sent ?
                <div>
                    <h1 style={{ textAlign: 'center', padding: 24 }}> Reset Password </h1>
                    <p style={{ fontSize: "1rem" }}>{sent} Please check your email box. </p>
                    <Row>
                        <Col span={12}>
                            <NavLink
                                style={{ marginRight: '10px' }}
                                to='/registration/login'> Login
                            </NavLink>
                        </Col>
                        <Col span={12} style={{ textAlign: 'right' }}>
                            <NavLink
                                style={{ marginRight: '10px' }}
                                to='/'> Return Home
                            </NavLink>
                        </Col>
                    </Row>
                </div>
                :
                <div>
                    {props.loading ?
                        <LoadingOutlined />
                        :
                        <Form></Form>
                        // <Form onSubmit={handleSubmit}>
                        //     <h1 style={{ textAlign: 'center', padding: 24 }}> Reset Password </h1>
                        //     <p style={{ fontSize: "1rem" }}>Please enter the email address associated with your account.</p>
                        //     <Form.Item>
                        //         {getFieldDecorator('email', {
                        //             rules: [
                        //                 {
                        //                     type: 'email',
                        //                     message: 'The input is not a valid E-mail!',
                        //                 },
                        //                 {
                        //                     required: true,
                        //                     message: 'Please input your E-mail!',
                        //                 },
                        //             ],
                        //         })(<Input
                        //             prefix={<Icon type="mail" style={{ color: 'rgba(0,0,0,.25)' }} />}
                        //             placeholder="Email" size="large"
                        //         />)}
                        //     </Form.Item>

                        //     {errorMessage}

                        //     <Form.Item>
                        //         <Row style={{ fontSize: "1rem" }}>
                        //             <Col span={12}>
                        //                 <Button size="large" type="primary" htmlType="submit" style={{ marginRight: '10px' }}>
                        //                     Submit
                        //     </Button>
                        //     Or
                        //     <NavLink
                        //                     style={{ marginRight: '10px' }}
                        //                     to='/registration/signup'> Sign Up
                        //     </NavLink>
                        //                 <br />
                        //             </Col>
                        //             <Col span={12} style={{ textAlign: 'right' }}>
                        //                 <NavLink
                        //                     style={{ marginRight: '10px' }}
                        //                     to='/'> Return Home
                        //     </NavLink>
                        //             </Col>
                        //         </Row>
                        //     </Form.Item>
                        // </Form>

                    }
                </div>
            }
        </CustomLayout>
    )

};

// const WrappedForgotPasswordForm = Form.create({ name: 'forgot_password' })(ForgotPasswordForm);

const mapStateToProps = (state) => {
    return {
        loading: state.loading,
        error: state.error,
        token: state.token,
    }
};

export default connect(mapStateToProps, null)(ForgotPasswordForm);
