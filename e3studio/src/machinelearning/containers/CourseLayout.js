import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import '../assets/css/mlhome.css';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import { Layout } from 'antd';
import * as actions from '../../store/actions/auth';
// import ShowHeader from '../components/showheader';
import axios from 'axios';

import courseObj from '../../url/courseObj';

// import { coursetitle, courseapi } from '../components/courseinfo';

const { Footer } = Layout;

const CourseLayout = (props) => {
    const [setWidth, setSetWidth] = useState(false);
    const [topImageCnt, setTopImageCnt] = useState();
    const [loaded2, setLoaded2] = useState(false);
    const history = useHistory();



    useEffect(() => {

        if (window.innerWidth < 576) {
            setSetWidth(true);
        } else {
            setSetWidth(false);
        };

        var courseTitle;
        // var courseAPI;
        for (const [key, value] of Object.entries(courseObj)) {
            if (key === props.match.params.subject) {
                courseTitle = value;
                // courseAPI = key;
                // setCourseTitle(value);
                // setCourseApi(key);
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

    }, [props.match.params.subject, props.match.params.chapter]);

    function handleUrl2() {
        history.push(`/courses/${props.match.params.subject}`);
    };

    const windowHeight = window.innerHeight - window.innerWidth * 90 / 1920 - 96;

    var d = new Date();
    var y = d.getFullYear();
    return (
        <div>
            <Layout>
                <div id="head-div" onClick={() => { handleUrl2() }} >
                    {loaded2 && <img id="head-image" src={topImageCnt.top_image} style={{ width: "100%" }} alt="" />}
                </div>
                <Layout style={setWidth ? { margin: "16px 0 16px", minHeight: windowHeight } : { margin: "24px 0", height: windowHeight }}>
                    {props.children}
                </Layout>
                <Footer className="e3s-footer" >Copyright © E3 Studio {y}</Footer>
            </Layout>
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

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(CourseLayout));

