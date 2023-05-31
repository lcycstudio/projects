import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import '../assets/css/appsArithmetic.css';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import { Layout, List } from 'antd';
import * as actions from '../../store/actions/auth';
import axios from 'axios';
// import AppLayout from './AALayout';

import { arithname, arithapi } from '../components/appinfo';

// import LoginForm from '../../registration/components/LoginForm';
// import { coursetitle, courseapi } from '../components/courseinfo';

const { Footer } = Layout;

const AAGrade = (props) => {
    const [content, setContent] = useState([]);
    const [loaded, setLoaded] = useState(false);
    const [topImageCnt, setTopImageCnt] = useState();
    const [loaded2, setLoaded2] = useState(false);
    const [windowWidth, setWindowWidth] = useState(false);
    useEffect(() => {
        if (window.innerWidth < 576) {
            setWindowWidth(true);
        } else {
            setWindowWidth(false);
        };

        var appnamE = props.match.params.appname;
        var appName = appnamE.charAt(0).toUpperCase() + appnamE.slice(1);
        axios.get(`/${arithapi}/api/${appName}/`)
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

    function handleUrl2(appname, grade) {
        var newAppname = appname.charAt(0).toLowerCase() + appname.slice(1);
        history.push(`/apps/arithmetic/${newAppname}/${grade}`);
    };

    // function handleHome() {
    //     window.location.href = "/";
    // };

    // function handleCourses() {
    //     // window.location.href = "/courses";
    //     history.replace("/courses");
    // };

    var d = new Date();
    var y = d.getFullYear();
    return (
        <div>
            {loaded ?
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
                    <Layout id="math-app-layout-home" >
                        <div>
                            <h3 style={{ textAlign: "center" }}>{content.appname}</h3>
                            <div style={windowWidth ? { margin: "30px auto" } : { width: "500px", margin: "30px auto" }}>
                                {content.grades.length === 0 ?
                                    <p style={{ textAlign: "center", marginTop: "80px" }}>Chapter content is not yet available.</p>
                                    :
                                    <List
                                        dataSource={content.grades}
                                        renderItem={(item, index) => (
                                            <List.Item>
                                                <h6
                                                    className="grade-item text-center"
                                                    onClick={() => { handleUrl2(content.appname, content.webs[index]) }}
                                                >{item}</h6>
                                            </List.Item>
                                        )}
                                    />
                                }
                            </div>
                        </div>
                    </Layout>
                    <Footer id="math-app-footer-home">Copyright © E3 Studio {y}</Footer>
                </Layout>
                :
                <div className="text-center">

                    {/* <Icon type="loading" style={{ color: "blue" }} /> */}
                </div>
            }
        </div>
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

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(AAGrade));

