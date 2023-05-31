import React from 'react';

function OnePortfolio(props) {
    return (
        <div className="col-lg-6">
            <a className="portfolio-item" href={props.webUrl}>
                <span className="caption">
                    <span className="caption-content">
                        <h1 style={{ color: "white" }}>{props.name}</h1>
                        <p className="mb-0">{props.content}</p>
                    </span>
                </span>
                <img className="img-fluid" src={`${props.imgUrl}`} alt="" />
            </a>
        </div>
    )
}

export default OnePortfolio;
