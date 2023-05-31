import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
// import '../assets/css/p11home.css';
import { Layout, Menu, List } from 'antd';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import * as actions from '../../store/actions/auth';
import axios from 'axios';

const { SubMenu } = Menu;
const { Header } = Layout;

const ShowHeader = (props) => {
    const [content, setContent] = useState([]);
    const [secind, setSecind] = useState();
    const [loaded, setLoaded] = useState(false);
    const [auth, setAuth] = useState(false);

    useEffect(() => {
        if (props.token !== null) {
            if (props.course !== null && props.course.includes(props.coursetitle)) {
                setAuth(true);
            };
            axios.get(`${props.MainUrl}/${props.courseapi}/api/list/`)
                .then(res => {
                    setContent(res.data);
                    setLoaded(true);
                });
        };
    }, [props.token, props.course, props.MainUrl, props.courseapi, props.coursetitle]);

    const history = useHistory();

    function handleUrl1(chapter) {
        history.push(`/courses/${props.courseapi}/${chapter}`.replace(/\s/g, '').toLowerCase());
    };

    function handleUrl2(chapter, section, index) {
        // props.seturl(`courses/api/Physics 11/${chapter}/${index}`);
        // props.seturl(`${props.courseapi}/api/${chapter}/${index}`);
        setSecind(index);
        // let url = `/${props.courseapi}/${chapter}/${section}`.replace(/\s/g, '').toLowerCase();
        // history.replace(`/courses/${props.courseapi}/${chapter}/${section}`.replace(/\s/g, '').toLowerCase());
        if (window.location.href.includes(`/${chapter}/`.replace(/\s/g, '').toLowerCase())) {
            history.push(`/courses/${props.courseapi}/${chapter}/${section}`.replace(/\s/g, '').toLowerCase());
            var element = document.getElementById("iSection");
            element.scrollIntoView();
        } else {
            history.replace(`/courses/${props.courseapi}/${chapter}/${section}`.replace(/\s/g, '').toLowerCase());
        };
    };

    return (
        <Header className="physics11-header text-center">
            {props.token ?
                loaded ?
                    auth ?
                        <List
                            grid={{ gutter: 16, column: content.length }}
                            dataSource={content}
                            renderItem={item => (
                                <List.Item >
                                    <Menu
                                        mode="horizontal"
                                        defaultSelectedKeys={[`${secind}`]}
                                        selectedKeys={[`${secind}`]}
                                        style={{ lineHeight: '56px', borderBottom: "0" }}
                                    >
                                        <SubMenu
                                            title={<span onClick={() => handleUrl1(item.chapter)}
                                                style={{ fontSize: "1rem", fontWeight: "500" }}
                                            >{item.chapter}</span>}
                                        >
                                            {item.sections && item.sections.map((section, index) => {
                                                return <Menu.Item
                                                    key={index}
                                                    className="header-section-list"
                                                    onClick={() => handleUrl2(item.chapter, section, index)}
                                                >
                                                    <span className="header-section-text">{section}</span>
                                                </Menu.Item>
                                            })}
                                        </SubMenu>
                                    </Menu>
                                </List.Item>
                            )}
                        />
                        :
                        <div className="text-center">
                            <Icon type="loading" style={{ color: "blue" }} />
                        </div>
                    :
                    <h1>Welcome to Physics 11</h1>
                :
                <h1>Welcome to Physics 11</h1>
            }
        </Header>
    )
}

const mapStateToProps = (state) => {
    return {
        token: state.token,
        course: state.course
    }
};

const mapDispatchToProps = dispatch => {
    return {
        logout: () => dispatch(actions.authLogout()),
        seturl: (thisurl) => dispatch(actions.setUrl(thisurl))
    }
};

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ShowHeader));
