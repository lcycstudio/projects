var checkBounds = function (eqx) {
  var proceed;

  var count = eqx.split("np").length - 1;
  for (var i = 1; i <= count; i++) {
    eqx = eqx.replace("np", "Math");
  };
  count = eqx.split(".pi").length - 1;
  for (i = 1; i <= count; i++) {
    eqx = eqx.replace(".pi", ".PI");
  };

  window['x'] = 'x'
  if (eqx.search("=") === 1) {
    proceed = 'Please remove the "=" sign.'
  } else {
    try {
      // eslint-disable-next-line
      var funcs = Function('return ' + eqx);
      proceed = funcs();
    } catch (err) {
      proceed = "Please remove any variables.";
      return proceed;
    };
  };

  return proceed;

};

export default checkBounds;
