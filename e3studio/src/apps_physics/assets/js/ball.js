
var ball = new Image, shadow = new Image, shading = new Image;
window.onload = function () {
    var c = document.getElementById('canvas');
    var w = c.width = 800;
    var h = c.height = 600;
    var ctx = c.getContext('2d');
    var dx = 5, dy = -2;
    var x = 400, y = 100, a = 0;
    var deg2rad = Math.PI / 180;
    var da = 10 * deg2rad;

    var scale = 1.0;
    var bw = (ball.width * scale) / 2;
    var bh = (ball.height * scale) / 2;


    setInterval(function () {
        ctx.clearRect(0, 0, w, h);

        ctx.translate(x, y);
        // ctx.drawImage(shadow, -bw + 10, -bh + 10);
        ctx.rotate(a);
        ctx.drawImage(ball, -bw, -bh, ball.width * scale, ball.height * scale);
        ctx.rotate(-a);                      // The shading shouldn't be rotated
        // ctx.drawImage(shading, -bw, -bh);
        ctx.translate(-x, -y);

        x += dx;
        a += da;
        y += dy;

        if ((x - bw < 0) || (x + bw > w)) {
            dx *= -1;
            da *= -1;
        }

        if ((y - bh < 0) || (y + bh > h)) {
            dy *= -1;
            da *= -1;
        }

    }, 30);
}
ball.src = 'smiley.gif';
// shadow.src = 'beachball_shadow.png';
// shading.src = 'beachball_shading.png';
