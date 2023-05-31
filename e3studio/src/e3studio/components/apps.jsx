import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import axios from 'axios';

import OneApp from './oneApp';


const App = (props) => {
    const [apps, setAppss] = useState();
    const [loaded, setLoaded] = useState(false);


    useEffect(() => {
        axios.get(`/apps/api/list/`)
            .then(res => {
                setAppss(res.data);
                setLoaded(true);
            });
    }, [props]);
    return (
        <section className="apps" id="app" ref={props.gref}>
            <div className="container">
                <div className="content-section-heading text-center">
                    <h2 className="mb-5 mx-auto text-white">Available Apps</h2>
                </div>
                {loaded &&
                    <div className="row no-gutters">
                        {apps.map(portfolio => (
                            <OneApp
                                key={portfolio.id}
                                name={portfolio.appname}
                                content={portfolio.content}
                                imgUrl={process.env.PUBLIC_URL + `${portfolio.front_image}`}
                                // process.env.PUBLIC_URL + 
                                webUrl={`${portfolio.web}`}
                            />
                        ))}
                    </div>
                }
            </div>
        </section>
    );
}

export default App;
