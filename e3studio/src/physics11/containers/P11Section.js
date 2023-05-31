import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import '../assets/css/p11home.css';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import { Layout, Menu, Button, Row, Col } from 'antd';
import * as actions from '../../store/actions/auth';
import axios from 'axios';
import CourseLayout from './CourseLayout';

import LoginForm from '../../registration/components/LoginForm';
import { coursetitle, courseapi } from '../components/courseinfo';

const { Content, Sider } = Layout;

const P11Section = (props) => {
    const [content, setContent] = useState([]);
    const [secind, setSecind] = useState();
    const [loaded, setLoaded] = useState(false);
    const [auth, setAuth] = useState(false);

    useEffect(() => {
        if (props.token !== null) {
            if (props.course !== null && props.course.includes(coursetitle)) {
                setAuth(true);
            };
        };
        var thisUrl = props.thisurl;
        if (thisUrl !== null) {
            var sectionUrl = thisUrl.substring(0, thisUrl.length - 1);
            axios.get(`/${sectionUrl}`)
                .then(res => {
                    setContent(res.data);
                    setSecind(thisUrl.substr(-1));
                    setLoaded(true);
                });
        };
    }, [props.thisurl, props.token, props.course]);


    const history = useHistory();

    function handleUrl(chapter, section, index) {
        history.replace(`/courses/${courseapi}/${chapter}/${section}`.replace(/\s/g, '').toLowerCase());
        var element = document.getElementById("iSection");
        element.scrollIntoView();
    };

    const handleLogout = () => {
        props.logout();
    };

    function handleHome() {
        window.location.href = "/";
    };

    function handleCourses() {
        // window.location.href = "/courses";
        history.replace("/courses");
    };

    return (
        <CourseLayout>
            {props.token ?
                loaded ?
                    auth ?
                        <Sider width={200} style={{ background: '#fff' }}>
                            <Menu
                                mode="inline"
                                defaultSelectedKeys={[`${secind}`]}
                                selectedKeys={[`${secind}`]}
                                style={{ height: '100%', borderRight: 0 }}
                            >
                                <Menu.Item style={{ fontSize: "1rem", fontWeight: "700", pointerEvents: "none" }}>{content.chapter}</Menu.Item>
                                {content.sections && content.sections.map((each, index) => {
                                    return <Menu.Item key={index}
                                        onClick={() => handleUrl(content.chapter, content.sections[index], index)}
                                    >{content.id}.{index + 1} {each}</Menu.Item>
                                })}
                                <Menu.Item onClick={handleHome}>Home</Menu.Item>
                                <Menu.Item onClick={handleCourses}>Courses</Menu.Item>
                                <Menu.Item onClick={handleLogout}>Logout</Menu.Item>
                            </Menu>
                        </Sider>
                        :
                        <Sider width={0} style={{ background: '#F0F2F5' }} />
                    :
                    <Sider width={200} style={{ background: '#F0F2F5' }}>
                        <div className="text-center">
                            <Icon type="loading" style={{ color: "blue" }} />
                        </div>
                    </Sider>
                :
                <Sider width={200} style={{ background: '#F0F2F5' }} />
            }
            {props.token ?
                loaded ?
                    auth ?
                        <Layout style={{ margin: '0 24px 24px', height: "100%", backgroundColor: "white" }}>
                            {loaded &&
                                <Content
                                    className="section-content"
                                    style={{
                                        background: "white",
                                        padding: "0 24 24 24",
                                        margin: 0,
                                    }}
                                >
                                    {props.children}
                                </Content>
                            }
                        </Layout>
                        :
                        <div style={{ width: "400px", margin: "20px auto 0" }}>
                            <p style={{ textAlign: 'center' }}>You have not registered for this course.</p>
                            <p style={{ textAlign: 'center' }}>Please contact me for assistance.</p>
                            <Row>
                                <Col span={8}>
                                    <div style={{ textAlign: "center" }}>
                                        <Button type="primary" onClick={handleHome}>Home</Button>
                                    </div>
                                </Col>
                                <Col span={8}>
                                    <div style={{ textAlign: "center" }}>
                                        <Button type="primary" onClick={handleCourses}>Courses</Button>
                                    </div>
                                </Col>
                                <Col span={8}>
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
                <div style={{ width: "400px", marginLeft: "29%", marginRight: "auto" }}>
                    <p style={{ textAlign: 'center' }}>Please sign in to view the content</p>
                    <LoginForm />
                </div>
            }
        </CourseLayout>
    );
}

const mapStateToProps = (state) => {
    return {
        token: state.token,
        thisurl: state.thisurl,
        course: state.course,
    }
};

const mapDispatchToProps = dispatch => {
    return {
        logout: () => dispatch(actions.authLogout())
    }
};

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(P11Section));

