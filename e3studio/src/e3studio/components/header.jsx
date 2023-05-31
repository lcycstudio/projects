import React from 'react';
import '../assets/css/es.css';
import '../assets/css/es.bootstrap.min.css';

const scrollToRef = (ref) => window.scrollTo({ top: ref.current.offsetTop, behavior: 'smooth' })

class Header extends React.Component {
    constructor(props) {
        super(props);
        this.myRef = React.createRef();
    }

    render() {
        return (
            <header className="masthead d-flex" id="page-top" ref={this.props.gref}>
                <div className="container text-center my-auto">
                    <h1 className="mb-1">E3 Studio</h1>
                    <h3 className="mb-5">
                        <em>A Personal Website from Lewis Chen</em>
                    </h3>
                    <button className="btn btn-primary btn-xl js-scroll-trigger" onClick={() => scrollToRef(this.props.iabout)}>Find Out More</button>
                </div>
                <div className="overlay"></div>
            </header>
        );
    }

}

export default Header;