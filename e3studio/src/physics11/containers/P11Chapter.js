import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import '../assets/css/p11home.css';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import { List, Button, Row, Col } from 'antd';
import * as actions from '../../store/actions/auth';
import axios from 'axios';
import CourseLayout from './CourseLayout';

import LoginForm from '../../registration/components/LoginForm';
import { coursetitle, courseapi } from '../components/courseinfo';


const P11Chapter = (props) => {
    const [content, setContent] = useState([]);
    const [loaded, setLoaded] = useState(false);
    const [auth, setAuth] = useState(false);

    useEffect(() => {
        if (props.token !== null) {
            if (props.course !== null && props.course.includes(coursetitle)) {
                setAuth(true);
            };
        };
        var chapter = props.match.params.chapter.replace(/\s/g, '').replace('%20', '').toLowerCase();
        axios.get(`/${courseapi}/api/list/`)
            .then(res1 => {
                var allchapter = res1.data;
                for (var i in allchapter) {
                    if (allchapter[i].chapter.replace(/\s/g, '').toLowerCase() === chapter) {
                        axios.get(`/${courseapi}/api/${allchapter[i].chapter}/`)
                            .then(res2 => {
                                setContent(res2.data);
                                setLoaded(true);
                            });
                    };
                };
            });
    }, [props.match.params.chapter, props.token, props.course]);

    const history = useHistory();

    function handleUrl2(chapter, section) {
        history.push(`/courses/${courseapi}/${chapter}/${section}`.replace(/\s/g, '').toLowerCase());
    };

    const handleLogout = () => {
        props.logout();
    };

    const handleHome = () => {
        window.location.href = "/";
    };

    return (
        <CourseLayout>
            <div style={{ margin: "0 20%" }}>
                {props.token ?
                    loaded ?
                        auth ?
                            <div>
                                <h3 style={{ textAlign: "center" }}>Chapter {content.id}: {content.chapter}</h3>
                                <div style={{ width: "500px", margin: "30px auto" }}>
                                    {content.sections.length === 0 ?
                                        <p style={{ textAlign: "center", marginTop: "80px" }}>Chapter content is not yet available.</p>
                                        :
                                        <List
                                            dataSource={content.sections}
                                            renderItem={(item, index) => (
                                                <List.Item>
                                                    <h6
                                                        className="section-item"
                                                        onClick={() => { handleUrl2(content.chapter, item) }}
                                                    >{content.id}.{index + 1} {item}</h6>
                                                </List.Item>
                                            )}
                                        />
                                    }
                                </div>
                            </div>
                            :
                            <div style={{ width: "400px", margin: "0 auto" }}>
                                <p style={{ textAlign: 'center' }}>You have not registered for this course.</p>
                                <p style={{ textAlign: 'center' }}>Please contact me for assistance.</p>
                                <Row>
                                    <Col span={12}>
                                        <div style={{ textAlign: "center" }}>
                                            <Button type="primary" onClick={handleHome}>Home</Button>
                                        </div>
                                    </Col>
                                    <Col span={12}>
                                        <div style={{ textAlign: "center" }}>
                                            <Button type="primary" onClick={handleLogout}>Logout</Button>
                                        </div>
                                    </Col>
                                </Row>
                            </div>
                        :
                        <div className="text-center">
                            <Icon type="loading" style={{ color: "blue" }} />
                        </div>
                    :
                    <div style={{ width: "400px", margin: "0 auto" }}>
                        <p style={{ textAlign: 'center' }}>Please sign in to view the content</p>
                        <LoginForm />
                    </div>
                }
            </div>
        </CourseLayout>
    );
}

const mapStateToProps = (state) => {
    return {
        token: state.token,
        course: state.course,
    }
};

const mapDispatchToProps = dispatch => {
    return {
        logout: () => dispatch(actions.authLogout())
    }
};

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(P11Chapter));

