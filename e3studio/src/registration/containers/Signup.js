import React, { useState, useEffect, useRef } from 'react';
import CustomLayout from './Layout';
import { connect } from 'react-redux';
import { Form, Input, Row, Col, Button } from 'antd';
import { } from '@ant-design/icons';
import { LoadingOutlined } from '@ant-design/icons';
import { NavLink } from 'react-router-dom';
import * as actions from '../../store/actions/auth';
import axios from 'axios';



const RegistrationForm = (props) => {

    const [invalid, setInvalid] = useState(null);
    const [confirmDirty, setConfirmDirty] = useState(false);

    const handleSubmit = e => {
        e.preventDefault();
        props.form.validateFieldsAndScroll((err, values) => {
            if (!err) {
                // props.onEmailUsername(values.email, values.username);
                axios.post(`/user/registration/account-email-username-check/`, {
                    email: values.email,
                    username: values.username
                })
                    .then(res => {
                        props.onAuth(
                            res.data.username,
                            res.data.email,
                            values.password,
                            values.confirm
                        );
                    })
                    .catch(error => {
                        setInvalid(error.response.data.message)
                        // state.invalid = error.response.data.message;
                        console.log("state.invalid: ", invalid)
                        // forceUpdate();
                    })
            }
        });
    };

    const [timer, setTimer] = useState(20);

    const [prevtoken, setPrevtoken] = useState(props.token);

    const interval = useRef(null);
    useEffect(() => {
        if (window.location.href.includes("/signup")) {
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

    const handleLogout = e => {
        e.preventDefault();
        clearInterval(interval.current);
        setTimer(20);
        props.logout();
    };


    const handleConfirmBlur = e => {
        const { value } = e.target;
        setConfirmDirty(confirmDirty => confirmDirty || !!value);
    };

    const compareToFirstPassword = (rule, value, callback) => {
        const { form } = props;
        if (value && value !== form.getFieldValue('password')) {
            callback('Two passwords that you enter is inconsistent!');
        } else {
            callback();
        }
    };

    const validateToNextPassword = (rule, value, callback) => {
        const { form } = props;
        if (value && confirmDirty) {
            form.validateFields(['confirm'], { force: true });
        }
        callback();
    };


    let errorMessage = null;
    if (invalid) {
        errorMessage = (
            <p style={{ "color": "red" }}>{invalid}</p>
        );
    } else if (props.error) {
        if (props.error.length > 1) {
            errorMessage = <ul style={{ "color": "red" }}>{props.error.map(x => <li>{x}</li>)}</ul>;
        } else {
            errorMessage = (
                <p style={{ "color": "red" }}>{props.error}</p>
            )
        }
    }

    const { getFieldDecorator } = props.form;

    return (
        <CustomLayout>
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
                        <Form>

                        </Form>
                    }
                </div>
            }
        </CustomLayout>
    );

};

// const WrappedRegistrationForm = Form.create({ name: 'register' })(RegistrationForm);


const mapStateToProps = (state) => {
    return {
        loading: state.loading,
        error: state.error,
        token: state.token,
    }
};

const mapDispatchToProps = dispatch => {
    return {
        // onEmailUsername: (email, username) => dispatch(actions.authEmailUsername(email, username)),
        onAuth: (username, email, password1, password2) => dispatch(actions.authSignup(username, email, password1, password2))
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(RegistrationForm);

