import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import '../assets/css/es.css';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Layout } from 'antd';
import * as actions from '../../store/actions/auth';
import axios from 'axios';
import OneApp from '../components/oneApp';


const { Footer } = Layout;

const ESApps = (props) => {
    const [apps, setApps] = useState();
    const [loaded, setLoaded] = useState(false);


    useEffect(() => {
        axios.get(`/apps/api/list/`)
            .then(res => {
                setApps(res.data);

                setLoaded(true);
            });
    }, [props]);

    var d = new Date();
    var y = d.getFullYear();

    return (
        <div>
            <section className="apps courses" id="app">
                <div className="container">
                    <div className="content-section-heading text-center">
                        <h2 className="mb-5 mx-auto text-white">Available Apps</h2>
                    </div>
                    {loaded &&
                        <div className="row no-gutters">
                            {apps.map(portfolio => (
                                <OneApp
                                    key={portfolio.id}
                                    name={portfolio.subject}
                                    content={portfolio.content}
                                    imgUrl={portfolio.front_image}
                                    webUrl={portfolio.web}
                                />
                            ))}
                        </div>
                    }
                </div>
            </section>

            <Footer style={{
                textAlign: "center",
                backgroundColor: "white",
                padding: "12px 0"
            }}>
                Copyright © E3 Studio {y}
            </Footer>
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

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ESApps));

