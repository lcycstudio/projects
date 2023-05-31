var xdata = [1.0, 2.0, 3.0000000000000004, 4.0, 5.0, 6.0, 7.0, 7.999999999999999, 9.0, 9.999999999999998, 10.999999999999998, 12.0, 13.0, 14.000000000000002, 15.000000000000002, 16.000000000000004, 17.000000000000004, 18.000000000000004, 19.000000000000007, 20.000000000000004, 21.000000000000007, 22.000000000000007, 23.000000000000007, 24.000000000000007, 25.000000000000007, 26.00000000000001, 27.00000000000001, 28.00000000000001, 29.000000000000014, 30.000000000000014, 31.000000000000014, 32.000000000000014, 33.000000000000014, 34.000000000000014, 35.000000000000014, 36.00000000000002, 37.00000000000002, 38.00000000000002, 39.00000000000002, 40.000000000000014, 41.000000000000014, 42.000000000000014, 43.00000000000001, 44.0, 45.0, 45.0, 45.00119998, 46.20117998, 47.401159979999996, 48.601139979999985, 49.80111997999998, 51.00109997999998, 52.201079979999975, 53.40105997999997, 54.60103997999997, 55.801019979999964, 57.00099997999996, 58.20097997999996, 59.40095997999995, 60.60093997999995, 61.80091997999995, 63.00089997999994, 64.20087997999994, 65.40085997999994, 66.60083997999992, 67.80081997999991, 69.00079997999991, 70.20077997999991, 71.4007599799999, 72.6007399799999, 73.8007199799999, 75.0006999799999, 76.20067997999989, 77.40065997999989, 78.60063997999988, 79.80061997999988, 81.00059997999988, 82.20057997999987, 83.40055997999987, 84.60053997999987, 85.80051997999986, 87.00049997999986, 88.20047997999986, 89.40045997999985, 90.60043997999983, 91.80041997999983, 93.00039997999983, 94.20037997999982, 95.40035997999982, 96.60033997999982, 97.80031997999981, 99.00029997999981, 99.20986711850927, 99.21106707850926, 100.41102707850926, 101.61098707850925, 102.81094707850924, 104.01090707850925, 105.21086707850924, 106.41082707850924, 107.61078707850923, 108.81074707850922, 110.01070707850923, 111.21066707850922, 112.41062707850922, 113.61058707850921, 114.8105470785092, 116.0105070785092, 117.2104670785092, 118.4104270785092, 119.61038707850918, 120.81034707850918, 122.01030707850919, 123.21026707850919, 124.41022707850917, 125.61018707850917, 126.31404535590954, 126.31524529590953, 127.51518529590953, 128.71512529590953, 129.91506529590953, 131.11500529590953, 132.31494529590952, 133.51488529590952, 134.71482529590952, 135.91476529590952, 137.1147052959095, 138.3146452959095, 139.51458529590948, 139.86560500973104, 139.86680492973102, 141.066724929731, 142.26664492973103, 143.46656492973102, 144.666484929731, 145.866404929731, 146.64096829025104, 146.64216819025103, 147.842068190251, 149.04196819025103, 150.02828983336417, 150.02948971336417, 151.22936971336418, 151.72161872239587, 151.72281858239586, 152.5679653816978, 152.5691652216978, 152.9908279647904, 152.9920277847904, 154.1718477847904, 155.3316677847904, 156.47148778479038, 157.5913077847904, 158.69112778479038, 159.7709477847904, 160.8307677847904, 161.8705877847904, 162.8904077847904, 163.8902277847904, 164.8700477847904, 165.8298677847904, 166.7696877847904, 167.68950778479038, 168.58932778479038, 169.46914778479038, 170.3289677847904, 171.1687877847904, 171.9886077847904, 172.7884277847904, 173.5682477847904, 174.3280677847904, 175.0678877847904, 175.7877077847904, 176.4875277847904, 177.1673477847904, 177.8271677847904, 178.4669877847904, 179.0868077847904, 179.6866277847904, 180.26644778479042, 180.82626778479042, 181.3660877847904, 181.88590778479042, 182.38572778479042, 182.8655477847904, 183.32536778479042, 183.7651877847904, 184.1850077847904, 184.5848277847904, 184.9646477847904, 185.32446778479041, 185.66428778479042, 185.9841077847904, 186.28392778479042, 186.56374778479042, 186.8235677847904, 187.06338778479042, 187.28320778479042, 187.4830277847904, 187.66284778479042, 187.8226677847904, 187.96248778479043, 188.08230778479043, 188.18212778479042, 188.26194778479044, 188.32176778479044, 188.36158778479043, 188.38140778479044, 188.38122778479044,];
var ydata = [99.951, 99.80399999999999, 99.55899999999998, 99.21599999999998, 98.77499999999998, 98.23599999999998, 97.59899999999998, 96.86399999999996, 96.03099999999995, 95.09999999999994, 94.07099999999993, 92.94399999999992, 91.71899999999991, 90.3959999999999, 88.9749999999999, 87.45599999999989, 85.83899999999988, 84.12399999999988, 82.31099999999988, 80.39999999999988, 78.39099999999988, 76.28399999999986, 74.07899999999985, 71.77599999999984, 69.37499999999983, 66.87599999999982, 64.27899999999981, 61.58399999999981, 58.79099999999981, 55.899999999999814, 52.91099999999981, 49.823999999999806, 46.638999999999804, 43.3559999999998, 39.9749999999998, 36.4959999999998, 32.918999999999805, 29.243999999999804, 25.470999999999805, 21.599999999999806, 17.63099999999981, 13.56399999999981, 9.398999999999813, 5.1359999999998145, 0.7749999999998168, 0, 0, 2.164594362117866, 4.231188724235731, 6.199783086353597, 8.070377448471463, 9.84297181058933, 11.517566172707195, 13.094160534825061, 14.572754896942927, 15.953349259060793, 17.23594362117866, 18.420537983296526, 19.50713234541439, 20.495726707532256, 21.386321069650123, 22.17891543176799, 22.873509793885855, 23.47010415600372, 23.968698518121588, 24.369292880239453, 24.671887242357318, 24.876481604475185, 24.98307596659305, 24.991670328710914, 24.90226469082878, 24.714859052946647, 24.42945341506451, 24.046047777182377, 23.564642139300243, 22.985236501418107, 22.307830863535973, 21.53242522565384, 20.659019587771702, 19.687613949889567, 18.618208312007432, 17.4508026741253, 16.185397036243163, 14.821991398361028, 13.360585760478893, 11.801180122596758, 10.143774484714623, 8.388368846832488, 6.534963208950352, 4.583557571068217, 2.534151933186081, 0.3867462953039453, 0, 0, 1.057797181058933, 2.017594362117866, 2.8793915431767987, 3.6431887242357317, 4.308985905294664, 4.876783086353597, 5.346580267412529, 5.718377448471461, 5.9921746295303935, 6.167971810589326, 6.245768991648259, 6.2255661727071905, 6.1073633537661225, 5.891160534825055, 5.576957715883987, 5.164754896942919, 4.654552078001852, 4.046349259060784, 3.340146440119716, 2.5359436211786486, 1.633740802237581, 0.6335379832965132, 0, 0, 0.5043985905294665, 0.9107971810589328, 1.2191957715883994, 1.429594362117866, 1.5419929526473324, 1.556391543176799, 1.4727901337062654, 1.2911887242357318, 1.0115873147651984, 0.6339859052946647, 0.15838449582413103, 0, 0, 0.22769929526473323, 0.3573985905294665, 0.38909788579419974, 0.32279718105893296, 0.15849647632366612, 0, 0, 0.08934964763236661, 0.08069929526473321, 0, 0, 0.020174823816183303, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,];
var wdata = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.998, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.996000000000002, 19.994000000000003, 19.994000000000003, 19.994000000000003, 19.994000000000003, 19.994000000000003, 19.994000000000003, 19.994000000000003, 19.994000000000003, 19.994000000000003, 19.994000000000003, 19.994000000000003, 19.994000000000003, 19.994000000000003, 19.992000000000004, 19.992000000000004, 19.992000000000004, 19.992000000000004, 19.992000000000004, 19.992000000000004, 19.992000000000004, 19.990000000000006, 19.990000000000006, 19.990000000000006, 19.990000000000006, 19.988000000000007, 19.988000000000007, 19.988000000000007, 19.986000000000008, 19.986000000000008, 19.98400000000001, 19.98400000000001, 19.98200000000001, 19.98200000000001, 19.648966666666677, 19.315933333333344, 18.98290000000001, 18.64986666666668, 18.316833333333346, 17.983800000000013, 17.65076666666668, 17.317733333333347, 16.984700000000014, 16.65166666666668, 16.31863333333335, 15.985600000000016, 15.652566666666683, 15.31953333333335, 14.986500000000017, 14.653466666666684, 14.320433333333352, 13.987400000000019, 13.654366666666686, 13.321333333333353, 12.98830000000002, 12.655266666666687, 12.322233333333354, 11.989200000000022, 11.656166666666689, 11.323133333333356, 10.990100000000023, 10.65706666666669, 10.324033333333357, 9.991000000000025, 9.657966666666692, 9.324933333333359, 8.991900000000026, 8.658866666666693, 8.32583333333336, 7.9928000000000266, 7.659766666666693, 7.326733333333359, 6.993700000000025, 6.660666666666692, 6.327633333333358, 5.994600000000024, 5.66156666666669, 5.328533333333357, 4.995500000000023, 4.662466666666689, 4.3294333333333554, 3.9964000000000217, 3.663366666666688, 3.3303333333333542, 2.9973000000000205, 2.6642666666666868, 2.331233333333353, 1.9982000000000195, 1.665166666666686, 1.3321333333333525, 0.999100000000019, 0.6660666666666855, 0.33303333333335194, 0,];
function init() {
    var canvas = document.getElementById('okcanvas');
    canvas.style.zoom = "1.0";
    var w = canvas.width = 640;
    var h = canvas.height = 480;
    var ctx = canvas.getContext('2d');
    var raf;
    var image = new Image();
    image.src = "smiley.gif";

    var ball = {
        x: 100 + xdata[0],
        y: 200 - ydata[0],
        vx: 5,
        vy: 2,
        radius: 25,
        color: 'blue',
        scale: 1.0,
        deg2rad: Math.PI / 180,
        a: 0,
        da: 10 * Math.PI / 180,
        count: 0,
        draw: function () {
            ctx.translate(this.x, this.y);
            ctx.rotate(this.a);
            ctx.drawImage(image, -(image.width * this.scale) / 2, -(image.height * this.scale) / 2, image.width * this.scale, image.height * this.scale);
            ctx.rotate(-this.a);
            ctx.translate(-this.x, -this.y);
            ball.x = 100 + xdata[this.count];
            ball.y = 200 - ydata[this.count];
            ball.a += wdata[this.count] * Math.PI / 180;
            this.count += 1;
            if (this.count === xdata.length) {
                this.count = 0;
            }
        }
    };

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ball.draw();
        raf = window.requestAnimationFrame(draw);
    }

    canvas.addEventListener('mouseover', function (e) {
        raf = window.requestAnimationFrame(draw);
    });

    canvas.addEventListener('mouseout', function (e) {
        window.cancelAnimationFrame(raf);
    });
}
init();
// var canvas = document.getElementById('okcanvas');
// var w = canvas.width = 640;
// var h = canvas.height = 480;
// var ctx = canvas.getContext('2d');
// var raf;
// var image = new Image();
// image.src = "smiley.gif";






// ball.draw();