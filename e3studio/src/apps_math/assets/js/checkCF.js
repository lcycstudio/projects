var checkCF = function (eqx, param) {
  var proceed = true;
  if (eqx.search("=") === 1) {
    eqx = eqx.slice(eqx.indexOf('=') + 1, eqx.length)

    if (eqx === "") {
      proceed = "Please complete the function."
    };
    var count = eqx.split("np").length - 1;
    for (var i = 1; i <= count; i++) {
      eqx = eqx.replace("np", "Math");
    };
    // when parameter is left blank
    if (param === "" || param === undefined) {
      window["x"] = 1;
      // countx checks if x is the parameter
      var countx = eqx.split("x").length - 1;
      if (countx < 1) {
        try {
          // eslint-disable-next-line
          var func = new Function('return ' + eqx);
          func();
          // return new Function(eqx);
        } catch (err) {
          // A1: x is not the parameter.
          // alert("Please check the parameter.");
          proceed = "x is not the default parameter.";
          return proceed;
        };
      } else if (countx > 1) {
        try {
          // eslint-disable-next-line
          func = new Function('return ' + eqx);
          func();
        } catch (err) {
          // alert("Please check the equation.");
          // A2: when x is the parameter, the simple function is invalid.
          proceed = "The function is invalid.";
          return proceed;
        }
      } else {
        try {
          // eslint-disable-next-line
          func = new Function('return ' + eqx);
          func();
        } catch (err) {
          // alert("Please check the equation.");
          // A3: the simple function is just wrong.

          proceed = "The function is invalid.";
          return proceed;
        }
      }
    }
    // when parameter is not blank or default
    else if (param !== "") {
      window[param] = 1;
      // countp checks the parameter
      var countp = eqx.split(param).length - 1;
      if (countp < 1) {
        try {
          // eslint-disable-next-line
          func = new Function('return ' + eqx);
          func();
        } catch (err) {
          // alert("Please check the equation.");
          // B2: the sf is invalid with the specified parameter.
          proceed = 'The parameter is fine, but the function is invalid.';
          return proceed;
        };
        // alert("Please check the parameter.");
        // B1: must specify the parameter if not default
        // return false;
      } else if (countp > 1) {
        try {
          // eslint-disable-next-line
          func = new Function('return ' + eqx);
          func();
        } catch (err) {
          // alert("Please check the equation.");
          // B2: the sf is invalid with the specified parameter.
          proceed = 'The parameter is fine, but the function is invalid.';
          return proceed;
        };
      } else {
        try {
          // eslint-disable-next-line
          func = new Function('return ' + eqx);
          func();
        } catch (err) {
          if (param === "a") {
            // alert("Please check the parameter.");
            // B3: the sf is invalid even if the parameter is "a"
            proceed = 'The parameter is fine, but the function is invalid.';
            return proceed;
            // return 'The parameter is fine, but the function is invalid.';
          } else {
            // alert("Please check the equation.");
            // B4: the sf is invalid
            proceed = 'The parameter is fine, but the function is invalid.';
            return proceed;
            // return 'The parameter is fine, but the function is invalid.';
          };
        };
      };
    };
  } else {
    try {
      // eslint-disable-next-line
      func = new Function('return ' + eqx);
      func();
    } catch (err) {
      proceed = "The equation needs an equal sign '='";
      return proceed;
    };
  };
  return proceed;
};

export default checkCF;
