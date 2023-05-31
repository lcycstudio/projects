import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import { Layout, Row, Col, Breadcrumb, Button, Slider, InputNumber } from 'antd';
import { AppleOutlined } from '@ant-design/icons';

import * as actions from '../../store/actions/auth';
import axios from 'axios';
import AppLayout from './APLayout';

import { appapi } from '../components/appinfo';

import initBuffers from '../components/initBuffers';
import initShaderProgram from '../components/initShaderProgram';
import drawBox from '../components/drawBox';

import { addStyles, StaticMathField } from 'react-mathquill'

var mat4 = require('gl-mat4');

addStyles()

const { Content } = Layout;

const AMHome = (props) => {
    // 
    const [appContent, setAppContent] = useState([]);
    const [windowWidth, setWindowWidth] = useState(false);
    const [loaded1, setLoaded1] = useState(false);

    const [pxValue, setPXValue] = useState(0);
    const [pyValue, setPYValue] = useState(0);
    const [nyValue, setNYValue] = useState(0);
    const [pzValue, setPZValue] = useState(0);
    const [nzValue, setNZValue] = useState(0);

    const [pmValue1, setPMValue1] = useState(0);
    const [pmValue2, setPMValue2] = useState('M = 9.1094\\times 10^{-31} kg');
    const [pmValue3, setPMValue3] = useState(9.1094e-31);

    const [pcValue1, setPCValue1] = useState(0);
    const [pcValue2, setPCValue2] = useState('Q = 1.602 \\times 10^{-19} C');
    const [pcValue3, setPCValue3] = useState(1.602e-19);

    const [mfValue1, setMFValue1] = useState(0);
    const [mfValue2, setMFValue2] = useState('B = 1.00 \\times 10^{-12} kg/s^{2}A');
    const [mfValue3, setMFValue3] = useState(1.00e-12);

    const [roValue2, setROValue2] = useState('\\omega = \\frac{QB}{M} = 0.176');
    // eslint-disable-next-line
    const [roValue3, setROValue3] = useState(0.176);

    const [checkro, setCheckro] = useState(true);
    const [direction, setDirection] = useState('z');
    const [resdata, setResdata] = useState();
    // eslint-disable-next-line
    const [error, setError] = useState("");

    function mainDat(rotx, roty, rotz) {
        const canvas1 = document.getElementById('my_Canvas1');
        const hl = canvas1.getContext('experimental-webgl');

        /*=========================Shaders========================*/

        // vertex shader source code
        var vertCode =
            'attribute vec3 coordinates;' +
            'uniform mat4 uMVMatrix;' +
            'uniform mat4 uPJMatrix;' +

            'void main(void) {' +
            ' gl_Position = uPJMatrix * uMVMatrix * vec4(coordinates, 1.0);' +
            'gl_PointSize = 10.0;' +
            '}';

        // fragment shader source code
        var fragCode =
            'void main(void) {' +
            ' gl_FragColor = vec4(1.0, 0.0, 1.0, 1.0);' +
            '}';


        // Create an empty buffer object to store the vertex buffer
        var vertex_buffer = hl.createBuffer();
        // Create a vertex shader object
        var vertShader = hl.createShader(hl.VERTEX_SHADER);
        hl.shaderSource(vertShader, vertCode);
        hl.compileShader(vertShader);

        // Create fragment shader object
        var fragShader = hl.createShader(hl.FRAGMENT_SHADER);
        hl.shaderSource(fragShader, fragCode);
        hl.compileShader(fragShader);

        // Create a shader program object to store
        // the combined shader program
        var shaderProgram1 = hl.createProgram();
        hl.attachShader(shaderProgram1, vertShader);
        hl.attachShader(shaderProgram1, fragShader);
        hl.linkProgram(shaderProgram1);



        /*============= Drawing the primitive ===============*/


        const rotx_objd = { value: rotx };
        const roty_objd = { value: roty };
        const rotz_objd = { value: rotz };


        var count = 0;
        function drawParticle(hl, canvas1, vertex_buffer, shaderProgram, rotx, roty, rotz) {
            count++;
            var length = resdata.xdata.length;
            var index = Math.floor(count / 0.3 % length);
            var vertices = [];
            vertices.push(resdata.xdata[index], resdata.ydata[index], resdata.zdata[index],);

            /*======== Associating shaders to buffer objects ========*/

            //Bind appropriate array buffer to it
            hl.bindBuffer(hl.ARRAY_BUFFER, vertex_buffer);

            // Pass the vertex data to the buffer
            hl.bufferData(hl.ARRAY_BUFFER, new Float32Array(vertices), hl.STATIC_DRAW);

            // Unbind the buffer
            hl.bindBuffer(hl.ARRAY_BUFFER, null);

            // Bind vertex buffer object
            hl.bindBuffer(hl.ARRAY_BUFFER, vertex_buffer);

            // Get the attribute location
            var coord = hl.getAttribLocation(shaderProgram, "coordinates");

            // Point an attribute to the currently bound VBO
            hl.vertexAttribPointer(coord, 3, hl.FLOAT, false, 0, 0);

            // Enable the attribute
            hl.enableVertexAttribArray(coord);

            const fieldOfView = 45 * Math.PI / 180;   // in radians
            const aspect = hl.canvas.clientWidth / hl.canvas.clientHeight;
            const zNear = 0.1;
            const zFar = 1000.0;
            const projectionMatrix1 = mat4.create();

            // note: glmatrix.js always has the first argument
            // as the destination to receive the result.
            mat4.perspective(projectionMatrix1,
                fieldOfView,
                aspect,
                zNear,
                zFar);

            // Set the drawing position to the "identity" point, which is
            // the center of the scene.
            const modelViewMatrix1 = mat4.create();

            mat4.translate(modelViewMatrix1,     // destination matrix
                modelViewMatrix1,     // matrix to translate
                [0.0, 0.0, -350.0]);  // amount to translate
            mat4.rotate(modelViewMatrix1,  // destination matrix
                modelViewMatrix1,  // matrix to rotate
                (-90 + rotx) * Math.PI / 180,     // amount to rotate in radians
                [1, 0, 0]);       // axis to rotate around (X)
            mat4.rotate(modelViewMatrix1,  // destination matrix
                modelViewMatrix1,  // matrix to rotate
                roty * Math.PI / 180,// amount to rotate in radians
                [0, 1, 0]);       // axis to rotate around (Y)
            mat4.rotate(modelViewMatrix1,  // destination matrix
                modelViewMatrix1,  // matrix to rotate
                (-90 + rotz) * Math.PI / 180,// amount to rotate in radians
                [0, 0, 1]);       // axis to rotate around (Z)


            // hl.clearColor(0.0, 0.8, 0.9, 0.0);  // Clear to black, fully opaque
            // hl.clearDepth(1.0);                 // Clear everything
            // hl.enable(hl.DEPTH_TEST);           // Enable depth testing
            hl.depthFunc(hl.LEQUAL);            // Near things obscure far things
            hl.enable(hl.DEPTH_TEST);
            hl.clear(hl.COLOR_BUFFER_BIT | hl.DEPTH_BUFFER_BIT);


            hl.useProgram(shaderProgram1);

            hl.uniformMatrix4fv(
                hl.getUniformLocation(shaderProgram1, 'uPJMatrix'),
                false,
                projectionMatrix1);
            hl.uniformMatrix4fv(
                hl.getUniformLocation(shaderProgram1, 'uMVMatrix'),
                false,
                modelViewMatrix1);

            // Set the view port
            hl.viewport(0, 0, canvas1.width, canvas1.height);

            // Draw the triangle
            hl.drawArrays(hl.POINTS, 0, 1);
        }

        // var then = 0;

        // Draw the scene repeatedly
        function render(now) {
            now *= 0.001;  // convert to seconds
            // const deltaTime = now - then;
            // then = now;

            drawParticle(hl, canvas1, vertex_buffer, shaderProgram1, rotx_objd.value, roty_objd.value, rotz_objd.value);

            requestAnimationFrame(render);
        }
        requestAnimationFrame(render);
    }

    function mainBox(rotx, roty, rotz) {
        const canvas = document.getElementById('my_Canvas2');
        const gl = canvas.getContext('experimental-webgl');

        // If we don't have a GL context, give up now

        if (!gl) {
            alert('Unable to initialize WebGL. Your browser or machine may not support it.');
            return;
        }

        // Vertex shader program

        const vsSource = `
        attribute vec4 aVertexPosition;
        attribute vec4 aVertexColor;
        uniform mat4 uModelViewMatrix;
        uniform mat4 uProjectionMatrix;
        varying lowp vec4 vColor;
        void main(void) {
          gl_Position = uProjectionMatrix * uModelViewMatrix * aVertexPosition;
          vColor = aVertexColor;
        }
      `;

        // Fragment shader program

        const fsSource = `
        varying lowp vec4 vColor;
        void main(void) {
          gl_FragColor = vColor;
        }
      `;

        // Initialize a shader program; this is where all the lighting
        // for the vertices and so forth is established.
        const shaderProgram = initShaderProgram(gl, vsSource, fsSource);

        // Collect all the info needed to use the shader program.
        // Look up which attributes our shader program is using
        // for aVertexPosition, aVevrtexColor and also
        // look up uniform locations.
        const programInfo = {
            program: shaderProgram,
            attribLocations: {
                vertexPosition: gl.getAttribLocation(shaderProgram, 'aVertexPosition'),
                vertexColor: gl.getAttribLocation(shaderProgram, 'aVertexColor'),
            },
            uniformLocations: {
                projectionMatrix: gl.getUniformLocation(shaderProgram, 'uProjectionMatrix'),
                modelViewMatrix: gl.getUniformLocation(shaderProgram, 'uModelViewMatrix'),
            }
        };

        // Here's where we call the routine that builds all the
        // objects we'll be drawing.

        const buffers = initBuffers(gl, rotx, roty, rotz);

        // var then = 0;

        const rotx_obj = { value: rotx };
        const roty_obj = { value: roty };
        const rotz_obj = { value: rotz };
        // Draw the scene repeatedly
        function render(now) {
            now *= 0.001;  // convert to seconds
            // const deltaTime = now - then;
            // then = now;

            drawBox(gl, programInfo, buffers, rotx_obj.value, roty_obj.value, rotz_obj.value);

            requestAnimationFrame(render);
        }
        requestAnimationFrame(render);
    };

    const [rotx, setRotx] = useState(0);
    const [roty, setRoty] = useState(0);
    const [rotz, setRotz] = useState(0);

    function onChangePX(value) {
        setPXValue(value);
        setRotx(value);
    };
    function onChangePY(value) {
        setPYValue(value);
        setRoty(value);
    };
    function onChangeNY(value) {
        setNYValue(value);
        setRoty(-1.0 * value);
    };
    function onChangePZ(value) {
        setPZValue(value);
        setRotz(value);
    };
    function onChangeNZ(value) {
        setNZValue(value);
        setRotz(-1.0 * value);
    };

    const particles = {
        0: 'Electron',
        1000: 'Proton',
    };

    function onChangePM(value) {
        setPMValue1(value);
        const electron = 9.1094;
        const exp = 1e-31;
        const ratio = 16716.8906;
        if (value === 0) {
            setPMValue2('M = 9.1094 \\times 10^{-31} kg');
            setPMValue3(9.1094e-31);
            var ro = (pcValue3 * mfValue3 / (9.1094e-31)).toFixed(3);
            setROValue3(ro);
            setROValue2('\\omega = \\frac{QB}{M} = ' + ro.toString());
        } else if (value === 1000) {
            setPMValue2('M = 1.6726 \\times 10^{-27} kg');
            setPMValue3(1.6726e-27);
            ro = (pcValue3 * mfValue3 / (1.6726e-27)).toFixed(3);
            setROValue3(ro);
            setROValue2('\\omega = \\frac{QB}{M} = ' + ro.toString());
        } else {
            var ans = (Number((electron + (ratio * value / 1000)).toFixed(4)) * exp).toString();
            var ans1 = ans.slice(0, 6);
            var ans2 = ans.slice(-3,);
            var ans3 = 'M = ' + ans1 + "\\times 10^{" + ans2 + "} kg";
            setPMValue2(ans3);
            var mass = (electron + (ratio * value / 1000)) * exp;
            setPMValue3(mass);
            ro = (pcValue3 * mfValue3 / mass).toFixed(3);
            setROValue3(ro);
            setROValue2('\\omega = \\frac{QB}{M} = ' + ro.toString());
        };
        if (ro < 0.1 || ro > 10) {
            setCheckro(false)
        } else {
            setCheckro(true)
        };
    };

    const charge = {
        0: '1.602e-19',
        100: {
            style: {
                width: "70px",
            },
            label: '1.602e-17',
        },
    };

    function onChangePC(value) {
        setPCValue1(value);
        const charge = 1.602;
        const exp = 1e-19;
        const ratio = 100;
        if (value === 0) {
            setPCValue2('Q = 1.602 \\times 10^{-19} C');
            setPCValue3(1.602e-19);
            var ro = ((1.602e-19) * mfValue3 / pmValue3).toFixed(3);
            setROValue3(ro);
            setROValue2('\\omega = \\frac{QB}{M} = ' + ro.toString());
        } else if (value === 100) {
            setPCValue2('Q = 1.602 \\times 10^{-17} C');
            setPCValue3(1.602e-17);
            ro = ((1.602e-17) * mfValue3 / pmValue3).toFixed(3);
            setROValue3(ro);
            setROValue2('\\omega = \\frac{QB}{M} = ' + ro.toString());
        }
        else {
            var ans = (Number((charge + (ratio * value / 100)).toFixed(3)) * exp).toString();
            var ans1 = ans.slice(0, 4);
            var ans2 = ans.slice(-3,);
            if (ans2.includes('e')) {
                ans2 = ans2.slice(-2,);
            };
            var ans3 = "Q = " + ans1 + "\\times 10^{" + ans2 + "} C";
            setPCValue2(ans3);
            var chg = (charge + (ratio * value / 100)) * exp;
            setPCValue3(chg);
            ro = (chg * mfValue3 / pmValue3).toFixed(3);
            setROValue3(ro);
            setROValue2('\\omega = \\frac{QB}{M} = ' + ro.toString());
        };
        if (ro < 0.1 || ro > 10) {
            setCheckro(false)
        } else {
            setCheckro(true)
        };
    };

    const magnetic = {
        0: '1.0e-12',
        1000: {
            style: {
                width: "46px",
            },
            label: '1.0e-7',
        },
    };

    function onChangeMF(value) {
        setMFValue1(value);
        const magneticF = 1.0;
        const exp = 1e-12;
        const ratio = 100000;
        if (value === 0) {
            setMFValue2('B = 1.00 \\times 10^{-12} kg/s^{2}A');
            setMFValue3(1.00e-12);
            var ro = (pcValue3 * (1.00e-12) / pmValue3).toFixed(3);
            setROValue3(ro);
            setROValue2('\\omega = \\frac{QB}{M} = ' + ro.toString());
        } else if (value === 1000) {
            setMFValue2('B = 1.00 \\times 10^{-7} kg/s^{2}A');
            setMFValue3(1.00e-7);
            ro = (pcValue3 * (1.00e-7) / pmValue3).toFixed(3);
            setROValue3(ro);
            setROValue2('\\omega = \\frac{QB}{M} = ' + ro.toString());
        }
        else {
            var ans = (Number((magneticF + (ratio * value / 1000)).toFixed(3)) * exp).toString();
            var ans1 = ans.slice(0, 4);
            var ans2 = ans.slice(-3,);
            if (ans2.includes('e')) {
                ans2 = ans2.slice(-2,);
            };
            var ans3 = "B = " + ans1 + "\\times 10^{" + ans2 + "} kg/s^{2}A";
            setMFValue2(ans3);
            var mag = (magneticF + (ratio * value / 1000)) * exp;
            setMFValue3(mag);
            ro = (pcValue3 * mag / pmValue3).toFixed(3);
            setROValue3(ro);
            setROValue2('\\omega = \\frac{QB}{M} = ' + ro.toString());
        };
        if (ro < 0.1 || ro > 10) {
            setCheckro(false)
        } else {
            setCheckro(true)
        };
    };

    const [spValue1, setSPValue1] = useState(1);

    const speed = {
        1: '1',
        10: '10',
    };

    function onChangeSP(value) {
        setSPValue1(value);
    };




    useEffect(() => {

        if (window.innerWidth < 576) {
            setWindowWidth(true);
        } else {
            setWindowWidth(false);
        };

        axios.get(`/${appapi}/api/A Particle in Magnetic Field/`)
            .then(res => {
                setAppContent(res.data);
            });
        if (loaded1) {
            mainDat(rotx, roty, rotz);
            mainBox(rotx, roty, rotz);
        };
        // eslint-disable-next-line
    }, [props.match.url, rotx, roty, rotz, loaded1]);


    function handleSubmit() {
        setLoaded1(false);
        setResdata("");
        axios.put(`/apps_physics/api/A Particle in Magnetic Field/put/`, {
            mass: pmValue3,
            charge: pcValue3,
            magnet: mfValue3,
            speed: spValue1,
            direction: direction
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
                            <p className="latex-p" >Particle Mass</p>
                            <Slider defaultValue={0} marks={particles}
                                min={0} max={1000}
                                value={typeof pmValue1 === 'number' ? pmValue1 : 0}
                                onChange={onChangePM}
                                style={{ margin: "10px 30px 0" }}
                            />
                            <br />
                            <Row>
                                <Col xl={12} lg={12} md={12} sm={24} xs={24}>
                                    <div className="text-center" style={windowWidth ? { margin: "10px 0" } : {}} >
                                        <InputNumber
                                            min={0}
                                            max={1000}
                                            value={pmValue1}
                                            onChange={onChangePM}
                                        />
                                    </div>
                                </Col>
                                <Col xl={12} lg={12} md={12} sm={24} xs={24}>
                                    <div className={windowWidth ? "text-center" : "text-left"} >
                                        <StaticMathField style={{ border: " 1px solid", padding: "0px 4px" }}>
                                            {pmValue2}
                                        </StaticMathField>
                                    </div>
                                </Col>
                            </Row>
                            <br />
                            <p className="latex-p" >Particle Charge</p>
                            <Slider defaultValue={0} marks={charge}
                                min={0} max={100}
                                value={typeof pcValue1 === 'number' ? pcValue1 : 0}
                                onChange={onChangePC}
                                style={{ margin: "10px 30px 0" }}
                            />
                            <br />
                            <Row>
                                <Col xl={12} lg={12} md={12} sm={24} xs={24}>
                                    <div className="text-center" style={windowWidth ? { margin: "10px 0" } : {}}>
                                        <InputNumber
                                            min={0}
                                            max={100}
                                            value={pcValue1}
                                            onChange={onChangePC}
                                        />
                                    </div>
                                </Col>
                                <Col xl={12} lg={12} md={12} sm={24} xs={24}>
                                    <div className={windowWidth ? "text-center" : "text-left"} >
                                        <StaticMathField style={{ border: " 1px solid", padding: "0px 4px" }}>
                                            {pcValue2}
                                        </StaticMathField>
                                    </div>
                                </Col>
                            </Row>
                            <br />
                            <p className="latex-p" >Magnetic Field</p>
                            <Slider defaultValue={0} marks={magnetic}
                                min={0} max={1000}
                                value={typeof mfValue1 === 'number' ? mfValue1 : 0}
                                onChange={onChangeMF}
                                style={{ margin: "10px 30px 0" }}
                            />
                            <br />
                            <Row>
                                <Col xl={12} lg={12} md={12} sm={24} xs={24}>
                                    <div className="text-center" style={windowWidth ? { margin: "10px 0" } : {}}>
                                        <InputNumber
                                            min={0}
                                            max={1000}
                                            value={mfValue1}
                                            onChange={onChangeMF}
                                        />
                                    </div>
                                </Col>
                                <Col xl={12} lg={12} md={12} sm={24} xs={24}>
                                    <div className={windowWidth ? "text-center" : "text-left"} >
                                        <StaticMathField style={{ border: " 1px solid", padding: "0px 4px" }}>
                                            {mfValue2}
                                        </StaticMathField>
                                    </div>
                                </Col>
                            </Row>
                            <br />
                            <p className="latex-p" >Initial Speed</p>
                            <Slider defaultValue={0} marks={speed}
                                min={1} max={10}
                                value={typeof spValue1 === 'number' ? spValue1 : 0}
                                onChange={onChangeSP}
                                style={{ margin: "10px 30px 0" }}
                            />
                            <br />

                            <br />
                            <p className="latex-p" >Direction <span style={{ fontWeight: "normal" }}>(default: z)</span></p>
                            <Row style={{ marginTop: "10px" }}>
                                <Col span={8} className="text-center">
                                    <Button className="direction-buttons" onClick={() => { setDirection('x') }}>X</Button>
                                </Col>
                                <Col span={8} className="text-center">
                                    <Button className="direction-buttons" onClick={() => { setDirection('y') }}>Y</Button>
                                </Col>
                                <Col span={8} className="text-center">
                                    <Button className="direction-buttons" onClick={() => { setDirection('z') }}>Z</Button>
                                </Col>
                            </Row>
                            <br />
                            <p className="latex-p" >Ratio</p>
                            <Row>
                                <Col xl={12} lg={12} md={12} sm={24} xs={24}>
                                    <div className="text-left" >
                                        <p>In order to make a successful run, the ratio must be between 0.1 and 10. </p>
                                    </div>
                                </Col>
                                <Col xl={12} lg={12} md={12} sm={24} xs={24}>
                                    <Row>
                                        <Col span={16}>
                                            <div className="text-left" >
                                                <StaticMathField style={{ border: " 1px solid", padding: "0px 4px" }}>
                                                    {roValue2}
                                                </StaticMathField>
                                            </div>
                                        </Col>
                                        <Col span={8}>
                                            {checkro ?
                                                <AppleOutlined />
                                                // <Icon type="check-circle" style={{ fontSize: '32px', marginTop: "5px" }} theme="twoTone" twoToneColor="#52c41a" />
                                                :
                                                <AppleOutlined />
                                                // <Icon type="close-circle" style={{ fontSize: '32px', marginTop: "5px" }} theme="twoTone" twoToneColor="#eb2f96" />
                                            }
                                        </Col>
                                    </Row>
                                </Col>
                            </Row>
                            <div className="text-center" style={{ marginTop: "10px" }}>
                                <Button type="primary" onClick={handleSubmit} disabled={!checkro && 'disabled'}>Run</Button>
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
                                <div style={windowWidth ? {} : { margin: "0 100px" }}>
                                    <h5>Adjust Camera</h5>
                                    <Row>
                                        <Col xl={4} lg={4} md={4} sm={24} xs={24}>
                                            <p className="text-left" style={{ marginTop: "6px" }} >Positive x-axis: </p>
                                        </Col>
                                        <Col xl={16} lg={16} md={16} sm={24} xs={24}>
                                            <Slider defaultValue={0} reverse={false} max={90} min={0}
                                                onChange={onChangePX}
                                                value={typeof pxValue === 'number' ? pxValue : 0}
                                            />
                                        </Col>
                                        <Col xl={4} lg={4} md={4} sm={24} xs={24}>
                                            <InputNumber
                                                min={0}
                                                max={90}
                                                value={pxValue}
                                                onChange={onChangePX}
                                            />
                                        </Col>
                                    </Row>
                                    <Row>
                                        <Col xl={4} lg={4} md={4} sm={24} xs={24}>
                                            <p className="text-left" style={{ marginTop: "6px" }} >Positive y-axis: </p>
                                        </Col>
                                        <Col xl={16} lg={16} md={16} sm={24} xs={24}>
                                            <Slider defaultValue={0} reverse={false} max={90} min={0}
                                                onChange={onChangePY}
                                                value={typeof pyValue === 'number' ? pyValue : 0}
                                                disabled={nyValue > 0 ? true : false}
                                            />
                                        </Col>
                                        <Col xl={4} lg={4} md={4} sm={24} xs={24}>
                                            <InputNumber
                                                min={0}
                                                max={90}
                                                value={pyValue}
                                                onChange={onChangePY}
                                                disabled={nyValue > 0 ? true : false}
                                            />
                                        </Col>
                                    </Row>
                                    <Row>
                                        <Col xl={4} lg={4} md={4} sm={24} xs={24}>
                                            <p className="text-left" style={{ marginTop: "6px" }} >Negative y-axis: </p>
                                        </Col>
                                        <Col xl={16} lg={16} md={16} sm={24} xs={24}>
                                            <Slider defaultValue={0} reverse={false} max={90} min={0}
                                                onChange={onChangeNY}
                                                value={typeof nyValue === 'number' ? nyValue : 0}
                                                disabled={pyValue > 0 ? true : false}
                                            />
                                        </Col>
                                        <Col xl={4} lg={4} md={4} sm={24} xs={24}>
                                            <InputNumber
                                                min={0}
                                                max={90}
                                                value={nyValue}
                                                onChange={onChangeNY}
                                                disabled={pyValue > 0 ? true : false}
                                            />
                                        </Col>
                                    </Row>
                                    <Row>
                                        <Col xl={4} lg={4} md={4} sm={24} xs={24}>
                                            <p className="text-left" style={{ marginTop: "6px" }} >Positive z-axis: </p>
                                        </Col>
                                        <Col xl={16} lg={16} md={16} sm={24} xs={24}>
                                            <Slider defaultValue={0} reverse={false} max={90} min={0}
                                                onChange={onChangePZ}
                                                value={typeof pzValue === 'number' ? pzValue : 0}
                                                disabled={nzValue > 0 ? true : false}
                                            />
                                        </Col>
                                        <Col xl={4} lg={4} md={4} sm={24} xs={24}>
                                            <InputNumber
                                                min={0}
                                                max={90}
                                                value={pzValue}
                                                onChange={onChangePZ}
                                                disabled={nzValue > 0 ? true : false}
                                            />
                                        </Col>
                                    </Row>
                                    <Row>
                                        <Col xl={4} lg={4} md={4} sm={24} xs={24}>
                                            <p className="text-left" style={{ marginTop: "6px" }} >Negative z-axis: </p>
                                        </Col>
                                        <Col xl={16} lg={16} md={16} sm={24} xs={24}>
                                            <Slider defaultValue={0} reverse={false} max={90} min={0}
                                                onChange={onChangeNZ}
                                                value={typeof nzValue === 'number' ? nzValue : 0}
                                                disabled={pzValue > 0 ? true : false}
                                            />
                                        </Col>
                                        <Col xl={4} lg={4} md={4} sm={24} xs={24}>
                                            <InputNumber
                                                min={0}
                                                max={90}
                                                value={nzValue}
                                                onChange={onChangeNZ}
                                                disabled={pzValue > 0 ? true : false}
                                            />
                                        </Col>
                                    </Row>

                                </div>
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
