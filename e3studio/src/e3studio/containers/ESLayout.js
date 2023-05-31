import React, { useRef, useEffect, useState } from 'react';
import About from '../components/about';
import Header from '../components/header';
import Services from '../components/services';
import Portfolio from '../components/portfolio';
import Contact from '../components/contact';
import Footer from '../components/footer';
import ShowNav from '../components/nav/shownav';
import App from '../components/apps';

import '../assets/css/es.css';


const scrollToRef = (ref) => window.scrollTo({ top: ref.offsetTop, behavior: 'smooth' })
const useMountEffect = (fun) => useEffect(fun, [])


const ESLayout = (props) => {

    const [showUparrow, setShowUparrow] = useState(false);

    const home = useRef(null);
    const about = useRef(null);
    const services = useRef(null);
    const portfolio = useRef(null);
    const contact = useRef(null);
    const app = useRef(null);

    useMountEffect(() => scrollToRef(home));
    useMountEffect(() => scrollToRef(about));
    useMountEffect(() => scrollToRef(services));
    useMountEffect(() => scrollToRef(portfolio));
    useMountEffect(() => scrollToRef(contact));
    useMountEffect(() => scrollToRef(app));

    function handleScroll() {
        window.addEventListener('scroll', updateScroll);
    }

    function updateScroll() {
        if (window.scrollY > 0) {
            setShowUparrow(true);
        } else {
            setShowUparrow(false);
        }
    }

    return (
        <div onScroll={handleScroll()}>
            <ShowNav ihome={home} iabout={about} iservices={services} iportfolio={portfolio} iapp={app} icontact={contact} />

            <Header gref={home} iabout={about} iportfolio={portfolio} />

            <About gref={about} iservices={services}></About>

            <Services gref={services} iportfolio={portfolio} iapp={app}></Services>

            {/* <Callout iportfolio={portfolio}></Callout> */}

            <Portfolio gref={portfolio}></Portfolio>

            <App gref={app}></App>
            {/* <Button></Button> */}
            {/* need to change the map to contact */}
            <Contact gref={contact}></Contact>

            <Footer></Footer>

            <span className="scroll-to-top rounded" style={{ visibility: showUparrow ? 'visible' : 'hidden' }} onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
                <i className="fa fa-angle-up"></i>
            </span>
        </div>
    );
}

export default ESLayout;
