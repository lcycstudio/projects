import React from 'react';

const scrollToRef = (ref) => window.scrollTo({ top: ref.current.offsetTop, behavior: 'smooth' });

class Services extends React.Component {
    // constructor(props) {
    //     super(props);
    // }
    render() {
        return (
            <section className="content-section bg-offer text-white text-center" id="services" ref={this.props.gref}>
                <div className="container">
                    <div className="content-section-heading">
                        <h3 className="text-warning mb-0">Services</h3>
                        <h2 className="mb-5">What I Offer</h2>
                    </div>
                    <div className="row mb-5">
                        <div className="col-lg-6 col-md-6 mb-5 mb-lg-0">
                            <span className="service-icon rounded-circle mx-auto mb-3">
                                <i className="icon-calendar"></i>
                            </span>
                            <h4>
                                <strong>Courses</strong>
                            </h4>
                            <p className="text-faded mb-0">Course materials are served and managed in backend</p>
                        </div>
                        {/*<div className="col-lg-3 col-md-6 mb-5 mb-lg-0">
                            <span className="service-icon rounded-circle mx-auto mb-3">
                                <i className="icon-film"></i>
                            </span>
                            <h4>
                                <strong>Tutoring</strong>
                            </h4>
                            <p className="text-faded mb-0">Focus on math and physics homework and problems</p>
                        </div>
                        <div className="col-lg-3 col-md-6 mb-5 mb-md-0">
                            <span className="service-icon rounded-circle mx-auto mb-3">
                                <i className="icon-pencil"></i>
                            </span>
                            <h4>
                                <strong>Problems</strong>
                            </h4>
                            <p className="text-faded mb-0">Wide variety of problems and tests available onsite for students</p>
                        </div> */}
                        <div className="col-lg-6 col-md-6">
                            <span className="service-icon rounded-circle mx-auto mb-3">
                                <i className="icon-drawer"></i>
                            </span>
                            <h4>
                                <strong>Apps</strong>
                            </h4>
                            <p className="text-faded mb-0">Various apps which I find useful and interesting</p>
                        </div>
                    </div>
                </div>
                <div className="container">
                    <div className="row">
                        <div className="col-lg-6 col-md-6 mb-5 mb-lg-0">
                            <button className="btn btn-warning btn-xl" onClick={() => scrollToRef(this.props.iportfolio)}>Available Courses</button>
                        </div>
                        <div className="col-lg-6 col-md-6 mb-5 mb-lg-0">
                            <button className="btn btn-warning btn-xl" onClick={() => scrollToRef(this.props.iapp)}>Available Courses</button>
                        </div>
                    </div>
                </div>
                {/* <button className="btn btn-warning btn-xl" onClick={() => scrollToRef(this.props.iportfolio)}>Available Courses</button> */}
            </section>
        );
    }
}

export default Services;