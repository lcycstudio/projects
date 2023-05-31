import numpy as np
from fractions import Fraction


def get_yp(N, x, h, f):
    yp = np.zeros(N)
    yp[0] = (f[1] - f[0]) / h
    yp[N - 1] = (f[N - 1] - f[N - 2]) / h
    for k in range(1, N - 1):
        # 3-point formula
        yp[k] = (f[k + 1] - f[k - 1]) / (2 * h)
    return yp


def math_sf_find_y(function, func_array, x_array, y):
    # f is a python function in string with equal sign
    # a and b aree the first two points
    # xtol is the tolerance
    # N is max number of steps
    wavefunc = ["np.arccos", "np.arcsin", "np.arctan", "np.cos", "np.cosh", "np.cot",
                "np.coth", "np.csc", "np.sec", "np.sin", "np.sinh", "np.tan", "np.tanh"]
    fmax = max(func_array)
    fmin = min(func_array)
    finc = (fmax - fmin) / len(func_array)
    for i in range(len(func_array)):
        if np.abs(y - func_array[i]) <= 10 * finc:
            a = x_array[i]
            break
    for i in range(i, len(func_array)):
        if np.abs(y - func_array[i]) >= 10 * finc:
            b = x_array[i]
            break
    function = function[function.index("=") + 1:len(function)]
    countX = function.count("x")
    function_a = function.replace("x", str(a), countX)
    function_b = function.replace("x", str(b), countX)
    countexp = function.count("exp")
    function_a = function_a.replace("eap", "exp", countexp)
    function_b = function_b.replace("ebp", "exp", countexp)
    for i in wavefunc:
        if i in function:
            wave = True
            break
        else:
            wave = False
    if wave:
        n = 1
        N = 20
        function_m = function_a.replace("a", "m", function_a.count("a"))
        while n <= N:
            m = 0.5 * (a + b)
            fa = eval(function_a)
            fm = eval(function_m)
            if eval(function_a) * eval(function_m) <= y:
                b = m
            else:
                a = m
            n = n + 1
        xint = m
    else:
        xtol = 0.001
        N = 100
        n = 1
        while n < N and (np.abs(b - a) > xtol):
            fx0 = eval(function_a)
            fx1 = eval(function_b)
            m = (fx1 - fx0) / (b - a)
            xint = a - (fx0 / m) + (y / m)
            a = b
            b = xint
            n = n + 1
    return round(xint, 4)


def get_ypp(N, x, h, f):
    ypp = np.zeros(N)
    for k in range(1, N - 1):
        ypp[k] = (f[k + 1] - 2 * f[k] + f[k - 1]) / (h**2)
    ypp[0] = ypp[1]
    ypp[N - 1] = ypp[N - 2]
    return ypp


def get_yppp(N, x, h, f):
    yp = np.zeros(N)  # 1st derivative function for storing
    yppp = np.zeros(N)  # 3rd derivative function for storing

    yp[0] = (f[1] - f[0]) / h  # 1st order forward differencing for k=0
    yp[1] = (f[2] - f[1]) / h  # 1st order forward differencing for k=1
    yp[2] = (f[3] - f[2]) / h  # 1st order forward differencing for k=2
    # 2nd order forward differencing from yp
    yppp[1] = (yp[2] - 2 * yp[1] + yp[0]) / (h**2)
    yppp[0] = yppp[1]

    # 1st order backward differencing for k=N-1
    yp[N - 1] = (f[N - 1] - f[N - 2]) / h
    # 1st order backward differencing for k=N-2
    yp[N - 2] = (f[N - 2] - f[N - 3]) / h
    # 1st order backward differencing for k=N-3
    yp[N - 3] = (f[N - 3] - f[N - 4]) / h
    # 2nd order forward differencing from yp
    yppp[N - 2] = (yp[N - 1] - 2 * yp[N - 2] + yp[N - 3]) / (h**2)
    yppp[N - 1] = yppp[N - 2]

    for k in range(2, N - 2):
        yppp[k] = (f[k + 2] * 0.5 - f[k - 2] * 0.5 -
                   f[k + 1] + f[k - 1]) / (h**3)
    return yppp


