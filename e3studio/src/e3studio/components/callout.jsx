import React from 'react';

const scrollToRef = (ref) => window.scrollTo({ top: ref.current.offsetTop, behavior: 'smooth' });


class Callout extends React.Component {
    // constructor(props) {
    //     super(props);
    // }
    render() {
        return (
            <section className="callout">
                <div className="container text-center">
                    <h2 className="mx-auto mb-5">Welcome to <br /><em>E3 Studio!</em></h2>
                    <button className="btn btn-primary btn-xl" onClick={() => scrollToRef(this.props.iportfolio)}>Available Subjects</button>
                </div>
            </section>
        );
    }
}

export default Callout;
