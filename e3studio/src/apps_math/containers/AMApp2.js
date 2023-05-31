import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import { Layout, Row, Col, Breadcrumb, Button, Input } from 'antd';
import * as actions from '../../store/actions/auth';
import axios from 'axios';
import AppLayout from './AMLayout';

import { appapi } from '../components/appinfo';
import odeFilter from '../assets/js/odeFilter';
import bdFilter from '../assets/js/boundFilter';
import checkBounds from '../assets/js/checkBounds';
import checkDE from '../assets/js/checkDE';

import { addStyles, EditableMathField, StaticMathField } from 'react-mathquill'

addStyles()

const { Content } = Layout;

const AMHome = (props) => {
    // 
    const [appContent, setAppContent] = useState([]);
    const [imgContent, setImgContent] = useState();
    const [windowWidth, setWindowWidth] = useState(false);
    const [invalid, setInvalid] = useState("");
    // const [isDE, setIsDE] = useState(false);
    // const [iAppName, setIAppName] = useState("");
    const [warning0, setWarning0] = useState("");
    // eslint-disable-next-line
    const [warning1, setWarning1] = useState("");
    const [warning2, setWarning2] = useState("");
    const [warning3, setWarning3] = useState("");
    const [warning4, setWarning4] = useState("");
    // eslint-disable-next-line
    const [warning5, setWarning5] = useState("");
    // eslint-disable-next-line
    const [warning6, setWarning6] = useState("");
    const [loaded1, setLoaded1] = useState(false);
    const [loaded2, setLoaded2] = useState(false);

    const [latexEdit0, setLatexEdit0] = useState("");
    const [latexEdit1, setLatexEdit1] = useState("");
    const [latexEdit2, setLatexEdit2] = useState("");
    const [latexEdit3, setLatexEdit3] = useState("");
    const [latexEdit4, setLatexEdit4] = useState("");
    const [latexEdit5, setLatexEdit5] = useState("");
    const [latexEdit6, setLatexEdit6] = useState("");
    const [latexEdit7, setLatexEdit7] = useState("");
    const [latexEdit8, setLatexEdit8] = useState("");
    const [latexEdit9, setLatexEdit9] = useState("");
    const [latexEdit10, setLatexEdit10] = useState("");
    const [latexEdit11, setLatexEdit11] = useState("");
    const [latexEdit12, setLatexEdit12] = useState("");

    const latexList = [latexEdit0, latexEdit1, latexEdit2, latexEdit3, latexEdit4, latexEdit5, latexEdit6, latexEdit7, latexEdit8, latexEdit9, latexEdit10, latexEdit11, latexEdit12];
    const setList = [setLatexEdit0, setLatexEdit1, setLatexEdit2, setLatexEdit3, setLatexEdit4, setLatexEdit5, setLatexEdit6, setLatexEdit7, setLatexEdit8, setLatexEdit9, setLatexEdit10, setLatexEdit11, setLatexEdit12];

    useEffect(() => {

        if (window.innerWidth < 576) {
            setWindowWidth(true);
        } else {
            setWindowWidth(false);
        };

        // var iAppNameVar = "";
        // for (const [key, value] of Object.entries(appsObj)) {
        //     if (props.match.url.includes(key)) {
        //         iAppNameVar = value;
        //         setIAppName(value);
        //     };
        //     if (!props.match.url.includes('commonfunctions')) {
        //         setIsDE(true);
        //     } else {
        //         setIsDE(false);
        //     };
        // };


        axios.get(`/${appapi}/api/Initial Value Problems/`)
            .then(res => {
                setAppContent(res.data);
                setLoaded1(true);
            });

    }, [props.match]);

    function handleSubmit(event, option) {
        event.preventDefault();

        var proceed0 = false;
        // eslint-disable-next-line
        var proceed1 = false;
        var proceed2 = false;
        var proceed3 = false;
        var proceed4 = false;
        var proceed5 = false;
        var proceed6 = false;
        var valueIFV;
        var valueIDV;
        var valueLB;
        var valueRB;


        if (latexEdit0 !== "") {
            setWarning0();
            var pyFunc = odeFilter(latexEdit0);
            proceed0 = true;
        } else {
            setWarning0("This is required. Please enter your ODE.")
        };

        var forxvalue = "";
        if (option === '5') {
            forxvalue = checkBounds(bdFilter(event.target.value));
        }

        var foryvalue = "";
        if (option === '6') {
            foryvalue = checkBounds(bdFilter(event.target.value));
        }




        if (latexEdit2 === "") {
            setWarning2("This intial value is required.");
        } else {
            setWarning2("");
            valueIFV = checkBounds(bdFilter(latexEdit2));
        };

        if (latexEdit0 === "") {
            setWarning3("");
        } else if (pyFunc[1] === '2' && latexEdit3 === "") {
            setWarning3("This is required for 2nd order ODE.")
        } else if (pyFunc[1] === '2' && latexEdit3 !== "") {
            setWarning3("");
            valueIDV = checkBounds(bdFilter(latexEdit3));
        }
        // eslint-disable-next-line
        else if (pyFunc[1] === '1' && latexEdit3 !== ""); {
            setLatexEdit3("");
        }

        if (latexEdit4 === "") {
            setWarning4("This is required. Please enter your initial parameter.")
        } else {
            setWarning4("");
            valueLB = checkBounds(bdFilter(latexEdit4));
        };

        if (latexEdit5 === "") {
            proceed5 = true;
        } else {
            valueRB = checkBounds(bdFilter(latexEdit5));
        };

        if (isNaN(valueIFV)) {
            setWarning2(valueIFV);
        } else {
            proceed2 = true;
            setWarning2("");
        };

        if (latexEdit3 !== "" && isNaN(valueIDV)) {
            setWarning3(valueIDV);
        } else {
            proceed3 = true;
            setWarning3("");
        };


        if (!proceed4 && isNaN(valueLB)) {
            setWarning4(valueLB);
        } else if (!proceed5 && isNaN(valueRB)) {
            setWarning5(valueRB);
        } else if (valueLB < valueRB) {
            setWarning4("");
            setWarning5("");
            proceed4 = true;
            proceed5 = true;
        } else if (valueLB >= valueRB) {
            setWarning4('Left bound must be less than right bound.');
            setWarning5('Left bound must be less than right bound.');
        } else {
            proceed4 = true;
            proceed5 = true;
        };

        var latexTitle = latexEdit6;
        if (latexEdit6 === "") {
            latexTitle = latexEdit0;
        };

        if (proceed0 && proceed2 && proceed3 && proceed4 && proceed5) {
            pyFunc = odeFilter(latexEdit0);
            proceed6 = checkDE(pyFunc[0], pyFunc[1]);
        };

        if (latexEdit0 === "") {
            setWarning0("This is required. Please enter your ODE.")
        } else if (latexEdit2 === "") {
            setWarning2("This is required. Please enter your intial value y0.")
        } else if (latexEdit4 === "") {
            setWarning4("This is required. Please enter your intial paramater t0.")
        } else if (proceed6 !== true) {
            setWarning0(proceed6);
        } else {
            setWarning2("");
            setWarning4("");
            axios.put(`/${appapi}/api/Initial Value Problems/put/`, {
                equation: pyFunc,
                parameter: latexEdit1,
                ifv: bdFilter(latexEdit2),
                idv: bdFilter(latexEdit3),
                left_bound: bdFilter(latexEdit4),
                right_bound: bdFilter(latexEdit5),
                title: latexTitle,
                hlabel: latexEdit7,
                vlabel: latexEdit8,
                option: option,
                forxvalue: forxvalue,
                foryvalue: foryvalue,
            }).then(res => {
                window.stop();
                setImgContent(res.data);
                setLoaded2(true);
                // setImageHash(Date.now());
                var index = 0;
                for (const [key] of Object.entries(res.data)) {
                    setList[index](res.data[key])
                    if (index === 0) {
                        setList[index](latexEdit0)
                    }
                    if (index === 2 && res.data[key].includes("np")) {
                        setList[index](latexEdit2)
                    } else if (index === 3 && res.data[key].includes("np")) {
                        setList[index](latexEdit3)
                    };
                    index++;
                };
            }).catch(error => {
                setInvalid(error.response.data.message);
                // state.invalid = error.response.data.message;
                // forceUpdate();
            });
        };



    };

    const history = useHistory();

    function handleUrl0() {
        history.push(`/`);
    };

    function handleUrl1() {
        history.push(`/apps`);
    };

    function handleUrl2() {
        history.push(`/apps/math`);
    };

    return (

        <AppLayout>
            <Breadcrumb style={windowWidth ? { margin: '8px 0 8px 32px' } : { margin: '8px 0 8px 16px' }}>
                <Breadcrumb.Item className="math-app-breadcrumb" onClick={() => handleUrl0()} >Home</Breadcrumb.Item>
                <Breadcrumb.Item className="math-app-breadcrumb" onClick={() => handleUrl1()} >Apps</Breadcrumb.Item>
                <Breadcrumb.Item className="math-app-breadcrumb" onClick={() => handleUrl2()} >Math</Breadcrumb.Item>
                <Breadcrumb.Item >{loaded1 && appContent[0].appname}</Breadcrumb.Item>
            </Breadcrumb>
            <Content className="math-app-content">
                <Row>
                    <Col xl={10} lg={10} md={10} sm={24} xs={24}>
                        {loaded1 &&

                            // eslint-disable-next-line
                            appContent.map((item, index) => {
                                if (index === 2 || index === 4) {
                                    return <Row key={index}>
                                        <Col xl={12} lg={12} md={12} sm={24} xs={24}>
                                            <div style={windowWidth ? {} : { marginLeft: "60px" }} key={index}>
                                                <p className="latex-p" >{item.name}</p>
                                                <EditableMathField
                                                    className="latex-fields form-control"
                                                    latex={loaded2 ? latexList[index] : latexList[index]} // latex value for the input field
                                                    onChange={(mathField,) => {
                                                        var myContext = { ilatex: mathField.latex(), setLatexEdit: setList[index] };
                                                        // eslint-disable-next-line
                                                        return new Function(item.latex).call(myContext);
                                                    }}
                                                />
                                                <p className="latex-note">
                                                    <span dangerouslySetInnerHTML={{ __html: item.note }} />&nbsp;
                                                    <span style={{ color: "#d9534f" }}>
                                                        {index === 2 && warning2}
                                                        {index === 4 && warning4}
                                                    </span>
                                                </p>
                                                <span>{index === 3 && warning3}</span>
                                            </div>
                                        </Col>
                                        <Col xl={12} lg={12} md={12} sm={24} xs={24}>
                                            <div style={windowWidth ? {} : { marginLeft: "20px" }} key={index + 1}>
                                                <p className="latex-p" >{appContent[index + 1].name}</p>
                                                <EditableMathField
                                                    className="latex-fields form-control"
                                                    latex={loaded2 ? latexList[index + 1] : latexList[index + 1]} // latex value for the input field
                                                    onChange={(mathField,) => {
                                                        var myContext = { ilatex: mathField.latex(), setLatexEdit: setList[index + 1] };
                                                        // eslint-disable-next-line
                                                        return new Function(appContent[index + 1].latex).call(myContext);
                                                    }}
                                                />
                                                <p className="latex-note">
                                                    <span dangerouslySetInnerHTML={{ __html: appContent[index + 1].note }} />&nbsp;
                                                    <span style={{ color: "#d9534f" }}>
                                                        {index + 1 === 3 && warning3}
                                                    </span>
                                                </p>

                                                <span>{index === 3 && warning3}</span>
                                            </div>
                                        </Col>
                                    </Row>
                                }
                                else if (index !== 3 && index !== 5) {
                                    return <div style={windowWidth ? {} : { marginLeft: "60px" }} key={index}>
                                        <p className="latex-p" >{item.name}</p>
                                        <EditableMathField
                                            className="latex-fields form-control"
                                            latex={loaded2 ? latexList[index] : latexList[index]} // latex value for the input field
                                            onChange={(mathField,) => {
                                                var myContext = { ilatex: mathField.latex(), setLatexEdit: setList[index] };
                                                // eslint-disable-next-line
                                                return new Function(item.latex).call(myContext);
                                            }}
                                        />
                                        <p className="latex-note">{item.note}&nbsp;
                                    <span style={{ color: "#d9534f" }}>
                                                {index === 0 && warning0}
                                                {index === 2 && warning2}
                                                {index === 3 && warning3}
                                                {index === 4 && warning4}
                                            </span>
                                        </p>
                                        {/* <span></span> */}
                                        <span>{index === 3 && warning3}</span>
                                        {index === appContent.length - 1 &&
                                            <div className="text-center" >
                                                <Button type="primary" onClick={(event) => handleSubmit(event, '0')}>Submit</Button>
                                            </div>
                                        }
                                    </div>

                                }
                            })
                        }
                    </Col>

                    <Col xl={14} lg={14} md={14} sm={24} xs={24} style={{ textAlign: "center" }}>
                        {!loaded2 && <h3 style={windowWidth ? { marginTop: "50px" } : {}}>Figure to be Loaded Here</h3>}
                        {loaded2 &&
                            <div>
                                <p>{invalid}</p>
                                <div>
                                    <img id="figure" alt=""
                                        src={imgContent.figure}
                                        style={windowWidth ? { width: "100%" } : {}}
                                    />
                                </div>
                                <br />
                                <br />
                                <div style={windowWidth ? {} : { margin: "0 200px" }}>
                                    <Row >
                                        <Col xl={6} lg={6} md={6} sm={24} xs={24}>
                                            <Button type="primary" onClick={(event) => handleSubmit(event, '1')}>Get y and y'</Button>
                                            <br />
                                            <br />
                                        </Col>
                                        <Col xl={6} lg={6} md={6} sm={24} xs={24}>
                                            <Button type="primary" className="fig-buttons" onClick={(event) => handleSubmit(event, '3')}>Get y' and y''</Button>
                                            <br />
                                            <br />
                                        </Col>
                                        <Col xl={6} lg={6} md={6} sm={24} xs={24}>
                                            <Button type="primary" onClick={(event) => handleSubmit(event, '2')}>Get y and y''</Button>
                                            <br />
                                            <br />
                                        </Col>
                                        <Col xl={6} lg={6} md={6} sm={24} xs={24}>
                                            <Button type="primary" className="fig-buttons" onClick={(event) => handleSubmit(event, '4')}>Get y, y' and y''</Button>
                                            <br />
                                            <br />
                                        </Col>
                                    </Row>
                                    <div>
                                        <Row >
                                            <Col xl={6} lg={6} md={6} sm={24} xs={24}>
                                                <p style={windowWidth ? { margin: "auto 60px" } : { margin: "auto 30px" }}>
                                                    For x = <Input onPressEnter={(event) => handleSubmit(event, '5')} />
                                                </p>
                                                <br />
                                                <br />
                                            </Col>
                                            <Col xl={6} lg={6} md={6} sm={24} xs={24}>
                                                <p style={windowWidth ? { margin: "auto 60px" } : { margin: "auto 30px" }}>
                                                    Find y =
                                                </p>
                                                <StaticMathField className="latex-input-find" style={{ backgroundColor: "white", color: "black" }}>
                                                    {loaded2 && imgContent.forxvalue}
                                                </StaticMathField>
                                                <br />
                                                <br />
                                            </Col>
                                            <Col xl={6} lg={6} md={6} sm={24} xs={24}>
                                                <p style={windowWidth ? { margin: "auto 60px" } : { margin: "auto 30px" }}>
                                                    For y = <Input onPressEnter={(event) => handleSubmit(event, '6')} />
                                                </p>
                                                <br />
                                                <br />
                                            </Col>
                                            <Col xl={6} lg={6} md={6} sm={24} xs={24}>
                                                <p style={windowWidth ? { margin: "auto 60px" } : { margin: "auto 30px" }}>
                                                    Find x =
                                                </p>
                                                <StaticMathField className="latex-input-find" style={{ backgroundColor: "white", color: "black" }}>
                                                    {loaded2 && imgContent.foryvalue}
                                                </StaticMathField>
                                                <br />
                                                <br />
                                            </Col>
                                        </Row>
                                    </div>
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
