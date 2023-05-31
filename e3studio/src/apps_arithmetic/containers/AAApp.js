import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import '../assets/css/appsArithmetic.css';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import { Layout, Row, Col, Breadcrumb, Button, Input } from 'antd';
import * as actions from '../../store/actions/auth';
import axios from 'axios';
import AppLayout from './AALayout';

import { arithapi } from '../components/appinfo';
// import funFilter from '../assets/js/funFilter';
// import odeFilter from '../assets/js/odeFilter';
// import bdFilter from '../assets/js/boundFilter';
// import checkBounds from '../assets/js/checkBounds';
// import checkCF from '../assets/js/checkCF';
// import checkDE from '../assets/js/checkDE';

import { addStyles, StaticMathField } from 'react-mathquill'

addStyles()

const { Content } = Layout;

const AMHome = (props) => {
    // 
    const [appContent, setAppContent] = useState([]);
    const [putContent, setPutContent] = useState();
    const [windowWidth, setWindowWidth] = useState(false);
    const [isDisabled, setIsDisabled] = useState(false);
    // const [invalid, setInvalid] = useState("");
    // const [isDE, setIsDE] = useState(false);
    // const [iAppName, setIAppName] = useState("");
    const [fraction, setFraction] = useState(false);

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
    const [warning0, setWarning0] = useState("");
    const [warning1, setWarning1] = useState("");
    const [warning2, setWarning2] = useState("");
    const [warning3, setWarning3] = useState("");
    const [warning4, setWarning4] = useState("");
    const [warning5, setWarning5] = useState("");
    const [warning6, setWarning6] = useState("");
    const [warning7, setWarning7] = useState("");
    const [warning8, setWarning8] = useState("");
    const [warning9, setWarning9] = useState("");

    const latexList = [latexEdit0, latexEdit1, latexEdit2, latexEdit3, latexEdit4, latexEdit5, latexEdit6, latexEdit7, latexEdit8, latexEdit9];
    const setList = [setLatexEdit0, setLatexEdit1, setLatexEdit2, setLatexEdit3, setLatexEdit4, setLatexEdit5, setLatexEdit6, setLatexEdit7, setLatexEdit8, setLatexEdit9];
    const warningList = [warning0, warning1, warning2, warning3, warning4, warning5, warning6, warning7, warning8, warning9];
    const setWarning = [setWarning0, setWarning1, setWarning2, setWarning3, setWarning4, setWarning5, setWarning6, setWarning7, setWarning8, setWarning9];

    useEffect(() => {
        if (window.innerWidth < 576) {
            setWindowWidth(true);
        } else {
            setWindowWidth(false);
        };


        // for (const [key, value] of Object.entries(appsObj)) {
        //     if (props.match.params.appname === key) {
        //         iAppNameVar = value;
        //         setIAppName(value);
        //     };
        // };

        axios.get(`/${arithapi}/api/list/`)
            .then(res => {
                for (var i in res.data) {
                    if (props.match.params.appname === res.data[i].web) {
                        // setPutContent(res.data[i]);
                        for (var j in res.data[i].webs) {
                            if (props.match.params.grade === res.data[i].webs[j]) {
                                axios.get(`/${arithapi}/api/${res.data[i].web}/${res.data[i].grades[j]}/get/`)
                                    .then(res1 => {
                                        setAppContent(res1.data);
                                        setLoaded1(true);
                                        if (res1.data.grade.includes('Fraction')) {
                                            setFraction(true);
                                        } else {
                                            setFraction(false);
                                        };
                                    });
                            };
                        };
                    };
                };
            });

        // axios.get(`/${arithapi}/api/${iAppNameVar}/`)
        //     .then(res => {
        //         setAppContent(res.data);
        //         setLoaded1(true);
        //     });

    }, [props]);

    function handleSubmit(appweb, grade, list) {
        var inputList = [];
        var regExp = /[a-zA-Z]/g;
        var remainder = grade.includes("Remainder");
        if (remainder === false) {
            for (var i in latexList) {
                if (latexList[i] === "") {
                    setWarning[i]('Required!');
                    break;
                } else if (regExp.test(latexList[i])) {
                    setWarning[i]('No letters!');
                    break;
                } else {
                    setWarning[i]('');
                    inputList[i] = list[i] + " = " + latexList[i];
                };
            };
        } else {
            for (i in latexList) {
                if (latexList[i] === "") {
                    setWarning[i]('Required!');
                    break;
                } else {
                    setWarning[i]('');
                    inputList[i] = list[i] + " = " + latexList[i];
                };
            };
        };

        if (inputList.length === 10) {
            setIsDisabled(true);
            axios.put(`/${arithapi}/api/${appweb}/${grade}/put/`, {
                input_0: inputList[0],
                input_1: inputList[1],
                input_2: inputList[2],
                input_3: inputList[3],
                input_4: inputList[4],
                input_5: inputList[5],
                input_6: inputList[6],
                input_7: inputList[7],
                input_8: inputList[8],
                input_9: inputList[9]
            }).then(res => {
                setPutContent(res.data);
                setLoaded2(true);
            });
        }

    }
    const history = useHistory();

    function handleUrl0() {
        history.push(`/`);
    };

    function handleUrl1() {
        history.push(`/apps`);
    };

    function handleUrl2() {
        history.push(`/apps/arithmetic`);
    };

    function handleUrl3(appweb) {
        history.push(`/apps/arithmetic/${appweb}`);
    };

    function handleRetry() {
        history.go(0);
    };

    function handlePrevious(appweb, previous) {
        history.push(`/apps/arithmetic/${appweb}/${previous}`);
        history.go(0);
        // if (loaded2) {
        //     history.go(0);
        // } else {
        //     for (var i in latexList) {
        //         if (latexList[i] !== "") {
        //             history.go(0);
        //         };
        //     };
        // };
    };

    function handleNext(appweb, next) {
        history.push(`/apps/arithmetic/${appweb}/${next}`);
        history.go(0);
    };

    return (
        <AppLayout loaded2={loaded2}>
            <Breadcrumb style={windowWidth ? { margin: '8px 0 8px 32px' } : { margin: '8px 0 8px 16px' }}>
                <Breadcrumb.Item className="math-app-breadcrumb" onClick={() => handleUrl0()} >Home</Breadcrumb.Item>
                <Breadcrumb.Item className="math-app-breadcrumb" onClick={() => handleUrl1()} >Apps</Breadcrumb.Item>
                <Breadcrumb.Item className="math-app-breadcrumb" onClick={() => handleUrl2()} >Arithmetic</Breadcrumb.Item>
                <Breadcrumb.Item className="math-app-breadcrumb" onClick={() => handleUrl3(appContent.appweb)} >{loaded1 && appContent.appname}</Breadcrumb.Item>
                <Breadcrumb.Item >{loaded1 && appContent.grade}</Breadcrumb.Item>
            </Breadcrumb>
            <Content className="math-app-content">
                {loaded1 &&
                    <div style={{ textAlign: "center" }}>
                        <Row>
                            {appContent.list.map((each, index) => {
                                return <div key={index}>
                                    <Col xl={12} lg={12} md={12} sm={12} xs={12}
                                        style={fraction ?
                                            { margin: "0px auto", marginTop: "10px", paddingRight: "0px", textAlign: "right" }
                                            :
                                            { margin: "10px auto", paddingRight: "0px", textAlign: "right" }
                                        }>
                                        <StaticMathField>{each} =</StaticMathField>
                                    </Col>
                                    <Col xl={1} lg={1} md={1} sm={4} xs={4}
                                        style={{ margin: "10px auto" }}>
                                        <div>
                                            <Input
                                                disabled={isDisabled}
                                                onChange={event => {
                                                    var myContext = { ilatex: event.target.value, setLatexEdit: setList[index] };
                                                    // eslint-disable-next-line
                                                    return new Function('"use strict"; this.setLatexEdit(this.ilatex)').call(myContext);
                                                }}
                                            />
                                        </div>
                                    </Col>
                                    <Col xl={11} lg={11} md={11} sm={8} xs={8}
                                        style={{ margin: "10px auto", paddingLeft: "10px", textAlign: "left" }}>
                                        <span style={{ fontSize: "small", color: "#fa7f72" }}>
                                            {warningList[index] !== "" && warningList[index]}
                                        </span>
                                        {loaded2 &&
                                            <div>
                                                {putContent.check[index] === 'check' ?
                                                    <div>
                                                        {/* <Icon type={putContent.check[index]} style={{ color: "green" }} /> */}
                                                        <span style={{ fontSize: "small", color: "green" }}>
                                                            &nbsp; &nbsp; Answer: {putContent.answer[index]}
                                                        </span>
                                                    </div>
                                                    :
                                                    <div>
                                                        {/* <Icon type={putContent.check[index]} style={{ color: "red" }} /> */}
                                                        <span style={{ fontSize: "small", color: "red" }}>
                                                            &nbsp; &nbsp; Answer: {putContent.answer[index]}
                                                        </span>
                                                    </div>
                                                }
                                            </div>
                                        }
                                    </Col>
                                </div>
                            })}
                        </Row>
                        <br />
                        <Row>
                            {loaded2 &&
                                <Col span={24}>
                                    <h6>Score: {putContent.score}</h6>
                                    <br />
                                </Col>
                            }
                            <br />
                            <Col span={12}>
                                <div className="text-right" style={{ paddingRight: "20px" }}>
                                    {fraction ?
                                        <Button type="primary" onClick={() => handleSubmit(appContent.appweb, appContent.grade, appContent.listab)}>Submit</Button>
                                        :
                                        <Button type="primary" onClick={() => handleSubmit(appContent.appweb, appContent.grade, appContent.list)}>Submit</Button>
                                    }
                                </div>
                            </Col>
                            <Col span={12}>
                                <div className="text-left" style={{ paddingLeft: "20px" }}>
                                    {loaded2 ?
                                        <Button type="primary" onClick={() => handleRetry()}>Again</Button>
                                        :
                                        <Button type="primary" onClick={() => handleRetry()}>Refresh</Button>
                                    }
                                </div>
                            </Col>
                        </Row>
                        <br />
                        <Row>
                            <Col span={windowWidth ? 24 : 12} style={windowWidth ? { textAlign: "center", marginBottom: "10px" } : { textAlign: "center" }}>
                                {appContent.previous !== "none" &&
                                    <Button onClick={() => { handlePrevious(appContent.appweb, appContent.prev_web) }}>{'<< '} {appContent.previous} </Button>
                                }

                            </Col>
                            <Col span={windowWidth ? 24 : 12} style={windowWidth ? { textAlign: "center", marginTop: "10px" } : { textAlign: "center" }}>
                                {appContent.next !== "none" &&
                                    <Button onClick={() => { handleNext(appContent.appweb, appContent.next_web) }}>{appContent.next} {'>>'}</Button>
                                }
                            </Col>
                        </Row>
                    </div>

                }
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
