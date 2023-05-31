import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import '../assets/css/es.css';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Layout } from 'antd';
import * as actions from '../../store/actions/auth';
import axios from 'axios';
import OnePortfolio from '../components/onePortfolio';


const { Footer } = Layout;

const ESCourses = (props) => {
    const [portfolios, setPortfolios] = useState();
    const [loaded, setLoaded] = useState(false);


    useEffect(() => {
        axios.get(`/courses/api/list/`)
            .then(res => {
                setPortfolios(res.data);

                setLoaded(true);
            });
    }, [props]);

    var d = new Date();
    var y = d.getFullYear();

    return (
        <div>
            <section className="callout courses" id="portfolio">
                <div className="container">
                    <div className="content-section-heading text-center">
                        <h2 className="mb-5 mx-auto text-white">Available Courses</h2>
                    </div>
                    {loaded &&
                        <div className="row no-gutters">
                            {portfolios.map(portfolio => (
                                <OnePortfolio
                                    key={portfolio.id}
                                    name={portfolio.subject}
                                    content={portfolio.content}
                                    imgUrl={`${portfolio.front_image}`}
                                    webUrl={`${portfolio.web}`}
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

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ESCourses));

