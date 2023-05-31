import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import { Layout, Row, Col, Breadcrumb, Button, Slider, } from 'antd';
import * as actions from '../../store/actions/auth';
import axios from 'axios';
import AppLayout from './APLayout';

import { appapi } from '../components/appinfo';

// import initBuffers from '../components/initBuffers';
// import initShaderProgram from '../components/initShaderProgram';
// import drawBox from '../components/drawBox';
import { addStyles } from 'react-mathquill'
// var mat4 = require('gl-mat4');

addStyles()

const { Content } = Layout;

const AMHome = (props) => {
    // 
    const [appContent, setAppContent] = useState([]);
    const [windowWidth, setWindowWidth] = useState(false);
    const [loaded1, setLoaded1] = useState(false);

    const [hValue, setHValue] = useState(3);
    const [hvValue, setHvValue] = useState(20);
    const [dvvValue, setDvvValue] = useState(0);
    const [uvvValue, setUvvValue] = useState(0);
    const [vvValue, setVvValue] = useState(0);
    const [gravValue, setGravValue] = useState(9.8);
    const [airrValue, setAirrValue] = useState(0);
    const [corValue, setCorValue] = useState(0.5);
    const [freqValue, setFreqValue] = useState(20);
    const [rbValue, setRbValue] = useState(0.1);
    const [frValue, setFrValue] = useState(20);
    const [ballscale, setBallscale] = useState(0.36)
    const [direction, setDirection] = useState('clockwise');

    const [resdata, setResdata] = useState();
    // eslint-disable-next-line
    const [error, setError] = useState("");

    const heights = {
        1: '1',
        10: '10',
    };

    const horizontal_v = {
        0: '0',
        50: '50',
    };

    const vertical_v_down = {
        0: '0',
        50: '50',
    };

    const vertical_v_up = {
        0: '0',
        50: '50',
    };

    const gravs = {
        0.1: '0.1',
        100: '100',
    };

    const airrs = {
        0: '0',
    };

    const cors = {
        0: '0',
        0.99: '0.99',
    };

    const freqs = {
        0: '0',
        90: '90',
    }

    const radii = {
        0.01: '0.01',
        1.0: '1.0',
    }

    const frics = {
        1: '1',
        200: '200',
    }

    function onChangeHeight(value) {
        setHValue(value);
    };

    function onChangeHV(value) {
        setHvValue(value);
    };

    function onChangeDVV(value) {
        setDvvValue(value);
        setVvValue(-value);
    };

    function onChangeUVV(value) {
        setUvvValue(value);
        setVvValue(value);
    };

    function onChangeGrav(value) {
        setGravValue(value);
    };

    function onChangeAirr(value) {
        setAirrValue(value);
    };

    function onChangeCOR(value) {
        setCorValue(value);
    };

    function onChangeFREQ(value) {
        setFreqValue(value);
    };

    function onChangeRB(value) {
        setRbValue(value);
        setBallscale(1.818 * value + 0.182);
    };

    function onChangeFR(value) {
        setFrValue(value);
    };

    function init() {
        var canvas1 = document.getElementById('my_Canvas1');
        var canvas2 = document.getElementById('my_Canvas2');
        // canvas1.style.zoom = "1.0";
        var ctx1 = canvas1.getContext('2d');
        var ctx2 = canvas2.getContext('2d');
        var image = new Image();
        image.src = require("../assets/img/smiley.gif");
        var background = new Image();
        background.src = require('../assets/img/sea.jpg');

        var ball = {
            x: 100 + resdata.xdata[0],
            y: canvas1.height - 100 - resdata.ydata[0],//(hValue * 50 + 100) - resdata.ydata[0],
            a: 0,
            count: 0,
            draw: function () {
                ctx1.translate(this.x, this.y);
                ctx1.rotate(this.a);
                ctx1.drawImage(image, -(image.width * ballscale) / 2, -(image.height * ballscale) / 2, image.width * ballscale, image.height * ballscale);
                ctx1.rotate(-this.a);
                ctx1.translate(-this.x, -this.y);
                if (resdata.xdata[this.count] > (canvas1.width - 10)) {
                    var cc = Math.floor(resdata.xdata[this.count] / canvas1.width);
                    ball.x = resdata.xdata[this.count] - (cc * canvas1.width - 10);
                } else {
                    ball.x = 100 + resdata.xdata[this.count];
                }
                ball.y = canvas1.height - 100 - resdata.ydata[this.count]; //(hValue * 50 + 100) - resdata.ydata[this.count];
                ball.a += resdata.wdata[this.count] * Math.PI / 180;
                this.count += 1;
                if (this.count === resdata.xdata.length) {
                    this.count = 0;
                };
                ctx2.drawImage(background, 0, 0);
            }
        };

        function draw() {
            ctx1.clearRect(0, 0, canvas1.width, canvas1.height);
            ctx2.clearRect(0, 0, canvas1.width, canvas1.height);
            ball.draw();
            window.requestAnimationFrame(draw);
        }

        window.requestAnimationFrame(draw);
        // canvas.addEventListener('mouseover', function (e) {
        //     raf = window.requestAnimationFrame(draw);
        // });

        // canvas.addEventListener('mouseout', function (e) {
        //     window.cancelAnimationFrame(raf);
        // });
    }

    useEffect(() => {

        if (window.innerWidth < 576) {
            setWindowWidth(true);
        } else {
            setWindowWidth(false);
        };

        axios.get(`/${appapi}/api/A Bouncing Ball/`)
            .then(res => {
                setAppContent(res.data);
            });
        if (loaded1) {
            init();
        };
        // eslint-disable-next-line
    }, [props.match.url, loaded1]);


    function handleSubmit() {
        setLoaded1(false);
        setResdata("");
        axios.put(`/apps_physics/api/A Bouncing Ball/put/`, {
            height: hValue * 50,
            vertical_v: vvValue,
            horizontal_v: hvValue,
            gravitational: gravValue,
            air_resistance: airrValue,
            restitution: corValue,
            frequency: freqValue,
            radius: rbValue,
            friction: frValue,
            clockwise: direction,
        }).then(res => {
            setResdata(res.data);
            setLoaded1(true);
        }).catch(error => {
            setError(error);
        });
    };

    const history = useHistory();

    function handleUrl0() {
        history.push(`/`);
    };

    function handleUrl1() {
        history.push(`/apps`);
    };

    function handleUrl2() {
        history.push(`/apps/physics`);
    };

    return (
        <AppLayout>
            <Breadcrumb style={windowWidth ? { margin: '8px 0 8px 32px' } : { margin: '8px 0 8px 16px' }}>
                <Breadcrumb.Item className="math-app-breadcrumb" onClick={() => handleUrl0()} >Home</Breadcrumb.Item>
                <Breadcrumb.Item className="math-app-breadcrumb" onClick={() => handleUrl1()} >Apps</Breadcrumb.Item>
                <Breadcrumb.Item className="math-app-breadcrumb" onClick={() => handleUrl2()} >Physics</Breadcrumb.Item>
                <Breadcrumb.Item >{appContent.appname}</Breadcrumb.Item>
            </Breadcrumb>
            <Content className="math-app-content">
                <Row>
                    <Col xl={10} lg={10} md={10} sm={24} xs={24}>
                        <div style={windowWidth ? {} : { marginLeft: "60px" }}>
                            <p className="latex-p" >Height <span style={{ fontWeight: "normal", fontSize: "14px", color: "#bbbbbb" }}>(default = 10 m)</span></p>
                            <Slider defaultValue={0} marks={heights}
                                min={1} max={10} step={0.1}
                                value={typeof hValue === 'number' ? hValue : 1}
                                onChange={onChangeHeight}
                                style={{ margin: "10px 30px 0" }}
                            />
                            <br />
                            <p className="latex-p" >Ball Radius <span style={{ fontWeight: "normal", fontSize: "14px", color: "#bbbbbb" }}>(m)</span></p>
                            <Slider defaultValue={0} marks={radii}
                                min={0.01} max={1.0} step={0.01}
                                value={typeof rbValue === 'number' ? rbValue : 0}
                                onChange={onChangeRB}
                                style={{ margin: "10px 30px 0" }}
                            />
                            <br />
                            <p className="latex-p" >Initial Horizontal Velocity <span style={{ fontWeight: "normal", fontSize: "14px", color: "#bbbbbb" }}>(default = 20 m/s)</span></p>
                            <Slider defaultValue={0} marks={horizontal_v}
                                min={0} max={50}
                                value={typeof hvValue === 'number' ? hvValue : 0}
                                onChange={onChangeHV}
                                style={{ margin: "10px 30px 0" }}
                            />
                            <br />
                            <p className="latex-p" >Initial Downward Vertical Velocity <span style={{ fontWeight: "normal", fontSize: "14px", color: "#bbbbbb" }}>(default = 0 m/s)</span></p>
                            <Slider defaultValue={0} marks={vertical_v_down}
                                min={0} max={50}
                                value={typeof dvvValue === 'number' ? dvvValue : 0}
                                onChange={onChangeDVV}
                                style={{ margin: "10px 30px 0" }}
                                disabled={uvvValue > 0 ? true : false}
                            />
                            <br />
                            <p className="latex-p" >Initial Upward Vertical Velocity <span style={{ fontWeight: "normal", fontSize: "14px", color: "#bbbbbb" }}>(default = 0 m/s)</span></p>
                            <Slider defaultValue={0} marks={vertical_v_up}
                                min={0} max={50}
                                value={typeof uvvValue === 'number' ? uvvValue : 0}
                                onChange={onChangeUVV}
                                style={{ margin: "10px 30px 0" }}
                                disabled={dvvValue > 0 ? true : false}
                            />
                            <br />
                            <Row>
                                <Col xl={14} lg={14} md={14} sm={24} xs={24}>
                                    <p className="latex-p" >Spin Speed <span style={{ fontWeight: "normal", fontSize: "14px", color: "#bbbbbb" }}>(default = 50 1/s)</span></p>
                                    <Slider defaultValue={0} marks={freqs}
                                        min={0} max={90} step={1}
                                        value={typeof freqValue === 'number' ? freqValue : 0}
                                        onChange={onChangeFREQ}
                                        style={{ margin: "10px 30px 0" }}
                                    />
                                </Col>
                                <Col xl={10} lg={10} md={10} sm={24} xs={24}>
                                    <p className="latex-p" >Direction <span style={{ fontWeight: "normal", fontSize: "14px", color: "#bbbbbb" }}>(default = clockwise)</span></p>
                                    <Row>
                                        <Col span={10}>
                                            <Button type="primary" style={{ marginTop: "5px" }} onClick={() => { setDirection('clockwise') }}>Clockwise</Button>
                                        </Col>
                                        <Col span={14}>
                                            <Button type="danger" style={{ marginTop: "5px" }} onClick={() => { setDirection('cclockwise') }}>Counterclockwise</Button>
                                        </Col>
                                    </Row>
                                </Col>
                            </Row>
                            <br />
                            <Row>
                                <Col xl={12} lg={12} md={12} sm={24} xs={24}>
                                    <p className="latex-p" >Gravitational Field <span style={{ fontWeight: "normal", fontSize: "14px", color: "#bbbbbb" }}>(default = 9.8 m/s/s)</span></p>
                                    <Slider defaultValue={0} marks={gravs}
                                        min={0.1} max={100} step={0.1}
                                        value={typeof gravValue === 'number' ? gravValue : 0}
                                        onChange={onChangeGrav}
                                        style={{ margin: "10px 30px 0" }}
                                    />
                                </Col>
                                <Col xl={12} lg={12} md={12} sm={24} xs={24}>
                                    <p className="latex-p" >Air Resistance <span style={{ fontWeight: "normal", fontSize: "14px", color: "#bbbbbb" }}>(default = 0 m/s/s)</span></p>
                                    <Slider defaultValue={0} marks={airrs}
                                        min={0} max={gravValue - 0.1} step={0.1}
                                        value={typeof airrValue === 'number' ? airrValue : 0}
                                        onChange={onChangeAirr}
                                        style={{ margin: "10px 30px 0" }}
                                    />
                                </Col>
                            </Row>
                            <br />
                            <p className="latex-p" >Coefficient of Resistution <span style={{ fontWeight: "normal", fontSize: "14px", color: "#bbbbbb" }}>(default = 0.5)</span></p>
                            <Slider defaultValue={0} marks={cors}
                                min={0} max={0.99} step={0.01}
                                value={typeof corValue === 'number' ? corValue : 0}
                                onChange={onChangeCOR}
                                style={{ margin: "10px 30px 0" }}
                            />

                            <br />
                            <p className="latex-p" >Coefficient of Friction <span style={{ fontWeight: "normal", fontSize: "14px", color: "#bbbbbb" }}>(default = 20)</span></p>
                            <Slider defaultValue={0} marks={frics}
                                min={1} max={200} step={1}
                                value={typeof frValue === 'number' ? frValue : 0}
                                onChange={onChangeFR}
                                style={{ margin: "10px 30px 0" }}
                            />
                            <br />
                            <div className="text-center">
                                <Button type="primary" onClick={handleSubmit}>Run</Button>
                            </div>
                        </div>
                    </Col>
                    <Col xl={14} lg={14} md={14} sm={24} xs={24} style={{ textAlign: "center" }}>
                        <h3 style={windowWidth ? { marginTop: "50px" } : {}}>Figure to be Loaded Here</h3>
                        {loaded1 &&
                            <div>
                                <div className="canvas-wrapper">
                                    <canvas id="my_Canvas1" width={windowWidth ? "311" : "640"} height={windowWidth ? "233" : "480"} style={{ zIndex: "1" }} />
                                    <canvas id="my_Canvas2" width={windowWidth ? "311" : "640"} height={windowWidth ? "233" : "480"} style={{ zIndex: "0" }} />
                                </div>
                                <br />
                                <br />

                            </div>
                        }
                    </Col>
                </Row>
            </Content>
        </AppLayout >

    );
}

const mapStateToProps = (state) => {
    return {
        token: state.token,
        course: state.course,
    }
};

const mapDispatchToProps = dispatch => {
    return {
        logout: () => dispatch(actions.authLogout())
    }
};

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(AMHome));
