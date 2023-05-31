import React from 'react';
import { Route } from 'react-router-dom';

// Registration
import Login from './registration/containers/Login';
import Signup from './registration/containers/Signup';
import ForgotPassword from './registration/containers/ForgotPassword';
import EmailVerify from './registration/containers/EmailVerify';
// import EmailConfirm from './registration/containers/EmailConfirm';

// E3 Studio
import ESLayout from './e3studio/containers/ESLayout';
import ESCourses from './e3studio/containers/ESCourses';
import ESApps from './e3studio/containers/ESApps';

// Physics 11
// import P11Home from './physics11/containers/P11Home';
// import P11Chapter from './physics11/containers/P11Chapter';
// import P11Content from './physics11/containers/P11Content';

// Machine Learning
import MLHome from './machinelearning/containers/MLHome';
import MLChapter from './machinelearning/containers/MLChapter';
import MLContent from './machinelearning/containers/MLContent';

// Apps Math
import AMHome from './apps_math/containers/AMHome';
import AMApp1 from './apps_math/containers/AMApp1';
import AMApp2 from './apps_math/containers/AMApp2';

// Apps Arithmetic
import AAHome from './apps_arithmetic/containers/AAHome';
import AAGrade from './apps_arithmetic/containers/AAGrade';
import AAApp from './apps_arithmetic/containers/AAApp';

// Apps Math
import APHome from './apps_physics/containers/APHome';
import APApp1 from './apps_physics/containers/APApp1';
import APApp2 from './apps_physics/containers/APApp2';

// Physics 11
// const physics11Home = '/courses/physics11';
// const physics11Chapter = '/courses/physics11/:chapter';
// const physics11Section = '/courses/physics11/:chapter/:section';

// Machine Learning
const courseHome = '/courses/:subject';
const courseChapter = '/courses/:subject/:chapter';
const courseSection = '/courses/:subject/:chapter/:section';

// Apps Math
const appsmathHome = '/apps/math';
const appsmathApp1 = '/apps/math/commonfunctions';
const appsmathApp2 = '/apps/math/initialvalueproblems';

// Apps Math
const appsarithHome = '/apps/arithmetic';
const appsarithGrade = '/apps/arithmetic/:appname';
const appsarithApp = '/apps/arithmetic/:appname/:grade';

// Apps Math
const appsphysHome = '/apps/physics';
const appsphysApp1 = '/apps/physics/aparticleinmagneticfield';
const appsphysApp2 = '/apps/physics/abouncingball';


class BaseRouter extends React.Component {
    render() {
        return (
            <div>
                <Route exact path='/' render={(props) => <ESLayout {...props} isAuth={this.props.isAuthenticated} />} />
                <Route exact path='/courses' render={(props) => <ESCourses {...props} isAuth={this.props.isAuthenticated} />} />
                <Route exact path='/apps' render={(props) => <ESApps {...props} isAuth={this.props.isAuthenticated} />} />

                <Route exact path='/registration/login' render={(props) => <Login {...props} isAuth={this.props.isAuthenticated} />} />
                <Route exact path='/registration/signup' render={(props) => <Signup {...props} isAuth={this.props.isAuthenticated} />} />
                <Route exact path='/registration/forgot_password' render={(props) => <ForgotPassword {...props} isAuth={this.props.isAuthenticated} />} />
                <Route exact path='/registration/email-verification-sent' component={EmailVerify} />

                {/* <Route exact path={physics11Home} render={(props) => <P11Home {...props} isAuth={this.props.isAuthenticated} />} /> */}
                {/* <Route exact path={physics11Chapter} render={(props) => <P11Chapter {...props} isAuth={this.props.isAuthenticated} />} /> */}
                {/* <Route exact path={physics11Section} render={(props) => <P11Content {...props} isAuth={this.props.isAuthenticated} />} /> */}

                <Route exact path={courseHome} render={(props) => <MLHome {...props} isAuth={this.props.isAuthenticated} />} />
                <Route exact path={courseChapter} render={(props) => <MLChapter {...props} isAuth={this.props.isAuthenticated} />} />
                <Route exact path={courseSection} render={(props) => <MLContent {...props} isAuth={this.props.isAuthenticated} />} />

                <Route exact path={appsmathHome} render={(props) => <AMHome {...props} isAuth={this.props.isAuthenticated} />} />
                <Route exact path={appsmathApp1} render={(props) => <AMApp1 {...props} isAuth={this.props.isAuthenticated} />} />
                <Route exact path={appsmathApp2} render={(props) => <AMApp2 {...props} isAuth={this.props.isAuthenticated} />} />

                <Route exact path={appsarithHome} render={(props) => <AAHome {...props} isAuth={this.props.isAuthenticated} />} />
                <Route exact path={appsarithGrade} render={(props) => <AAGrade {...props} isAuth={this.props.isAuthenticated} />} />
                <Route exact path={appsarithApp} render={(props) => <AAApp {...props} isAuth={this.props.isAuthenticated} />} />

                <Route exact path={appsphysHome} render={(props) => <APHome {...props} isAuth={this.props.isAuthenticated} />} />
                <Route exact path={appsphysApp1} render={(props) => <APApp1 {...props} isAuth={this.props.isAuthenticated} />} />
                <Route exact path={appsphysApp2} render={(props) => <APApp2 {...props} isAuth={this.props.isAuthenticated} />} />

            </div>
        )
    }
};

export default BaseRouter;