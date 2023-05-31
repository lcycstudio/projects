var checkDE = function (eqx, order) {
    var proceed = true;
    var count = eqx.split("np").length - 1;
    for (var i = 1; i <= count; i++) {
        eqx = eqx.replace("np", "Math");
    };
    if (eqx.includes("=")) {
        var esIndex = eqx.indexOf("=");

        var fun = eqx.substr(esIndex + 1, eqx.length);
        if (order === '1') {
            for (i in fun) {
                if (fun[i].toLowerCase() !== fun[i].toUpperCase()) {
                    window[fun[i]] = 1;
                };
            };
            try {
                // eslint-disable-next-line
                var func = new Function('return ' + fun);
                func();
            } catch (err) {
                // A1: This is not a valid 1st order equation.
                proceed = "This is not a valid 1st order equation.";
                return proceed;
            };
        } else if (order === '2') {
            // // 1. check for y' or similar
            // primeList = fun.split("'");
            // for (i in primeList) {
            //   var p = primeList[i];
            //   if (p != "") {
            //     if (p[p.length-1].toLowerCase() != p[p.length-1].toUpperCase()) {
            //       primeList[i] = primeList[i].replace(p[p.length-1],"v");
            //     };
            //   };
            // };
            // fun = primeList.join("");
            // // 2. check for dy/dx or similar
            // divideList = fun.split("/");
            // var format = /[!^*()+-=\[\]{};':"\\|\/?]/;
            // for (i in divideList) {
            //   var d = divideList[i];
            //   var dl = d.length;
            //   if (d.substr(dl-4,dl).toLowerCase() != d.substr(dl-4,dl).toUpperCase()) {
            //     if (d.substr(dl-4,dl).includes("d")) {
            //       divideList[i] = divideList[i].replace(d.substr(dl-4,dl),"v");
            //     };
            //   };
            //   if (d.substr(0,4).toLowerCase() != d.substr(0,4).toUpperCase()) {
            //     if (d.substr(0,4).includes("d")) {
            //       divideList[i] = divideList[i].replace(d.substr(0,4),"");
            //     };
            //   };
            // };
            // fun = divideList.join("");

            for (i in fun) {
                if (fun[i].toLowerCase() !== fun[i].toUpperCase()) {
                    window[fun[i]] = 1;
                };
            };
            try {
                // eslint-disable-next-line
                func = new Function('return ' + fun);
                func();
            } catch (err) {
                // A2: This is not a valid 2nd order equation.
                // console.log("Check Case A2 in checkDiffEqn.js");
                // alert("This is not a valid 2nd order equation.");
                proceed = "This is not a valid 2nd order equation.";
                return proceed;
            };
        };
    } else {
        fun = eqx;
        if (order === '1') {
            for (i in fun) {
                if (fun[i].toLowerCase() !== fun[i].toUpperCase()) {
                    window[fun[i]] = 1;
                };
            };
            try {
                // eslint-disable-next-line
                func = new Function('return ' + fun);
                func();
            } catch (err) {
                // A3: This is not a valid 1st order equation.
                // console.log("Check Case A3 in checkDiffEqn.js");
                // alert("This is not a valid 1st order equation.");
                proceed = "This is not a valid 1st order equation.";
                return proceed;
            };
        } else if (order === '2') {
            // // 3. check for y' or similar
            // primeList = fun.split("'");
            // for (i in primeList) {
            //   var p = primeList[i];
            //   if (p != "") {
            //     if (p[p.length-1].toLowerCase() != p[p.length-1].toUpperCase()) {
            //       primeList[i] = primeList[i].replace(p[p.length-1],"v");
            //     };
            //   };
            // };
            // fun = primeList.join("");
            // // 4. check for dy/dx or similar
            // divideList = fun.split("/");
            // var format = /[!^*()+-=\[\]{};':"\\|\/?]/;
            // for (i in divideList) {
            //   var d = divideList[i];
            //   var dl = d.length;
            //   if (d.substr(dl-2,dl).toLowerCase() != d.substr(dl-2,dl).toUpperCase()) {
            //     if (format.test(d.substr(dl-2,dl)) == false) {
            //       divideList[i] = divideList[i].replace(d.substr(dl-2,dl),"v");
            //     };
            //   };
            //   if (d.substr(0,2).toLowerCase() != d.substr(0,2).toUpperCase()) {
            //     if (format.test(d.substr(0,2)) == false) {
            //       divideList[i] = divideList[i].replace(d.substr(0,2),"");
            //     };
            //   };
            // };
            // fun = divideList.join("");

            for (i in fun) {
                if (fun[i].toLowerCase() !== fun[i].toUpperCase()) {
                    window[fun[i]] = 1;
                };
            };
            try {
                // eslint-disable-next-line
                func = new Function('return ' + fun);
                func();
            } catch (err) {
                // A4: This is not a valid 2nd order equation.
                // console.log("Check Case A4 in checkDiffEqn.js");
                // alert();
                proceed = "This is not a valid 2nd order equation.";
                return proceed;
            };
        };
    };
    return proceed;
};

export default checkDE;