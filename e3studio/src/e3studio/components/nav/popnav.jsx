import React from 'react';


const scrollToRef = (ref) => window.scrollTo({ top: ref.current.offsetTop, behavior: 'smooth' })
// const scrollToRef = (ref) => window.scrollTo(0, ref.current.offsetTop);
// const useMountEffect = (fun) => useEffect(fun, []);


class PopNav extends React.Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.state = { showPopup: false };
    }

    togglePopup() {
        this.setState({
            showPopup: !this.state.showPopup
        });
    }

    componentDidMount() {
        document.addEventListener('click', this.handleClick);
    }

    componentWillUnmount() {
        document.removeEventListener('click', this.handleClick);
    }

    handleClick(e) {
        if (!this.node.contains(e.target)) {
            if (this.props.ispop && !this.props.btnNode.contains(e.target)) {
                e.target.addEventListener('click', this.props.close);
            }
        }
    }

    clickLogin(e) {
        setTimeout(() => { window.location.href = "/registration/login" }, 500)
    }

    render() {
        return (
            <div>
                <nav className={this.props.active} onClick={this.props.toggle}>
                    <ul className="sidebar-nav" ref={node => this.node = node}>
                        <li className="sidebar-brand" onClick={() => scrollToRef(this.props.iihome)}>
                            <span> E3 Studio</span>
                        </li>
                        <li className="sidebar-nav-item" onClick={() => scrollToRef(this.props.iihome)}>
                            <span>Home</span>
                        </li>
                        <li className="sidebar-nav-item" onClick={() => scrollToRef(this.props.iiabout)}>
                            <span>About</span>
                        </li>
                        <li className="sidebar-nav-item" onClick={() => scrollToRef(this.props.iiservices)}>
                            <span>Services</span>
                        </li>
                        <li className="sidebar-nav-item" onClick={() => scrollToRef(this.props.iiportfolio)}>
                            <span>Courses</span>
                        </li>
                        <li className="sidebar-nav-item" onClick={() => scrollToRef(this.props.iiapp)}>
                            <span>Apps</span>
                        </li>
                        <li className="sidebar-nav-item" onClick={() => scrollToRef(this.props.iicontact)}>
                            <span>Contact</span>
                        </li>
                        <li className="sidebar-nav-item" onClick={this.clickLogin}>
                            <span className="js-scroll-trigger" >Login</span>
                        </li>
                    </ul>
                </nav>
            </div>
        );
    }
}

export default PopNav;