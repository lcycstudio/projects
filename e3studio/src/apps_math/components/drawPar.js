
import xdata from '../containers/xdata';
import ydata from '../containers/ydata';
import zdata from '../containers/zdata';
var mat4 = require('gl-mat4');
var count = 0;
export default function (hl, canvas1, vertex_buffer, shaderProgram, rotx, roty, rotz) {
    count++;
    var length = xdata.length;
    var index = Math.floor(count / 0.5 % length);
    var vertices = [];
    vertices.push(xdata[index], ydata[index], zdata[index],);

    const fieldOfView = 45 * Math.PI / 180;   // in radians
    const aspect = hl.canvas.clientWidth / hl.canvas.clientHeight;
    const zNear = 0.1;
    const zFar = 1000.0;
    const projectionMatrix = mat4.create();

    // note: glmatrix.js always has the first argument
    // as the destination to receive the result.
    mat4.perspective(projectionMatrix,
        fieldOfView,
        aspect,
        zNear,
        zFar);

    // Set the drawing position to the "identity" point, which is
    // the center of the scene.
    const modelViewMatrix = mat4.create();

    mat4.translate(modelViewMatrix,     // destination matrix
        modelViewMatrix,     // matrix to translate
        [0.0, 0.0, -350.0]);  // amount to translate
    mat4.rotate(modelViewMatrix,  // destination matrix
        modelViewMatrix,  // matrix to rotate
        (-90 + rotx) * Math.PI / 180,     // amount to rotate in radians
        [1, 0, 0]);       // axis to rotate around (X)
    mat4.rotate(modelViewMatrix,  // destination matrix
        modelViewMatrix,  // matrix to rotate
        roty * Math.PI / 180,// amount to rotate in radians
        [0, 1, 0]);       // axis to rotate around (Y)
    mat4.rotate(modelViewMatrix,  // destination matrix
        modelViewMatrix,  // matrix to rotate
        rotz * Math.PI / 180,// amount to rotate in radians
        [0, 0, 1]);       // axis to rotate around (Z)

    /*======== Associating shaders to buffer objects ========*/

    //Bind appropriate array buffer to it
    hl.bindBuffer(hl.ARRAY_BUFFER, vertex_buffer);

    // Pass the vertex data to the buffer
    hl.bufferData(hl.ARRAY_BUFFER, new Float32Array(vertices), hl.STATIC_DRAW);

    // Unbind the buffer
    hl.bindBuffer(hl.ARRAY_BUFFER, null);

    // Bind vertex buffer object
    hl.bindBuffer(hl.ARRAY_BUFFER, vertex_buffer);

    // Get the attribute location
    var coord = hl.getAttribLocation(shaderProgram, "coordinates");

    // Point an attribute to the currently bound VBO
    hl.vertexAttribPointer(coord, 3, hl.FLOAT, false, 0, 0);

    // Enable the attribute
    hl.enableVertexAttribArray(coord);

    // Clear the canvas
    // hl.clearColor(1.0, 1.0, 1.0, 0.0);
    // hl.clearDepth(1.0);                 // Clear everything


    hl.clearColor(0.0, 1.0, 1.0, 0.0);  // Clear to black, fully opaque
    hl.clearDepth(1.0);                 // Clear everything
    hl.enable(hl.DEPTH_TEST);           // Enable depth testing
    hl.depthFunc(hl.LEQUAL);            // Near things obscure far things
    hl.clear(hl.COLOR_BUFFER_BIT | hl.DEPTH_BUFFER_BIT);

    hl.uniformMatrix4fv(
        hl.getUniformLocation(shaderProgram, 'uProjectionMatrix'),
        false,
        projectionMatrix);
    hl.uniformMatrix4fv(
        hl.getUniformLocation(shaderProgram, 'uModelViewMatrix'),
        false,
        modelViewMatrix);

    // Set the view port
    hl.viewport(0, 0, canvas1.width, canvas1.height);

    // Draw the triangle
    hl.drawArrays(hl.POINTS, 0, 1);
}