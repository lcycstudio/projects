import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import '../assets/css/p11home.css';
import { Button, Row, Col, Breadcrumb, Card } from 'antd';
import { connect } from 'react-redux';
import { withRouter, useHistory } from 'react-router-dom';
import * as actions from '../../store/actions/auth';
import axios from 'axios';
import P11Section from './P11Section';

import { addStyles, StaticMathField } from 'react-mathquill';
import { MathComponent } from 'mathjax-react';
import { coursetitle, courseapi } from '../components/courseinfo';


addStyles()

const P11Content = (props) => {
    const [content, setContent] = useState();
    const [exercise, setExercise] = useState();
    const [answer, setAnswer] = useState();
    const [loaded, setLoaded] = useState(false);


    useEffect(() => {
        var chapter = props.match.params.chapter.replace(/\s/g, '').replace('%20', '').toLowerCase();
        var section = props.match.params.section.replace(/\s/g, '').replace('%20', '').toLowerCase();
        axios.get(`/${courseapi}/api/list/`)
            .then(res1 => {
                let allchapter = res1.data;
                for (var i in allchapter) {
                    if (allchapter[i].chapter.replace(/\s/g, '').toLowerCase() === chapter) {
                        let ichapter = allchapter[i].chapter;
                        axios.get(`/${courseapi}/api/${ichapter}/`)
                            .then(res2 => {
                                let allsection = res2.data.sections;
                                for (var j in allsection) {
                                    if (allsection[j].replace(/\s/g, '').toLowerCase() === section) {
                                        if (section === 'exercises') {
                                            axios.get(`/${courseapi}/api/${ichapter}/${allsection[j]}/exercises/`)
                                                .then(res3 => {
                                                    setExercise(res3.data);
                                                    setContent();
                                                    setLoaded(true);
                                                });
                                            props.seturl(`${courseapi}/api/${ichapter}/${j}`);
                                        } else {
                                            axios.get(`/${courseapi}/api/${ichapter}/${allsection[j]}/content/`)
                                                .then(res3 => {
                                                    setContent(res3.data);
                                                    setExercise();
                                                    setLoaded(true);
                                                });
                                            props.seturl(`${courseapi}/api/${ichapter}/${j}`);
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

    return (
        <P11Section>
            {loaded ?
                <div id="iSection" className="main-content" style={{ width: "1200px", margin: "0 auto", backgroundColor: "white" }}>
                    {exercise ?
                        <Breadcrumb style={{ padding: '12px 0 20px 0' }}>
                            <Breadcrumb.Item onClick={() => handleUrl1()} className="section-item">{coursetitle}</Breadcrumb.Item>
                            <Breadcrumb.Item onClick={() => handleUrl2(exercise.chapter)} className="section-item">Chapter {exercise.chapterID}: {exercise.chapter}</Breadcrumb.Item>
                            <Breadcrumb.Item >{exercise.section}</Breadcrumb.Item>
                        </Breadcrumb>
                        :
                        <Breadcrumb style={{ padding: '12px 0 20px 0' }}>
                            <Breadcrumb.Item onClick={() => handleUrl1()} className="section-item">{coursetitle}</Breadcrumb.Item>
                            <Breadcrumb.Item onClick={() => handleUrl2(content.chapter)} className="section-item">Chapter {content.chapterID}: {content.chapter}</Breadcrumb.Item>
                            <Breadcrumb.Item >{content.section}</Breadcrumb.Item>
                        </Breadcrumb>

                    }
                    {exercise ?
                        <div>
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
                                                    <br />
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
                            <h4>{content.section}</h4>
                            <br />
                            {content.paragraphs && content.paragraphs.map((each, index) => {
                                return <div key={index}>
                                    <div dangerouslySetInnerHTML={{ __html: content.paragraphs[index] }} />
                                    <br />
                                    {content.equations[index] &&
                                        <div style={{ textAlign: "center" }}>
                                            <MathComponent tex={content.equations[index]} />
                                        </div>
                                    }
                                    {content.images[index] &&
                                        <Card
                                            cover={<img src={content.images[index]} style={{ margin: "0 auto", width: "500px" }} alt="" />}
                                            style={{ textAlign: "center", border: "0" }}
                                        >
                                            <span style={{ fontWeight: "500", fontSize: "1rem" }}>Figure {content.chapterID}.{content.id}.{content.imageIndex[index]} {content.captions[index]}</span>
                                        </Card>
                                    }
                                    <br />
                                </div>
                            })}
                            <br />
                        </div>
                    }
                    {exercise ?
                        <Row>
                            <Col span={12}>
                                {exercise.previous !== "none" &&
                                    <Button onClick={() => { handlePrevious(exercise.chapter, exercise.previous) }}>{'<< '} {exercise.previous} </Button>
                                }
                            </Col>
                            <Col span={12} style={{ textAlign: "right" }}>
                                {exercise.next !== "none" &&
                                    <Button onClick={() => { handleNext(exercise.chapter, exercise.next) }}>{exercise.next} {'>>'}</Button>
                                }
                            </Col>
                        </Row>
                        :
                        <Row>
                            <Col span={12}>
                                {content.previous !== "none" &&
                                    <Button onClick={() => { handlePrevious(content.chapter, content.previous) }}>{'<< '} {content.previous} </Button>
                                }
                            </Col>
                            <Col span={12} style={{ textAlign: "right" }}>
                                {content.next !== "none" &&
                                    <Button onClick={() => { handleNext(content.chapter, content.next) }}>{content.next} {'>>'}</Button>
                                }
                            </Col>
                        </Row>
                    }
                    <br />
                    <br />
                </div>
                :
                <div className="text-center">
                    <Icon type="loading" style={{ color: "blue" }} />
                </div>
            }
        </P11Section>
    );
}


const mapStateToProps = (state) => {
    return {
        token: state.token,
    }
};

const mapDispatchToProps = dispatch => {
    return {
        logout: () => dispatch(actions.authLogout()),
        seturl: (thisurl) => dispatch(actions.setUrl(thisurl))
    }
};

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(P11Content));

