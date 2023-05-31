import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import '../assets/css/mlhome.css';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import { Layout, List, Card, Button, Row, Col } from 'antd';
import * as actions from '../../store/actions/auth';
import axios from 'axios';

import LoginForm from '../../registration/components/LoginForm';
// import { coursetitle, courseapi } from '../components/courseinfo';
import courseObj from '../../url/courseObj';
import { LoadingOutlined } from '@ant-design/icons';

const { Header, Footer } = Layout;

const MLHome = (props) => {
    const [setWidth, setSetWidth] = useState(false);
    const [content, setContent] = useState([]);
    const [topImageCnt, setTopImageCnt] = useState();
    const [loaded, setLoaded] = useState(false);
    const [loaded2, setLoaded2] = useState(false);
    const [auth, setAuth] = useState(false);
    const [coursetitle, setCourseTitle] = useState();
    const [courseapi, setCourseApi] = useState();
    // const courseObj = {
    //     'physics11': 'Physics 11',
    //     'machinelearning': 'Machine Learning',
    // };
    const windowHeight = window.innerHeight - window.innerWidth * 90 / 1920 - 120;//45 - 45 - 24;

    useEffect(() => {
        if (window.innerWidth < 576) {
            setSetWidth(true);
        } else {
            setSetWidth(false);
        };

        var courseTitle;
        var courseAPI;
        for (const [key, value] of Object.entries(courseObj)) {
            if (key === props.match.params.subject) {
                courseTitle = value;
                courseAPI = key;
                setCourseTitle(value);
                setCourseApi(key);
            };
        };

        axios.get(`/courses/api/list/`)
            .then(res => {
                for (var i in res.data) {
                    if (res.data[i].subject === courseTitle) {
                        setTopImageCnt(res.data[i]);
                        setLoaded2(true);
                    };
                };
            });

        if (props.token !== null) {
            if (props.course !== null && props.course.includes(courseTitle)) {
                setAuth(true);
            };
            axios.get(`/${courseAPI}/api/list/`)
                .then(res => {
                    setContent(res.data);
                    setLoaded(true);
                });
        };
    }, [props.match.params.subject, props.match.params.chapter, props.match.params.section, props.token, props.course]);

    var d = new Date();
    var y = d.getFullYear();

    const history = useHistory();

    function handleUrl1() {
        history.push(`/courses/${courseapi}`);
    };

    function handleUrl2(chapter) {
        history.push(`/courses/${courseapi}/${chapter}`.replace(/\s/g, '').toLowerCase());
    };

    const handleLogout = () => {
        props.logout();
    };

    const handleHome = () => {
        window.location.href = "/";
    };

    return (
        <div>
            <Layout>
                <div className="head-image" onClick={() => { handleUrl1() }} >
                    {loaded2 && <img src={topImageCnt.top_image} style={{ width: "100%" }} alt="" />}
                </div>
                <Header className="physics11-header text-center">
                    {setWidth ? <h4>Welcome to {coursetitle}</h4> : <h1>Welcome to {coursetitle}</h1>}
                </Header>
                {/* <Layout style={setWidth ? { margin: "20px 0", minHeight: windowHeight } : { margin: "20px 0", mineight: "758px" }}> */}
                <Layout style={{ marginTop: "20px", minHeight: windowHeight }}>
                    {props.token ?
                        loaded ?
                            <div style={{ margin: "0 20%" }}>
                                {auth ?
                                    <div>
                                        <List
                                            grid={{
                                                gutter: 16,
                                                xs: 1,
                                                sm: 2,
                                                md: 2,
                                                lg: 4,
                                                xl: 6,
                                                xxl: 4,
                                            }}
                                            dataSource={content}
                                            renderItem={item => (
                                                <List.Item>
                                                    <Card
                                                        hoverable
                                                        cover={loaded && <img src={item.cover} style={{ width: "100%", height: "200px", borderBottom: "1px solid" }} alt="" />}
                                                        style={{ border: "1px solid" }}
                                                        onClick={() => handleUrl2(item.chapter)}
                                                    >
                                                        <span style={{ fontWeight: "500", fontSize: "1rem" }}>{item.chapter}</span>
                                                    </Card>
                                                </List.Item>
                                            )}
                                        />
                                        <div style={{ textAlign: "center", marginTop: "20px" }}>
                                            <Button type="primary" onClick={handleLogout}>Logout</Button>
                                        </div>
                                    </div>
                                    :
                                    <div style={{ width: "400px", margin: "20px auto 0" }}>
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
                                }
                            </div>
                            :
                            <div className="text-center">
                                <LoadingOutlined />
                            </div>
                        :
                        <div style={{ width: "400px", margin: "0 auto" }}>
                            <p style={{ textAlign: 'center' }}>Please sign in to view the content</p>
                            <LoginForm />
                        </div>
                    }
                </Layout>
                <Footer className="e3s-footer">Copyright © E3 Studio {y}</Footer>
            </Layout>
        </div>
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

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(MLHome));

