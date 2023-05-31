import React, { useEffect } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import BaseRouter from './routes';
import { connect } from 'react-redux';
import * as actions from './store/actions/auth';
// import './e3studio/assets/simple-line-icons/css/simple-line-icons.css';
// import './e3studio/assets/css/es.bootstrap.min.css';

function App(props) {

  useEffect(() => {
    props.onTryAutoSignup();
  })
  return (
    <div className="App">
      <Router>
        {/* <CustomLayout> */}
        <BaseRouter {...props} />
        {/* </CustomLayout> */}
      </Router>
    </div>
  );
}

const mapStateToProps = state => {
  return {
    isAuthenticated: state.token !== null
  }
}

// automatic check for authentication
const mapDispatchToProps = dispatch => {
  return {
    onTryAutoSignup: () => dispatch(actions.authCheckState())
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App);
// export default App;


// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;