def get_integral(N, xa, h, fun):
    x2 = np.zeros(N + 1)
    f = np.zeros(N + 1)
    for k in range(1, N + 1):
        x2[k] = xa + (k - 1) * h
        f[k] = eval(fun.replace('x', str(x2[k]), fun.count('x')))
    if N % 2 == 0:
        n = N - 1
        xint = (h / 12) * (5 * f[N] + 8 * f[N - 1] - f[N - 2])
    else:
        n = N
        xint = 0
    sum = 0
    for k in range(2, n - 1 + 2, 2):
        sum = sum + 4.0 * f[k]

    for k in range(3, n - 2 + 2, 2):
        sum = sum + 2.0 * f[k]
    xint = xint + (h / 3) * (f[1] + sum + f[n])
    xint_frac = str(Fraction(xint).limit_denominator())
    return round(xint, 4), xint_frac


def get_RKFyp(N, x, hlist, f):
    yp = np.zeros(N)
    yp[0] = (f[1] - f[0]) / hlist[1]
    yp[N - 1] = (f[N - 1] - f[N - 2]) / hlist[N - 1]
    for k in range(1, N - 1):
        # 3-point formula
        yp[k] = (f[k + 1] - f[k - 1]) / (2 * hlist[k])
    return yp


def get_RKFypp(N, x, hlist, f):
    ypp = np.zeros(N)
    for k in range(1, N - 1):
        ypp[k] = (f[k + 1] - 2 * f[k] + f[k - 1]) / (hlist[k]**2)
    ypp[2] = ypp[3]
    ypp[1] = ypp[2]
    ypp[N - 1] = ypp[N - 2]
    return ypp


def RKF45(fun, yini, t0, tend, tole):
    c2 = 1 / 4
    a21 = 1 / 4
    c3 = 3 / 8
    a31 = 3 / 32
    a32 = 9 / 32
    c4 = 12 / 13
    a41 = 1932 / 2197
    a42 = -7200 / 2197
    a43 = 7296 / 2197
    c5 = 1
    a51 = 439 / 216
    a52 = -8
    a53 = 3680 / 513
    a54 = -845 / 4104
    c6 = 1 / 2
    a61 = -8 / 27
    a62 = 2
    a63 = -3544 / 2565
    a64 = 1859 / 4104
    a65 = -11 / 40
    bu1 = 16 / 135
    bu2 = 0
    bu3 = 6656 / 12825
    bu4 = 28561 / 56430
    bu5 = -9 / 50
    bu6 = 2 / 55
    bv1 = 25 / 216
    bv2 = 0
    bv3 = 1408 / 2565
    bv4 = 2197 / 4104
    bv5 = -1 / 5
    tlist = []
    ylist = []
    storh = []
    h = 0.1 * (float(tend) - float(t0))  # Set initial stepsize
    tlist.append(float(t0))
    ylist.append(float(yini))
    storh.append(h)  # Store stepsize
    n = 0
    tend = float(tend)
    while tlist[n] < tend:
        y = ylist[n]
        t = tlist[n]
        k1 = eval(fun)
        t = tlist[n] + c2 * h
        y = ylist[n] + a21 * h * k1
        k2 = eval(fun)
        t = tlist[n] + c3 * h
        y = ylist[n] + a31 * h * k1 + a32 * h * k2
        k3 = eval(fun)
        t = tlist[n] + c4 * h
        y = ylist[n] + a41 * h * k1 + a42 * h * k2 + a43 * h * k3
        k4 = eval(fun)
        t = tlist[n] + c5 * h
        y = ylist[n] + a51 * h * k1 + a52 * \
            h * k2 + a53 * h * k3 + a54 * h * k4
        k5 = eval(fun)
        t = tlist[n] + c6 * h
        y = ylist[n] + a61 * h * k1 + a62 * h * k2 + \
            a63 * h * k3 + a64 * h * k4 + a65 * h * k5
        k6 = eval(fun)
        u = ylist[n] + h * (bu1 * k1 + bu2 * k2 + bu3 *
                            k3 + bu4 * k4 + bu5 * k5 + bu6 * k6)
        v = ylist[n] + h * (bv1 * k1 + bv2 * k2 + bv3 *
                            k3 + bv4 * k4 + bv5 * k5)
        r = np.abs(v - u)
        if r <= tole:
            tlist.append(tlist[n] + h)
            storh.append(h)
            ylist.append(v)
            n = n + 1
        h = 0.9 * h * (tole / r)**0.2
        if tlist[-1] + h > tend:  # This is to ensure that we
            h = tend - tlist[-1]  # hit the end point tend

    h = (float(tend) - float(t0)) / (len(tlist) - 1)
    vlist = get_RKFyp(len(tlist), tlist, storh, ylist)
    alist = get_RKFyp(len(tlist), tlist, storh, vlist)
    vlist[0] = vlist[1]
    # alist[0] = alist[1]
    # alist[1] = alist[2]
    # alist[0] = alist[1]
    return tlist, ylist, vlist, alist, h


