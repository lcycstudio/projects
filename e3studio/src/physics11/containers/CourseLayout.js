import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import '../assets/css/p11home.css';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import { Layout } from 'antd';
import * as actions from '../../store/actions/auth';
import ShowHeader from '../components/showheader';
import axios from 'axios';


import { coursetitle, courseapi } from '../components/courseinfo';

const { Footer } = Layout;

const CourseLayout = (props) => {

    const [topImageCnt, setTopImageCnt] = useState();
    const [loaded2, setLoaded2] = useState(false);

    const history = useHistory();

    function handleUrl2() {
        history.push(`/courses/${courseapi}`);
    };


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
    }, []);

    var d = new Date();
    var y = d.getFullYear();
    return (
        <div>
            <Layout>
                <div className="head-image" onClick={() => { handleUrl2() }} >
                    {loaded2 && <img src={topImageCnt.top_image} style={{ width: "100%" }} alt="" />}
                </div>
                <ShowHeader MainUrl={MainUrl} coursetitle={coursetitle} courseapi={courseapi} />

                <Layout style={{ margin: "20px 0", height: "613px" }}>
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

