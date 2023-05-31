import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import axios from 'axios';

import OnePortfolio from './onePortfolio';


const Portfolio = (props) => {
    const [portfolios, setPortfolios] = useState();
    const [loaded, setLoaded] = useState(false);


    useEffect(() => {
        axios.get(`/courses/api/list/`)
            .then(res => {
                setPortfolios(res.data);

                setLoaded(true);
            });
    }, [props]);
    return (
        <section className="callout" id="portfolio" ref={props.gref}>
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
    );
}

export default Portfolio;