def EulerSympletic(fun, y0, yp0, t0, tend, N):
    h = (float(tend) - float(t0)) / N
    tlist = []
    ylist = []
    vlist = []
    tlist.append(float(t0))
    ylist.append(float(y0))
    vlist.append(float(yp0))
    for n in range(N):
        tlist.append(tlist[n] + h)
        ylist.append(ylist[n] + h * vlist[n])
        t = tlist[n]
        y = ylist[n + 1]
        v = vlist[n]
        vlist.append(vlist[n] + h * eval(fun))
    return tlist, ylist, vlist, h


def RK452nd(fun, y0, v0, t0, t1, N):
    # fun=MATLAB function handle
    # t0,y0,v0=initial conditions
    # tend=last time, N=Number of steps
    h = (float(t1) - float(t0)) / N
    tlist = []
    ylist = []
    vlist = []
    tlist.append(float(t0))
    ylist.append(float(y0))
    vlist.append(float(v0))

    for n in range(N):
        tlist.append(tlist[n] + h)
        k1 = vlist[n]
        k2 = vlist[n] + 0.5 * h * k1
        k3 = vlist[n] + 0.5 * h * k2
        k4 = vlist[n] + h * k3
        ylist.append(ylist[n] + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4))
        t = tlist[n]
        y = ylist[n]
        l1 = eval(fun)
        t = tlist[n] + 0.5 * h
        y = ylist[n] + 0.5 * h * k1
        l2 = eval(fun)
        y = ylist[n] + 0.5 * h * k2
        l3 = eval(fun)
        t = tlist[n] + h
        y = ylist[n] + h * k3
        l4 = eval(fun)
        vlist.append(vlist[n] + h / 6 * (l1 + 2 * l2 + 2 * l3 + l4))
    return tlist, ylist, vlist


def FF(fun, ya, yb, alpha, t0, t1, N):
    [x, y, v] = RK452nd(fun, ya, alpha, t0, t1, N)
    Fret = y[-1] - yb
    return Fret


def BVP(fun, ya, yb, t0, t1, tol, N):
    # fun is a MATLAB function
    # xa,xb,ya, and yb are the boundary cond.
    # tol is the tolerance, N is max number of steps
    alpha0 = 0.1
    alpha1 = 0.9  # Initial values for alpha
    n = 1  # Secant method for root finding
    while (n <= N) and (np.abs(alpha1 - alpha0) > tol):
        Falpha0 = FF(fun, ya, yb, alpha0, t0, t1, N)
        Falpha1 = FF(fun, ya, yb, alpha1, t0, t1, N)
        m = (Falpha1 - Falpha0) / (alpha1 - alpha0)
        alphaint = alpha0 - Falpha0 / m
        alpha0 = alpha1
        alpha1 = alphaint
        n = n + 1
    t, y, v = RK452nd(fun, ya, alphaint, t0, t1, N)
    return alphaint, t, y


