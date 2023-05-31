//var eqx = "y=\\frac{x^{\\frac{2}{3}}}{3}+\\ln\\left(x^3+2\\right)+3+\\sin x+\\arctan x";

var functionFilter = function (eqx, param) {
  // eslint-disable-next-line
  var symList1 = ["\\frac{", "\}\{", "\\left(", "\\right)", "e^", "\^", "\{", "\}", "\\pi", "\\cdot"];
  // eslint-disable-next-line
  var symList2 = ["(", ")/(", "(", ")", "np.exp(", "\*\*", "(", ")", "np.pi", "*"];
  var funcList = []; // function list in Latex
  funcList.push("\\arccos", "\\arcsin", "\\arctan", "\\cos", "\\cosh", "\\cot",
    "\\coth", "\\sqrt", "\\csc", "\\exp", "\\ln", "\\log", "\\sec", "\\sin",
    "\\sinh", "\\tan", "\\tanh", "np.exp(");
  var pythonList = []; // function list in Python
  pythonList.push("np.arccos(", "np.arcsin(", "np.arctan(", "np.cos(",
    "np.cosh(", "np.cot(", "np.coth(", "np.sqrt(", "np.csc(", "np.exp(",
    "np.log(", "np.log(", "np.sec(", "np.sin(", "np.sinh(", "np.tan(",
    "np.tanh(", "np.exp(");

  function equationFilter1(eqx) {
    for (var i in symList1) {
      if (eqx.includes(symList1[i])) {
        var count = eqx.split(symList1[i]).length - 1;
        for (var j = 1; j <= count; j++) {
          eqx = eqx.replace(symList1[i], symList2[i]);
        };
      };
    };
    return eqx;
  };

  function equationFilter2(eqx) {
    for (var i in funcList) {
      if (eqx.includes(funcList[i]) === true) {
        var count = eqx.split(funcList[i]).length - 1;
        for (var j = 1; j <= count; j++) {
          var countPM = eqx.indexOf(funcList[i]);
          var eqxL = eqx.length;
          var pTrue = eqx.slice(countPM, eqxL).includes("+");
          var mTrue = eqx.slice(countPM, eqxL).includes("-");
          if (pTrue === true || mTrue === true) {
            for (var k = countPM; k <= eqxL; k++) {
              if (eqx[k] === "+" || eqx[k] === "-") {
                eqx = eqx.slice(0, k) + ")" + eqx.slice(k);
                break;
              };
            };
          } else if (pTrue === false || mTrue === false) {
            eqx = eqx.concat(")");
          };
          eqx = eqx.replace(funcList[i], pythonList[i]);
        };
      };
    };
    if (eqx.includes("()")) {
      count = eqx.split("()").length - 1;
      for (j = 1; j <= count; j++) {
        eqx = eqx.replace("()", "");
      };
    };
    return eqx;
  };

  function equationFilter3(eqx) {
    var eqx1 = equationFilter1(eqx);
    var eqx2 = equationFilter2(eqx1);
    if (eqx2.includes(" ") === true) {
      var count = eqx2.split(" ").length - 1;
      for (var j = 1; j <= count; j++) {
        eqx2 = eqx2.replace(" ", "");
      }
    }
    // else {
    //   eqx2 = eqx2;
    // }
    if (eqx2.includes("np.pi")) {
      var npList = eqx2.split("np.pi");
      for (var i = 0; i < npList.length; i++) {
        if (i === 0) {
          var element = npList[i];
          var lastChar = element[element.length - 1];
          var firstChar = element[0];
          if (isNaN(lastChar) === false) {
            npList[i] = npList[i].concat("*");
          };
        } else {
          element = npList[i];
          lastChar = element[element.length - 1];
          firstChar = element[0];
          if (isNaN(lastChar) === false) {
            npList[i] = npList[i].concat("*");
          } else if (firstChar.toUpperCase() !== firstChar.toLowerCase()) {
            npList[i] = "*".concat(npList[i]);
          }
        }
      };
      eqx2 = npList.join("np.pi");
    };
    return eqx2;
  };

  function equationFilter4(eqx, param) {
    var eqx3 = equationFilter3(eqx, param);
    if (param === "" || param === undefined) {
      window["x"] = 1;
      var countx = eqx3.split("x").length - 1;
      // if (countx < 1) {
      //   eqx3 = eqx3;
      // } 
      if (countx => 1) {
        var eqx1 = [];
        for (var i = 1; i <= countx; i++) {
          var LofX = eqx3.indexOf("x") - 1;
          var RofX = eqx3.indexOf("x") + 1;
          if (isNaN(eqx3[LofX]) === false) {
            eqx1 = eqx1 + eqx3.slice(0, LofX + 1) + "*x";// + "x";
            eqx3 = eqx3.slice(RofX);
          } else if (isNaN(eqx3[LofX]) === true) {
            eqx1 = eqx1 + eqx3.slice(0, RofX);
            eqx3 = eqx3.slice(RofX);
          };
        };
        eqx1 = eqx1 + eqx3;
        eqx3 = eqx1;
        //try {eval(eqx);}
        //catch(err){alert("Please check the parameter.")}
      } else {
        LofX = eqx3.indexOf("x");
        if (isNaN(eqx3[LofX]) === false) {
          eqx3 = eqx3.slice(0, LofX) + "*" + eqx3.slice(LofX);
        };
        //try {eval(eqx);}
        //catch(err){alert("Please check the parameter.")}
      };
    } else if (param.toUpperCase() !== param.toLowerCase()) {
      window[param] = 1;
      var countp = eqx3.split(param).length - 1;
      // if (countp < 1) {
      //   eqx3 = eqx3;
      // } else 
      if (countp >= 1) {
        eqx1 = [];
        for (i = 1; i <= countp; i++) {
          LofX = eqx3.indexOf(param) - 1;
          RofX = eqx3.indexOf(param) + param.length;
          if (isNaN(eqx3[LofX]) === false) {
            eqx1 = eqx1 + eqx3.slice(0, LofX + 1) + "*" + param;
            eqx3 = eqx3.slice(RofX);
          } else if (isNaN(eqx3[LofX]) === true) {
            eqx1 = eqx1 + eqx3.slice(0, RofX);
            eqx3 = eqx3.slice(RofX);
          };
        };
        eqx1 = eqx1 + eqx3;
        eqx3 = eqx1;
        //try {eval(eqx);}
        //catch(err){alert("Please check the equation.")}
      } else {
        LofX = eqx3.indexOf(param);
        if (isNaN(eqx3[LofX]) === false) {
          eqx3 = eqx3.slice(0, LofX) + "*" + eqx3.slice(LofX);
        };
        //try {eval(eqx);}
        //catch(err){alert("Please check the equation.")}
      };

    };
    return eqx3;
  };

  return equationFilter4(eqx, param);
};

export default functionFilter;