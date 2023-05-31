import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import '../assets/css/p11home.css';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import { Layout, List, Card, Button, Row, Col } from 'antd';
import * as actions from '../../store/actions/auth';
import axios from 'axios';

import LoginForm from '../../registration/components/LoginForm';
import { coursetitle, courseapi } from '../components/courseinfo';

const { Header, Footer } = Layout;

const P11Home = (props) => {
    const [content, setContent] = useState([]);
    const [topImageCnt, setTopImageCnt] = useState();
    const [loaded, setLoaded] = useState(false);
    const [loaded2, setLoaded2] = useState(false);
    const [auth, setAuth] = useState(false);

    useEffect(() => {
        axios.get(`/courses/api/list/`)
            .then(res => {
                for (var i in res.data) {
                    if (res.data[i].subject === coursetitle) {
                        setTopImageCnt(res.data[i]);
                        setLoaded2(true);
                    };
                };
            });

        if (props.token !== null) {
            if (props.course !== null && props.course.includes(coursetitle)) {
                setAuth(true);
            };
            axios.get(`/${courseapi}/api/list/`)
                .then(res => {
                    setContent(res.data);
                    setLoaded(true);
                });
        };
    }, [props.token, props.course]);

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
                    <h1>Welcome to {coursetitle}</h1>
                </Header>
                <Layout style={{ marginTop: "20px", minHeight: "633px" }}>
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
                                                md: 4,
                                                lg: 4,
                                                xl: 6,
                                                xxl: 4,
                                            }}
                                            dataSource={content}
                                            renderItem={item => (
                                                <List.Item>
                                                    <Card
                                                        hoverable
                                                        cover={loaded && <img src={item.image} style={{ width: "100%", height: "200px", borderBottom: "1px solid" }} alt="" />}
                                                        style={{ border: "1px solid" }}
                                                        onClick={() => handleUrl2(item.chapter)}
                                                    >
                                                        <span style={{ fontWeight: "500", fontSize: "1rem" }}>Chapter {item.id}: {item.chapter}</span>
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
                                <Icon type="loading" style={{ color: "blue" }} />
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

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(P11Home));

