import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import '../assets/css/mlhome.css';
import { Button, Row, Col, Breadcrumb } from 'antd';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import * as actions from '../../store/actions/auth';
import axios from 'axios';

import MLSection from './MLSection';
import { addStyles, StaticMathField } from 'react-mathquill';
// import { MathComponent } from 'mathjax-react';
// import { coursetitle, courseapi } from '../components/courseinfo';
import courseObj from '../../url/courseObj';

addStyles()

const MLContent = (props) => {
    const [content, setContent] = useState();
    const [exercise, setExercise] = useState();
    const [answer, setAnswer] = useState();
    const [loaded, setLoaded] = useState(false);
    const [setWidth, setSetWidth] = useState(false);
    const [coursetitle, setCourseTitle] = useState();
    const [courseapi, setCourseApi] = useState();


    useEffect(() => {
        if (window.innerWidth < 576) {
            setSetWidth(true);
        } else {
            setSetWidth(false);
        };

        // var courseTitle;
        var courseAPI;
        for (const [key, value] of Object.entries(courseObj)) {
            if (key === props.match.params.subject) {
                // courseTitle = value;
                courseAPI = key;
                setCourseTitle(value);
                setCourseApi(key);
            };
        };

        var chapter = props.match.params.chapter.replace(/\s/g, '').replace('%20', '').toLowerCase();
        var section = props.match.params.section.replace(/\s/g, '').replace('%20', '').toLowerCase();

        axios.get(`/${courseAPI}/api/list/`)
            .then(res1 => {
                let allchapter = res1.data;
                for (var i in allchapter) {
                    if (allchapter[i].chapter.replace(/\s/g, '').toLowerCase() === chapter) {
                        let ichapter = allchapter[i].chapter;
                        axios.get(`/${courseAPI}/api/${ichapter}/`)
                            .then(res2 => {
                                let allsection = res2.data.sections;
                                for (var j in allsection) {
                                    if (allsection[j].replace(/\s/g, '').toLowerCase() === section) {
                                        if (section === 'exercises') {
                                            axios.get(`/${courseAPI}/api/${ichapter}/${allsection[j]}/exercises/`)
                                                .then(res3 => {
                                                    setExercise(res3.data);
                                                    setContent();
                                                    setLoaded(true);
                                                });
                                            props.seturl(`${courseAPI}/api/${ichapter}/${j}`);
                                        } else {
                                            axios.get(`/${courseAPI}/api/${ichapter}/${allsection[j]}/content/`)
                                                .then(res3 => {
                                                    setContent(res3.data);
                                                    setExercise();
                                                    setLoaded(true);
                                                });
                                            props.seturl(`${courseAPI}/api/${ichapter}/${j}`);
                                        }
                                    }
                                }
                            });
                    }
                }
            });
    }, [props.match.params.chapter, props.match.params.section, props]);

    function handleChoice(chapter, index, choice) {
        var id = index + 1;
        axios.put(`/${courseapi}/api/${chapter}/Exercises/put/${id}/`, {
            answer: choice,
        }).then(res4 => {
            setAnswer(res4.data);
            setLoaded(true);
        })
    };

    function handleDisable(answer, choice) {
        if (answer !== undefined && answer.answer === choice) {
            return true
        }
    };

    const history = useHistory();

    function handleUrl1() {
        history.push(`/courses/${courseapi}`);
    };

    function handleUrl2(chapter) {
        history.push(`/courses/${courseapi}/${chapter}`.replace(/\s/g, '').toLowerCase());
    };

    function handlePrevious(chapter, previous) {
        history.push(`/courses/${courseapi}/${chapter}/${previous}`.replace(/\s/g, '').toLowerCase());
        var element = document.getElementById("iSection");
        element.scrollIntoView();
    };

    function handleNext(chapter, next) {
        history.push(`/courses/${courseapi}/${chapter}/${next}`.replace(/\s/g, '').toLowerCase());
        var element = document.getElementById("iSection");
        element.scrollIntoView();
    };

    // const input = React.createRef();

    // function handleSubmit(chapter, section, index, e) {
    //     e.preventDefault();
    //     if (input.current.value.includes("plt.")) {
    //         setDisable(true);
    //     };
    //     var id = index + 1;
    //     axios.put(`/${courseapi}/api/${chapter}/${section}/coding/${id}/`, {
    //         code: input.current.value,
    //     }).then(res => {
    //         axios.get(`/${courseapi}/api/${chapter}/${section}/content/`)
    //             .then(res2 => {
    //                 setContent(res2.data);
    //                 setLoaded(true);
    //             });
    //     });
    // };

    // function handleEnter(chapter, section, index, e) {
    //     if (e.key === "Enter" && e.altKey) {
    //         var id = index + 1;
    //         axios.put(`/${courseapi}/api/${chapter}/${section}/coding/${id}/`, {
    //             code: input.current.value,
    //         }).then(res => {
    //             axios.get(`/${courseapi}/api/${chapter}/${section}/content/`)
    //                 .then(res2 => {
    //                     setContent(res2.data);
    //                     setLoaded(true);
    //                 });
    //         });
    //     };
    // };

    return (
        <MLSection>
            {loaded &&
                <div id="iSection" className="main-content" style={{ maxWidth: "1200px", margin: "0 auto", backgroundColor: "white" }}>
                    {exercise ?
                        <Breadcrumb style={setWidth ? { margin: '8px 0 8px 32px' } : { margin: '8px 0 8px 16px' }}>
                            <Breadcrumb.Item onClick={() => handleUrl1()} className="section-item">{coursetitle}</Breadcrumb.Item>
                            <Breadcrumb.Item onClick={() => handleUrl2(exercise.chapter)} className="section-item">Chapter {exercise.chapterID}: {exercise.chapter}</Breadcrumb.Item>
                            <Breadcrumb.Item >{exercise.section}</Breadcrumb.Item>
                        </Breadcrumb>
                        :
                        <Breadcrumb style={setWidth ? { margin: '8px 0 8px 32px' } : { margin: '8px 0', marginLeft: "1.3%" }}>
                            <Breadcrumb.Item onClick={() => handleUrl1()} className="section-item">{coursetitle}</Breadcrumb.Item>
                            <Breadcrumb.Item onClick={() => handleUrl2(content.chapter)} className="section-item">{content.chapter}</Breadcrumb.Item>
                            <Breadcrumb.Item >{content.section}</Breadcrumb.Item>
                        </Breadcrumb>
                    }
                    {/* <br /> */}
                    {exercise ?
                        <div>
                            <br />
                            <h4>{exercise.section}</h4>
                            <br />
                            {exercise.exercises && exercise.exercises.map((each, index) => {
                                return <div key={index}>
                                    <div dangerouslySetInnerHTML={{ __html: exercise.exercises[index] }} />
                                    <br />
                                    {answer &&
                                        <div>
                                            {answer.comment_1 ?
                                                <div>
                                                    {answer.comment_1 &&
                                                        <div>
                                                            <div dangerouslySetInnerHTML={{ __html: answer.comment_1 }} />
                                                            <br />
                                                        </div>
                                                    }
                                                    {answer.equation_1 &&
                                                        <div>
                                                            <StaticMathField style={{ border: "1px solid", padding: "20px 20px" }}>
                                                                {answer.equation_1}
                                                            </StaticMathField>
                                                            <br />
                                                        </div>
                                                    }

                                                    {answer.comment_2 &&
                                                        <div>
                                                            <div dangerouslySetInnerHTML={{ __html: answer.comment_2 }} />
                                                            <br />
                                                        </div>
                                                    }
                                                    <br />
                                                    {answer.equation_2 &&
                                                        <div>
                                                            <StaticMathField style={{ border: "1px solid", padding: "20px 20px" }}>
                                                                {answer.equation_2}
                                                            </StaticMathField>
                                                            <br />
                                                        </div>
                                                    }
                                                </div>
                                                :
                                                <div>
                                                    <p>{answer}</p>
                                                </div>
                                            }
                                        </div>
                                    }
                                    <Button className="exercise-button" style={{ marginRight: "20px", fontWeight: "600" }} onClick={() => handleChoice(exercise.chapter, index, 'A')} disabled={handleDisable(answer, 'A')}><div dangerouslySetInnerHTML={{ __html: exercise.choices[index][0] }} /></Button>
                                    <Button className="exercise-button" style={{ margin: "0 20px", fontWeight: "600" }} onClick={() => handleChoice(exercise.chapter, index, 'B')} disabled={handleDisable(answer, 'B')}><div dangerouslySetInnerHTML={{ __html: exercise.choices[index][1] }} /></Button>
                                    <Button className="exercise-button" style={{ marginLeft: "20px", fontWeight: "600" }} onClick={() => handleChoice(exercise.chapter, index, 'C')} disabled={handleDisable(answer, 'C')}><div dangerouslySetInnerHTML={{ __html: exercise.choices[index][2] }} /></Button>
                                    <br />
                                </div>

                            })}
                            <br />
                            <br />
                        </div>
                        :
                        <div >
                            {/* <h4>{content.section}</h4>
                            <br /> */}
                            {content.images && content.images.map((each, index) => {
                                return <div key={index}>
                                    {content.images[index] &&
                                        <div style={{ width: "100%" }}>
                                            <img src={content.images[index]}
                                                style={{ width: "100%" }} alt=""
                                                onContextMenu={(e) => { e.preventDefault() }}
                                                onMouseDown={(e) => { e.preventDefault() }}
                                            />
                                        </div>
                                    }
                                    <div style={{ fontFamily: "Times New Roman", fontSize: "1.1rem" }} dangerouslySetInnerHTML={{ __html: content.paragraphs[index] }} />
                                    {/* <br /> */}
                                    {/* {content.codetexts[index] &&
                                        <form onSubmit={(e) => handleSubmit(content.chapter, content.section, index, e)}>
                                            <label>
                                                In [{index + 1}]:
                                            </label>
                                            <textarea
                                                defaultValue={content.codetexts[index]}
                                                // value={content.codetexts[index]}
                                                ref={input}
                                                style={{ width: "100%", height: "100px", border: "0.1px solid", padding: "5px 10px" }}
                                                // onChange={handleChange}
                                                onKeyDown={(e) => handleEnter(content.chapter, content.section, index, e)}
                                            />
                                            <input type="submit" value="Submit" className="submit-button" disabled={disable} />
                                        </form>
                                    }
                                    {content.plots[index] &&
                                        <div>
                                            <p style={{ marginBottom: "5px" }}>Out [{index + 1}]:</p>
                                            <div style={{ border: "0.1px solid" }}>
                                                <img src={`mediafiles/${content.plots[index]}`} style={{ width: "500px" }} alt="" />
                                            </div>
                                        </div>
                                    }
                                    {content.values[index] &&
                                        <div>
                                            <p style={{ marginBottom: "5px" }}>Out [{index + 1}]:</p>
                                            <div style={{ border: "0.1px solid" }}>
                                                <p style={{ padding: "5px 10px" }}>{content.values[index]}</p>
                                            </div>
                                        </div>
                                    }

                                    {content.equations[index] &&
                                        <div style={{ textAlign: "center" }}>
                                            <MathComponent tex={content.equations[index]} />
                                        </div>
                                    } */}
                                    {/* <br /> */}
                                </div>
                            })}
                            <br />
                        </div>
                    }
                    {exercise ?
                        <Row>
                            <Col span={setWidth ? 24 : 12} style={setWidth ? { textAlign: "center", marginBottom: "10px" } : { textAlign: "left" }}>
                                {exercise.previous !== "none" &&
                                    <Button onClick={() => { handlePrevious(exercise.chapter, exercise.previous) }}>{'<< '} {exercise.previous} </Button>
                                }

                            </Col>
                            <Col span={setWidth ? 24 : 12} style={setWidth ? { textAlign: "center", marginTop: "10px" } : { textAlign: "right" }}>
                                {exercise.next !== "none" &&
                                    <Button onClick={() => { handleNext(exercise.chapter, exercise.next) }}>{exercise.next} {'>>'}</Button>
                                }
                            </Col>
                        </Row>
                        :
                        <Row>
                            <Col span={setWidth ? 24 : 12} style={setWidth ? { textAlign: "center", marginBottom: "10px" } : { textAlign: "left" }}>
                                {content.previous !== "none" &&
                                    <Button onClick={() => { handlePrevious(content.chapter, content.previous) }}>{'<< '} {content.previous} </Button>
                                }

                            </Col>
                            <Col span={setWidth ? 24 : 12} style={setWidth ? { textAlign: "center", marginTop: "10px" } : { textAlign: "right" }}>
                                {content.next !== "none" &&
                                    <Button onClick={() => { handleNext(content.chapter, content.next) }}>{content.next} {'>>'}</Button>
                                }
                            </Col>
                        </Row>
                    }
                    <br />
                    <br />
                </div>
            }
        </MLSection>
    );
}


const mapStateToProps = (state) => {
    return {
        loading: state.loading,
        token: state.token,
    }
};

const mapDispatchToProps = dispatch => {
    return {
        logout: () => dispatch(actions.authLogout()),
        seturl: (thisurl) => dispatch(actions.setUrl(thisurl))
    }
};

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(MLContent));

