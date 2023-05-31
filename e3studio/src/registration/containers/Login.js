import React, { useState, useEffect, useRef } from 'react';
import CustomLayout from './Layout';
import { connect } from 'react-redux';
import { Form, Input, Button, Row, Col } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';

import { NavLink } from 'react-router-dom';
// import { Link, withRouter } from 'react-router-dom';
import * as actions from '../../store/actions/auth';
// import axios from 'axios';
// import CustomForm from '../components/Form';

const NormalLoginForm = (props) => {

    const [timer, setTimer] = useState(20);

    const [prevtoken, setPrevtoken] = useState(props.token);

    const interval = useRef(null);
    useEffect(() => {
        if (window.location.href.includes("/login")) {
            if (props.token !== prevtoken && prevtoken === null) {
                setPrevtoken(props.token);
                var newtimer = timer;
                interval.current = setInterval(() => {
                    newtimer = newtimer - 1;
                    setTimer(timer => timer - 1);
                    if (newtimer < 1) {
                        clearInterval(interval.current);
                        window.location.href = "/";
                    }
                }, 1000);
            } else if (props.token !== prevtoken && props.token === null) {
                setPrevtoken(props.token);
                clearInterval(interval.current);
            };
        };
    }, [props.token, prevtoken, timer]);

    const handleSubmit = e => {
        e.preventDefault();
        props.form.validateFields((err, values) => {
            if (!err) {
                props.onAuth(values.username, values.password);
            }
        });
    };

    const handleLogout = e => {
        e.preventDefault();
        clearInterval(interval.current);
        setTimer(20);
        props.logout();
    };

    let errorMessage = null;
    if (props.error) {
        if (props.error.non_field_errors) {
            errorMessage = (
                <p style={{ "color": "red" }}>{props.error.non_field_errors}</p>
            );
        };
    };

    const { getFieldDecorator } = props.form;

    return (
        <CustomLayout >
            {props.token ?
                <div>
                    <h1 style={{ textAlign: 'center', padding: 24 }}>
                        You're logged in!
                        </h1>
                    <p style={{ textAlign: 'center' }}> Redirecting to Home Page in <span style={{ "color": "#fe6845" }}>{timer}</span> seconds.</p>
                    <Row>
                        <Col span={12}>
                            <Button onClick={handleLogout} type="primary">
                                Logout
                            </Button>
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
                        //                 </Button>
                        //                 Or
                        //                 <NavLink
                        //                 style={{ marginRight: '10px' }}
                        //                 to='/registration/signup'> Sign Up
                        //                 </NavLink>
                        //             <br />
                        //             <Col span={12}>
                        //                 <NavLink
                        //                     style={{ marginRight: '10px' }}
                        //                     to='/registration/forgot_password'> Forgot Password?
                        //                     </NavLink>
                        //             </Col>
                        //             <Col span={12} style={{ textAlign: 'right' }}>
                        //                 <NavLink
                        //                     style={{ marginRight: '10px' }}
                        //                     to='/'> Return Home
                        //                     </NavLink>
                        //             </Col>
                        //         </Row>
                        //     </Form.Item>
                        // </Form>

                    }
                </div>
            }
        </CustomLayout>

    );

}

// const WrappedNormalLoginForm = Form.create({ name: 'normal_login' })(NormalLoginForm);

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

export default connect(mapStateToProps, mapDispatchToProps)(NormalLoginForm);
