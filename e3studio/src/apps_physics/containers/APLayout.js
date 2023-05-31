import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import '../assets/css/appsPhysics.css';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import { AppleOutlined } from '@ant-design/icons';
import * as actions from '../../store/actions/auth';
import axios from 'axios';
// import ShowHeader from '../components/showheader';


import { appapi } from '../components/appinfo';

const { Header, Content, Footer, Sider } = Layout;
// const { SubMenu } = Menu;

const APLayout = (props) => {
    const [collapsedL, setCollapsedL] = useState(true);
    const [collapsedR, setCollapsedR] = useState(false);
    const [windowWidth, setWindowWidth] = useState(false);
    const [content, setContent] = useState([]);
    const [images, setImages] = useState();
    const [loaded, setLoaded] = useState(false);
    const [defaultKey, setDefaultKey] = useState();


    var toggleSiderLeft = () => {
        setCollapsedL(!collapsedL);
        var logo1 = document.getElementById("math-app-logo-1");
        if (!collapsedL) {
            logo1.style.clip = "rect(0 80px 200px 0)";
        } else {
            logo1.style.clip = "rect(0 200px 200px 0)";
        };
        var headerWidth = document.getElementById('math-app-header-div').offsetWidth;
        var headerImg = document.getElementById('math-app-header-image');
        if (!collapsedL && window.innerWidth < 576) {
            headerImg.style.clip = "rect(0 right 114px 0px)".replace("right", (headerWidth + 200).toString().concat("px"));
            headerImg.style.left = "0px"
        };
    };


    var onCollapseRight = collapsedrightbar => {
        setCollapsedR({ collapsedrightbar });
    };


    var setImageStyle = () => {
        var headerWidth = document.getElementById('math-app-header-div').offsetWidth;
        var headerImg = document.getElementById('math-app-header-image');
        headerImg.style.clip = "rect(0 right 114px 0px)".replace("right", headerWidth.toString().concat("px"));
        if (window.innerWidth < 576) {
            headerImg.style.clip = "rect(0 right 114px 25px)".replace("right", (headerWidth + 25).toString().concat("px"));
            headerImg.style.left = "-25px"
        };
        if (window.innerWidth <= 340) {
            headerImg.style.clip = "rect(0 right 114px 45px)".replace("right", (headerWidth + 45).toString().concat("px"));
            headerImg.style.left = "-45px"
        };
    };

    const history = useHistory();

    function handleUrl2(web) {
        history.push(`/apps/physics/${web}`);
    };

    function handleHome() {
        history.push('/');
    };

    function handleApps() {
        history.push('/apps');
    };

    useEffect(() => {
        if (window.innerWidth < 576) {
            setWindowWidth(true);
        } else {
            setWindowWidth(false);
        };

        axios.get(`/${appapi}/api/list/`)
            .then(res => {
                setContent(res.data);
                for (var i in res.data) {
                    if (props.match.url.includes(res.data[i].web)) {
                        setImages(res.data[i]);
                        setDefaultKey(i.toString());
                    };
                };
                setLoaded(true);
            });
    }, [props.match.url, defaultKey]);

    var d = new Date();
    var y = d.getFullYear();
    return (
        <div>
            <Layout style={{ minHeight: '100vh' }}>
                <Sider
                    id="sider-lg-1"
                    theme="light"
                    collapsible
                    collapsed={collapsedL}
                    onCollapse={toggleSiderLeft}
                    defaultCollapsed={true}
                    breakpoint={windowWidth ? "xs" : 'none'}
                    collapsedWidth={windowWidth ? "0" : '80'}
                    trigger={windowWidth && null}
                >
                    <div style={{ width: "200px", height: "114px", position: "relative" }}>
                        <img
                            id="math-app-logo-1" alt=""
                            style={{ clip: "rect(0 80px 200px 0)" }}
                            src={require('../assets/img/math_apps_logo.png')}
                        />
                    </div>
                    {loaded &&
                        <Menu style={{ marginTop: "32px" }} theme="light" defaultSelectedKeys={[defaultKey]} mode="inline">
                            {loaded && content.map((item, index) => {
                                return <Menu.Item
                                    onClick={() => handleUrl2(item.web)}
                                    key={index}>
                                    <AppleOutlined />
                                    <span>{item.appname}</span>
                                </Menu.Item>
                            })}
                            <Menu.Item onClick={handleApps}>
                                <AppleOutlined />
                                <span>Apps</span>
                            </Menu.Item>
                            <Menu.Item onClick={handleHome}>
                                <AppleOutlined />
                                <span>Home</span>
                            </Menu.Item>
                        </Menu>
                    }
                </Sider>

                <Layout>
                    <Header id="math-app-header">
                        <div id="math-app-header-div" style={{ position: "relative" }}>
                            {loaded && <img
                                id="math-app-header-image"
                                style={{ position: "absolute" }}
                                onLoad={setImageStyle} alt=""
                                src={images.top_image === null ? "ok" : images.top_image}
                            />}
                        </div>
                    </Header>
                    <Content style={{ margin: '0 16px' }}>
                        {windowWidth &&
                            <AppleOutlined />
                            // <Icon
                            //     style={{ position: "absolute", marginTop: "8px" }}
                            //     id="left-trigger"
                            //     type={collapsedL ? 'right-square' : 'left-square'}
                            //     theme="filled"
                            //     onClick={toggleSiderLeft}
                            // />
                        }
                        {props.children}
                    </Content>
                    <Footer id="math-app-footer">Copyright © E3 Studio {y}</Footer>
                </Layout>
                <Sider
                    id="sider-lg-2"
                    theme="light"
                    collapsible
                    collapsedrightbar={collapsedR.toString()}
                    onCollapse={onCollapseRight}
                    defaultCollapsed={true}
                    reverseArrow={true}
                    width={400}
                >
                    {loaded &&
                        <div className="sider-right">
                            <img src={loaded && images.right_image} width="100%" alt="" />
                            <div className="bottom-right" onClick={() => { window.open(images.right_image_web) }}>
                                <span style={collapsedR.collapsedrightbar ? { display: "none" } : collapsedR.collapsedrightbar === undefined ? { display: 'none' } : { color: "white", fontSize: "8px", display: "block" }}>
                                    {loaded && images.right_image_web}
                                </span>
                            </div>
                        </div>
                    }
                </Sider>

            </Layout>
        </div >
    );
}

const mapStateToProps = (state) => {
    return {
        token: state.token,
    }
};

const mapDispatchToProps = dispatch => {
    return {
        logout: () => dispatch(actions.authLogout())
    }
};

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(APLayout));

