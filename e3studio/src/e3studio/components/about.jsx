import React from 'react';

const scrollToRef = (ref) => window.scrollTo({ top: ref.current.offsetTop, behavior: 'smooth' })

class About extends React.Component {
    // constructor(props) {
    //     super(props);
    // }
    render() {
        return (
            <section className="content-section bg-light" id="about" ref={this.props.gref}>
                <div className="container text-center">
                    <div className="row">
                        <div className="col-lg-10 mx-auto">
                            <h2>E3 Studio is where I can showcase my skills in </h2>
                            <h2 style={{ marginBottom: "20px" }}>Web Development, Programming and Analytics</h2>
                            {/* <p className="lead mb-5">This theme features a flexible, UX friendly sidebar menu and stock photos from photographers at
                        <a href="https://unsplash.com/"> Unsplash</a>!</p> */}
                            <button className="btn btn-dark btn-xl js-scroll-trigger" onClick={() => scrollToRef(this.props.iservices)} >What We Offer</button>
                        </div>
                    </div>
                </div>
            </section>
        );
    }
}

export default About;