import React from 'react';

export default () => {
    var d = new Date();
    var y = d.getFullYear(); 
    return (
        <footer className="footer text-center">
            <div className="container">
            <ul className="list-inline mb-5">
                <li className="list-inline-item">
                <a className="social-link rounded-circle text-white mr-3" href="https://www.facebook.com/profile.php?id=100009138818956">
                    <i className="icon-social-facebook"></i>
                </a>
                </li>
                <li className="list-inline-item">
                <a className="social-link rounded-circle text-white mr-3" href="https://twitter.com/lcyc29">
                    <i className="icon-social-twitter"></i>
                </a>
                </li>
                <li className="list-inline-item">
                <a className="social-link rounded-circle text-white" href="https://github.com/Lcyc29">
                    <i className="icon-social-github"></i>
                </a>
                </li>
            </ul>
            <p className="text-muted small mb-0">Copyright &copy; E3 Studio {y}</p>
            </div>
        </footer>
    );
}