def get_double_integral(xa, xb, ya, yb, fun):
    find_var_list = [xa, xb, ya, yb]
    var = ""
    var_index = 4
    for i in find_var_list:
        try:
            float(eval(i))
        except Exception as inst:
            var_index = find_var_list.index(i)
            var = i
    if var_index == 4:
        N = 2001
    else:
        N = 10001
    X = ""
    Y = ""
    Z = ""
    if var_index == 4:
        funZ = fun.replace("x", "X", fun.count("x"))
        funZ = funZ.replace("y", "Y", fun.count("y"))
        xval = np.zeros(N + 1)
        yval = np.zeros(N + 1)
        hx = (float(eval(xb)) - float(eval(xa))) / (N - 1)
        hy = (float(eval(yb)) - float(eval(ya))) / (N - 1)
        for k in range(1, N + 1):
            xval[k] = eval(xa) + (k - 1) * hx
            yval[k] = eval(ya) + (k - 1) * hy
        X, Y = np.meshgrid(xval, yval)
        Z = eval(funZ)
    pythonList = ["np.sin", "np.cos", "np.tan", "np.arccos", "np.arcsin", "np.arctan",
                  "np.sinh", "np.cosh", "np.tanh", "np.csc", "np.sec", "np.cot",
                  "np.csch", "np.sech", "np.coth", "np.sqrt", "np.exp", "np.log"]
    for i in pythonList:
        if i in fun:
            fun = fun.replace(i, i[3:])

    if var_index == 0:  # xa is y
        var = '({0})'.format(var)
        int_fun = str(integrate(fun, Symbol('x')))
        int_fun1 = '({0})'.format(int_fun.replace('x', var))
        int_fun2 = int_fun.replace('x', xb)
        new_fun = int_fun2 + '-' + int_fun1
    elif var_index == 1:  # xb is y
        var = '({0})'.format(var)
        int_fun = str(integrate(fun, Symbol('x')))
        int_fun1 = '({0})'.format(int_fun.replace('x', xa))
        int_fun2 = int_fun.replace('x', var)
        new_fun = int_fun2 + '-' + int_fun1
    elif var_index == 2:  # ya is x
        var = '({0})'.format(var)
        int_fun = str(integrate(fun, Symbol('y')))
        int_fun1 = '({0})'.format(int_fun.replace('y', var))
        int_fun2 = int_fun.replace('y', yb)
        new_fun = int_fun2 + '-' + int_fun1
    elif var_index == 3:  # yb is x
        var = '({0})'.format(var)
        int_fun = str(integrate(fun, Symbol('y')))
        int_fun1 = '({0})'.format(int_fun.replace('y', ya))
        int_fun2 = int_fun.replace('y', var)
        new_fun = int_fun2 + '-' + int_fun1
    else:
        int_fun = str(integrate(fun, Symbol('y')))
        int_fun1 = '({0})'.format(int_fun.replace('y', ya))
        int_fun2 = int_fun.replace('y', yb)
        new_fun = int_fun2 + '-' + int_fun1
    for i in pythonList:
        if i[3:] in new_fun:
            new_fun = new_fun.replace(i[3:], i)

    f = np.zeros(N + 1)
    if var_index == 0 or 1 or 4:
        x2 = np.zeros(N + 1)
        h = (float(eval(xb)) - float(eval(xa))) / (N - 1)
        for k in range(1, N + 1):
            x2[k] = eval(xa) + (k - 1) * h
            f[k] = eval(new_fun.replace('x', str(x2[k]), new_fun.count('x')))
            if np.isinf(f[k]) or np.isnan(f[k]):
                f[k] = eval(new_fun.replace(
                    'x', str(x2[k] + 1j), new_fun.count('x')))
    else:
        y2 = np.zeros(N + 1)
        h = (float(eval(yb)) - float(eval(ya))) / (N - 1)
        for k in range(1, N + 1):
            y2[k] = eval(ya) + (k - 1) * h
            f[k] = eval(new_fun.replace('y', str(y2[k]), new_fun.count('y')))
            if np.isinf(f[k]) or np.isnan(f[k]):
                f[k] = eval(new_fun.replace(
                    'y', str(x2[k] + 1j), new_fun.count('y')))
    if N % 2 == 0:
        n = N - 1
        result = (h / 12) * (5 * f[N] + 8 * f[N - 1] - f[N - 2])
    else:
        n = N
        result = 0
    sum = 0
    for k in range(2, n - 1 + 2, 2):
        sum = sum + 4.0 * f[k]

    for k in range(3, n - 2 + 2, 2):
        sum = sum + 2.0 * f[k]
    result = (result + (h / 3) * (f[1] + sum + f[n])).real
    result_frac = str(Fraction(result).limit_denominator())
    return round(result, 4), result_frac, X, Y, Z
