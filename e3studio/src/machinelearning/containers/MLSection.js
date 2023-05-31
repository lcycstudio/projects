import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import '../assets/css/mlhome.css';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import { Layout, Menu, Button, Row, Col } from 'antd';
import * as actions from '../../store/actions/auth';
import axios from 'axios';
import CourseLayout from './CourseLayout';

import LoginForm from '../../registration/components/LoginForm';
// import { coursetitle, courseapi } from '../components/courseinfo';
import courseObj from '../../url/courseObj';
import { AppleOutlined, LoadingOutlined } from '@ant-design/icons';

const { Content, Sider } = Layout;
const { SubMenu } = Menu;

const MLSection = (props) => {
    // const [content, setContent] = useState([]);
    const [collapsedL, setCollapsedL] = useState(true);
    const [setWidth, setSetWidth] = useState(false);
    const [content, setContent] = useState([]);
    // const [secind, setSecind] = useState();
    const [loaded, setLoaded] = useState(false);
    const [auth, setAuth] = useState(false);
    // const [coursetitle, setCourseTitle] = useState();
    const [courseapi, setCourseApi] = useState();



    var toggleSiderLeft = () => {
        setCollapsedL(!collapsedL);
    };

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
                // setCourseTitle(value);
                setCourseApi(key);
            };
        };

        if (props.token !== null) {
            if (props.course !== null && props.course.includes(courseTitle)) {
                setAuth(true);
            };
        };

        axios.get(`/${courseAPI}/api/list/`)
            .then(res => {
                setContent(res.data);
                setLoaded(true);
            });

    }, [props.match.params.subject, props.thisurl, props.token, props.course]);


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

    return (
        <CourseLayout>
            {props.token ?
                loaded ?
                    auth ?
                        <Sider
                            id="ml-sider"
                            width="250"
                            theme="light"
                            collapsible
                            collapsed={collapsedL}
                            onCollapse={toggleSiderLeft}
                            defaultCollapsed={true}
                            breakpoint={setWidth ? "xs" : 'none'}
                            collapsedWidth={setWidth ? "0" : '80'}
                            trigger={setWidth && null}
                            style={{
                                overflow: 'auto',
                                // height: '100vh',
                                left: 0,
                            }}
                        >
                            <Menu theme="light" defaultSelectedKeys={['1']} mode="inline">
                                {content && content.map((each, index0) => {
                                    return each.sections.length !== 0 ?
                                        <SubMenu key={`chapter${index0}`}
                                            title={<span>
                                                {each.icon ?
                                                    <AppleOutlined />
                                                    :
                                                    <AppleOutlined />
                                                }
                                                <span>{each.chapter}</span>
                                            </span>}
                                        >
                                            {each.sections && each.sections.map((section, index1) => {
                                                return <Menu.Item
                                                    key={`section${index0}${index1}`}
                                                    onClick={() => handleUrl(each.chapter, section, index1)}
                                                >
                                                    {section}
                                                </Menu.Item>
                                            })}
                                        </SubMenu>
                                        :
                                        <Menu.Item key={`chapter${index0}`}>
                                            {each.icon ?
                                                <AppleOutlined />
                                                :
                                                <AppleOutlined />
                                            }
                                            <span>{each.chapter}</span>
                                        </Menu.Item>
                                })}
                                <Menu.Item onClick={handleHome}>
                                    <AppleOutlined />
                                    <span>Home</span>
                                </Menu.Item>
                                <Menu.Item onClick={handleLogout}>
                                    <AppleOutlined />
                                    <span>Logout </span>
                                </Menu.Item>
                            </Menu>
                        </Sider>
                        :
                        <Sider width={0} style={{ background: '#F0F2F5' }} />
                    :
                    <Sider width={200} style={{ background: '#F0F2F5' }}>
                        <div className="text-center">
                            <AppleOutlined />
                        </div>
                    </Sider>
                :
                <Sider width={200} style={{ background: '#F0F2F5' }} />
            }
            {props.token ?
                loaded ?
                    auth ?
                        <Layout style={setWidth ? { margin: '0 12px', backgroundColor: "white" } : { margin: '0 24px', backgroundColor: "white" }}>
                            {loaded &&
                                <Content
                                    className="section-content"
                                    style={{
                                        background: "white",
                                        padding: "0 24 24 24",
                                        margin: 0,
                                    }}
                                >
                                    {setWidth &&
                                        <AppleOutlined />
                                        // <Icon
                                        //     style={{ position: "absolute", marginTop: "8px", marginLeft: "2px" }}
                                        //     id="left-trigger"
                                        //     type={collapsedL ? 'right-square' : 'left-square'}
                                        //     theme="filled"
                                        //     onClick={toggleSiderLeft}
                                        // />
                                    }
                                    {props.children}
                                </Content>
                            }
                        </Layout>
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
                    :
                    <div className="text-center">
                        <LoadingOutlined />
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

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(MLSection));
