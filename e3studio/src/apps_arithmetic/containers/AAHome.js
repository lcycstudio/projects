import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import { Layout, Card, List } from 'antd';
import * as actions from '../../store/actions/auth';
import axios from 'axios';

import { arithname, arithapi } from '../components/appinfo';

// import { Button } from 'react-bootstrap';


const { Header, Footer } = Layout;

const { Meta } = Card;

const AMHome = (props) => {

    const [content, setContent] = useState([]);
    const [loaded, setLoaded] = useState(false);
    const [topImageCnt, setTopImageCnt] = useState();
    const [loaded2, setLoaded2] = useState(false);

    useEffect(() => {

        axios.get(`/${arithapi}/api/list/`)
            .then(res => {
                setContent(res.data);
                setLoaded(true);
            });
        axios.get(`/apps/api/list/`)
            .then(res => {
                for (var i in res.data) {
                    if (res.data[i].appname === arithname) {
                        setTopImageCnt(res.data[i]);
                        setLoaded2(true);
                    };
                };
            });
    }, [props]);

    var setImageStyle = () => {
        var headerWidth = document.getElementById('math-app-header-div-home').offsetWidth;
        var headerImg = document.getElementById('math-app-header-image-home');
        if (headerWidth < 576) {
            headerImg.style.objectPosition = "-100px";
        };
    };

    const history = useHistory();

    function handleUrl1() {
        history.push(`/apps/arithmetic`);
    };

    function handleUrl2(appweb) {
        history.push(`/apps/arithmetic/${appweb}`);
    };

    // const handleLogout = () => {
    //     props.logout();
    // };

    // const handleHome = () => {
    //     window.location.href = "/";
    // };

    var d = new Date();
    var y = d.getFullYear();
    return (
        <div>
            <Layout>
                <div id="math-app-header-div-home" onClick={handleUrl1}>
                    {loaded2 &&
                        <img
                            onLoad={setImageStyle}
                            id="math-app-header-image-home" alt=""
                            src={topImageCnt.top_image}
                        />
                    }
                </div>
                <Header id="math-app-header-text-home">
                    <h1>Welcome to {arithname}</h1>
                </Header>
                <Layout id="math-app-layout-home" >
                    <div style={{ margin: "0 20%" }}>
                        <List
                            grid={{
                                gutter: 16,
                                xs: 1,
                                sm: 2,
                                md: 3,
                                lg: 4,
                                xl: 4,
                                xxl: 4,
                            }}
                            dataSource={content}
                            renderItem={item => (
                                <List.Item>
                                    <Card
                                        className="math-app-card-home"
                                        hoverable
                                        cover={loaded && <img src={item.front_image}
                                            style={{ width: "100%", borderBottom: "1px solid" }} alt=""
                                        />}
                                        onClick={() => handleUrl2(item.web)}
                                    >
                                        <Meta title={item.appname} description={item.description} />
                                    </Card>
                                </List.Item>
                            )}
                        />
                    </div>
                </Layout>
                <Footer id="math-app-footer-home">Copyright © E3 Studio {y}</Footer>
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

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(AMHome));
