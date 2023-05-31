import React from 'react';
import { Form, Input, Button } from 'antd';
import { connect } from 'react-redux';
import axios from 'axios';



const CustomForm = (props) => {
    const handleFormSubmit = (event, requestType, articleID) => {
        const title = event.target.elements.title.value;
        const content = event.target.elements.content.value;
        axios.defaults.headers = {
            "Content-Type": "application/json",
            Authorization: this.props.token
        }
        switch (requestType) {
            case 'POST':
                return axios.post(`/api/`, {
                    title: title,
                    content: content,
                })
                    .then(res => console.log(res))
                    .catch(error => console.log(error));
            case 'PUT':
                return axios.put(`/api/${articleID}/`, {
                    title: title,
                    content: content,
                })
                    .then(res => console.log(res))
                    .catch(error => console.log(error));
        }
    };


    return (
        <div>
            <Form onSubmit={(event) => this.handleFormSubmit(
                event,
                this.props.requestType,
                this.props.articleID
            )}>
                <Form.Item label="Title" >
                    <Input name="title" placeholder="input placeholder" />
                </Form.Item>
                <Form.Item label="Content" >
                    <Input name="content" placeholder="input placeholder" />
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit">{this.props.btnText}</Button>
                </Form.Item>
            </Form>
        </div>
    );

}

const mapStateToProps = state => {
    return {
        token: state.token
    }
}

export default connect(mapStateToProps)(CustomForm);