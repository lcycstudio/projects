//var eqx = "y=\\frac{x^{\\frac{2}{3}}}{3}+\\ln\\left(x^3+2\\right)+3+\\sin x+\\arctan x";

var odeFilter = function (eqx) {
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
        };

        if (eqx2.includes("np.pi")) {
            var npList = eqx2.split("np.pi");
            for (var i in npList) {
                var element = npList[i];
                var lastChar = element[element.length - 1];
                var firstChar = element[0];
                if (isNaN(lastChar) === false) {
                    npList[i] = npList[i].concat("*");
                } else if (firstChar.toUpperCase() !== firstChar.toLowerCase()) {
                    npList[i] = "*".concat(npList[i]);
                }
            };
            eqx2 = npList.join("np.pi");
        };
        return eqx2;
    };

    eqx = equationFilter3(eqx);

    function equationFilter4(eqx) {
        if (eqx.includes("=")) {
            var fun = eqx.split("=")[1];
            // 1. check for y' or similar
            if (fun.includes("'") === true) {
                var primeList = fun.split("'");
                for (var i = 0; i < primeList.length - 1; i++) {
                    var p = primeList[i];
                    if (p !== "") {
                        if (p[p.length - 1].toLowerCase() !== p[p.length - 1].toUpperCase()) {
                            primeList[i] = primeList[i].replace(p[p.length - 1], "v");
                        };
                    };
                };
                fun = primeList.join("");
            } else if (fun.includes("/")) {
                // 2. check for dy/dx or similar
                var divideList = fun.split("/");
                // var format = /[!^*()+-=\[\]{};':"\\|\/?]/;
                for (i in divideList) {
                    var d = divideList[i];
                    var dl = d.length;
                    if (d.substr(dl - 4, dl).toLowerCase() !== d.substr(dl - 4, dl).toUpperCase()) {
                        if (d.substr(dl - 4, dl).includes("d")) {
                            divideList[i] = divideList[i].replace(d.substr(dl - 4, dl), "v");
                        };
                    };
                    if (d.substr(0, 4).toLowerCase() !== d.substr(0, 4).toUpperCase()) {
                        if (d.substr(0, 4).includes("d")) {
                            divideList[i] = divideList[i].replace(d.substr(0, 4), "");
                        };
                    };
                };
                fun = divideList.join("");
            };
            eqx = [eqx.split("=")[0], fun].join("=");
        } else {
            if (eqx.includes("'")) {
                primeList = eqx.split("'");
                for (i = 0; i < primeList.length - 1; i++) {
                    p = primeList[i];
                    if (p !== "") {
                        if (p[p.length - 1].toLowerCase() !== p[p.length - 1].toUpperCase()) {
                            primeList[i] = primeList[i].replace(p[p.length - 1], "v");
                        };
                    };
                };
                eqx = primeList.join("");
            } else if (eqx.includes("/")) {
                // 2. check for dy/dx or similar
                divideList = eqx.split("/");
                // var format = /[!^*()+-=\[\]{};':"\\|\/?]/;
                for (i in divideList) {
                    d = divideList[i];
                    dl = d.length;
                    if (d.substr(dl - 4, dl).toLowerCase() !== d.substr(dl - 4, dl).toUpperCase()) {
                        if (d.substr(dl - 4, dl).includes("d")) {
                            divideList[i] = divideList[i].replace(d.substr(dl - 4, dl), "v");
                        };
                    };
                    if (d.substr(0, 4).toLowerCase() !== d.substr(0, 4).toUpperCase()) {
                        if (d.substr(0, 4).includes("d")) {
                            divideList[i] = divideList[i].replace(d.substr(0, 4), "");
                        };
                    };
                };
                eqx = divideList.join("");
            };
        };
        return eqx;
    };

    eqx = equationFilter4(eqx);

    function equationFilter5(eqx) {
        if (eqx.includes("=")) {
            var esIndex = eqx.indexOf("=");
            var orderString = eqx.substr(0, esIndex);
            if (orderString.includes("''") || orderString.includes("d^2")) {
                var order = '2';
            } else if (orderString.includes("'") || orderString.includes("d")) {
                order = '1';
            } else {
                order = '0';
            };
            var fun = eqx.split("=")[1];
            // var format = /[!^*()+-=\[\]{};':"\\|\/?]/;
            var funLen = fun.length;
            for (var i = 1; i < funLen; i++) {
                if (fun[i].toLowerCase() !== fun[i].toUpperCase()) {
                    if (!isNaN(fun[i - 1])) {
                        fun = fun.split(fun[i]).join("*" + fun[i]);
                        funLen = fun.length;
                    }
                };
            };
            eqx = [eqx.split("=")[0], fun].join("=");
        } else {
            if (eqx.includes("v")) {
                order = '2';
            } else {
                order = '1';
            };
            // eslint-disable-next-line
            var eqxLen = eqx.length;
            for (i = 1; i < eqx.length; i++) {
                if (eqx[i].toLowerCase() !== eqx[i].toUpperCase()) {
                    if (!isNaN(eqx[i - 1])) {
                        eqx = eqx.split(eqx[i]).join("*" + eqx[i]);
                        eqxLen = eqx.length;
                    };
                };
            };
        };
        return [eqx, order];
    };

    return equationFilter5(eqx);
};

export default odeFilter;