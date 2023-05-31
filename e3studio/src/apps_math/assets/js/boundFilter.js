var boundFilter = function (eqx) {
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

  const eqx1 = equationFilter1(eqx);

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
    return eqx;
  };

  var eqx2 = equationFilter2(eqx1);

  if (eqx2.includes("np.pi")) {
    var npList = eqx2.split("np.pi");
    for (var i = 0; i < npList.length; i++) {
      // if (i === 0) {
      var element = npList[i];
      var lastChar = element[element.length - 1];
      // var firstChar = element[0];
      if (isNaN(lastChar) === false) {
        npList[i] = npList[i].concat("*");
      }
    }
    eqx2 = npList.join("np.pi");
  }

  return eqx2;
};

export default boundFilter;
