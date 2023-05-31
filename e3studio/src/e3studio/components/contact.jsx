import React, { useState } from 'react';
import axios from 'axios';


import { Form, Input, Button } from 'antd';
// import TextArea from 'antd/lib/input/TextArea';

const { TextArea } = Input;

function Contact(props) {
    // constructor(props) {
    //     super(props);
    // }
    const formItemLayout = {
        labelCol: {
            xs: { span: 24 },
            sm: { span: 8 },
        },
        wrapperCol: {
            xs: { span: 24 },
            sm: { span: 16 },
        },
    };



    const [textlength, setTextlength] = useState(1000);
    const [overlength, setOverlength] = useState();
    const [errormsg, setErrormsg] = useState('');
    const [disablebutton, setDisablebutton] = useState(false);
    const [response, setResponse] = useState();

    function handleChange(e) {
        const max_num_char = 1000;
        setTextlength(max_num_char - e.target.value.length);
        if (max_num_char - e.target.value.length === 1000) {
            setErrormsg('Please leave a message.');
        } else if (e.target.value.length - max_num_char > 0) {
            setErrormsg('Message cannot be longer than 1000 characters.');
            setTextlength(0);
            setOverlength(e.target.value.length - max_num_char);
        } else {
            setOverlength();
        };
    };

    function handleSubmit(e) {
        e.preventDefault();
        props.form.validateFields((err, values) => {
            if (!err) {
                setDisablebutton(true);
                axios.put(`/courses/api/message/`, {
                    name: values.name,
                    email: values.email,
                    message: values.message,
                }).then(res => {
                    setResponse(res.data);
                });
            };
        });
    };

    function handleResend() {
        setResponse();
        setDisablebutton(false);
    };

    return (
        <section id="contact" className="contact " ref={props.gref}>
            <div className="container">
                <div className="content-section-heading text-center">
                    <h3 className="mb-0" style={{ color: "#F22D30" }}>Like what you see?</h3>
                    <h2 className="mb-5">Contact Me</h2>
                </div>

                {!response ?
                    <div className="contact-form-box">
                        {/* <Form {...formItemLayout} onSubmit={handleSubmit}>
                            <Form.Item className="contact-form" label="Your Name">
                                {getFieldDecorator('name', {
                                    rules: [{ required: true, message: 'Please input your name.', whitespace: true }],
                                })(<Input style={{ fontWeight: "500" }} />)}
                            </Form.Item>

                            <Form.Item className="contact-form" label="Your E-mail">
                                {getFieldDecorator('email', {
                                    rules: [
                                        {
                                            type: 'email',
                                            message: 'The input is not valid E-mail!',
                                        },
                                        {
                                            required: true,
                                            message: 'Please input your E-mail!',
                                        },
                                    ],
                                })(<Input style={{ fontWeight: "500" }} />)}
                            </Form.Item>
                            <Form.Item className="contact-form" label="Your Message">
                                {getFieldDecorator('message', {
                                    rules: [{
                                        required: true,
                                        whitespace: true,
                                        max: 1000,
                                        message: `${errormsg}`
                                    }],
                                })(<TextArea style={{ fontSize: "18px", fontWeight: "500" }} onChange={handleChange} autoSize={{ minRows: 10 }} />)}
                            </Form.Item>
                            <div className="text-center">
                                <p style={{ padding: "5px 15px", color: "#1890ff", fontSize: "16px" }}>
                                    Maximum characters left: {textlength}
                                    <br />
                                    {overlength && <span>Please delete {overlength} characters.</span>}
                                </p>
                            </div>
                            <div className="text-center">
                                <Button className="contact-send-button" type="primary ant-btn-lg" htmlType="submit" style={{ width: "200px" }} disabled={disablebutton}>
                                    Send
                                </Button>
                            </div>
                        </Form>
                     */}
                    </div>
                    :
                    <div style={{ height: "530px" }}>
                        <h5 style={{ textAlign: "center", color: "#30475e" }}>{response}</h5>
                        <br />

                        <div className="text-center">
                            <h2>Thank You</h2>
                            <span className="response service-icon rounded-circle mx-auto mb-3">
                                ❤❤❤
                            </span>
                            <Button type="primary ant-btn-lg" onClick={handleResend} style={{ width: "200px" }}>
                                Send Another One
                            </Button>
                        </div>
                    </div>
                }
            </div>


            {/* <iframe width="100%" height="100%" frameBorder="0" scrolling="no" marginHeight="0" marginWidth="0" src="https://maps.google.com/maps?f=q&amp;source=s_q&amp;hl=en&amp;geocode=&amp;q=Twitter,+Inc.,+Market+Street,+San+Francisco,+CA&amp;aq=0&amp;oq=twitter&amp;sll=28.659344,-81.187888&amp;sspn=0.128789,0.264187&amp;ie=UTF8&amp;hq=Twitter,+Inc.,+Market+Street,+San+Francisco,+CA&amp;t=m&amp;z=15&amp;iwloc=A&amp;output=embed"></iframe> */}
            <br />
            {/* <small>
                <a href="https://maps.google.com/maps?f=q&amp;source=embed&amp;hl=en&amp;geocode=&amp;q=Twitter,+Inc.,+Market+Street,+San+Francisco,+CA&amp;aq=0&amp;oq=twitter&amp;sll=28.659344,-81.187888&amp;sspn=0.128789,0.264187&amp;ie=UTF8&amp;hq=Twitter,+Inc.,+Market+Street,+San+Francisco,+CA&amp;t=m&amp;z=15&amp;iwloc=A"></a>
            </small> */}
        </section>
    );

}

// const WrappedContactForm = Form.create({ name: 'register' })(Contact);

export default Contact;