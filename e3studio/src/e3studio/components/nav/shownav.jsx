import React from 'react';
import PopNav from './popnav';

// const scrollToRef = (ref) => window.scrollTo({top: ref.current.offsetTop, behavior:'smooth'})

class ShowNav extends React.Component {
    constructor(props) {
        super(props);
        this.state = { showPopup: false };
    }

    closePopup() {
        this.setState({
            showPopup: false
        });
    }

    togglePopup() {
        this.setState({
            showPopup: !this.state.showPopup
        });
    }

    // componentDidMount() {
    //     document.addEventListener('click', this.handleClick);
    // }

    // componentWillUnmount() {
    //     document.removeEventListener('click', this.handleClick);
    // }

    render() {
        const isPop = this.state.showPopup;
        return (
            <div>
                <button className="menu-toggle rounded" onClick={this.togglePopup.bind(this)} ref={node => this.node = node} >
                    {isPop ? <i className="fa fa-times"></i> : <i className="fa fa-bars"></i>}
                </button>
                <PopNav
                    active={isPop ? "sidebar-wrapper active" : "sidebar-wrapper"}
                    toggle={this.togglePopup.bind(this)}
                    close={this.closePopup.bind(this)}
                    btnNode={this.node}
                    ispop={isPop}
                    iihome={this.props.ihome}
                    iiabout={this.props.iabout}
                    iiservices={this.props.iservices}
                    iiportfolio={this.props.iportfolio}
                    iiapp={this.props.iapp}
                    iicontact={this.props.icontact}
                />
            </div>
        )
    }
}

export default ShowNav;