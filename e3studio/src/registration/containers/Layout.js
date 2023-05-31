import React from 'react';
import '../assets/css/registration.css';
import 'antd/dist/antd.css';
import { Layout } from 'antd';
import { Row, Col } from 'antd';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import * as actions from '../../store/actions/auth';
import login_image from '../assets/img/regi_1.jpg';






const { Content, Footer } = Layout;

class CustomLayout extends React.Component {

    render() {
        var d = new Date();
        var y = d.getFullYear();
        return (
            <Layout className="layout">
                {/* <Header>
                    <div className="logo" />
                    <Menu
                        theme="dark"
                        mode="horizontal"
                        defaultSelectedKeys={['2']}
                        style={{ lineHeight: '64px' }}
                    >
                    {
                        this.props.token ?
                        <Menu.Item key="2" onClick={this.props.logout}>
                            Logout
                        </Menu.Item>
                        :
                        <Menu.Item key="2">
                            <Link to="/login">Login</Link>
                        </Menu.Item>
                    }
                        <Menu.Item key="1">
                            <Link to={articlePath}>Posts</Link>
                        </Menu.Item>
                        
                        
                    </Menu>
                </Header> */}
                <Content style={{ padding: '50px 50px' }}>
                    {/* <Breadcrumb style={{ margin: '16px 0' }}>
                        <Breadcrumb.Item><Link to={articlePath}>Home</Link></Breadcrumb.Item>
                        <Breadcrumb.Item><Link to={articlePath}>List</Link></Breadcrumb.Item>
                        <Breadcrumb.Item>App</Breadcrumb.Item>
                    </Breadcrumb> */}
                    <Row gutter={[24, 16]} >
                        <Col xs={24} sm={24} md={12} lg={14} xl={14} >
                            {/* <div className="login-image" style={{ background: '#fff', padding: 24, minHeight: 280 }}> */}
                            <img className="login-image" src={login_image} alt="Login" />
                            {/* </div> */}
                        </Col>
                        <Col xs={24} sm={24} md={12} lg={10} xl={10} >
                            <div style={{ background: '#fff', padding: 24, minHeight: '100%' }}>
                                {this.props.children}
                            </div>
                        </Col>
                    </Row>
                    {/* <div style={{ background: '#fff', padding: 24, minHeight: 280 }}>
                        {this.props.children}
                    </div> */}
                </Content>
                <Footer style={{ textAlign: 'center', backgroundColor: "white" }}>Copyright © E3 Studio {y}</Footer>
            </Layout>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        token: state.token,
    }
};

const mapDispatchToProps = dispatch => {
    return {
        logout: () => dispatch(actions.authLogout())
    }
};

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(CustomLayout));
