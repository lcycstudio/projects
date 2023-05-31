import numpy as np


def acc1(w, v):
    return w * v


def acc2(w, v):
    return -w * v


def acc3(w, v):
    return 0


def particle(w, speed, direction):
    v0 = speed
    RL = v0 / w
    t0 = 0  # t0=initial time
    tend = 20 * np.pi  # tend=last time
    N = 1000  # N=Number of steps = 10000 large enough
    h = (tend - t0) / N  # Grid size
    t = np.arange(t0, tend + h, h)

    x = np.ones(len(t))
    y = np.ones(len(t))
    z = np.ones(len(t))
    vx = np.ones(len(t))
    vy = np.ones(len(t))
    vz = np.ones(len(t))

    if direction == 'y':
        x0 = 0
        y0 = 0
        z0 = RL
        vx0 = v0
        vy0 = v0
        vz0 = 0
    else:
        x0 = 0       # x initial position x0=0
        y0 = RL       # y initial position y0=2
        z0 = 0       # z initial position z0=0
        vx0 = v0      # x initial velocity vx0=xp0=1
        vy0 = 0       # y initial velocity vy0=yp0=0
        vz0 = v0      # z initial velocity vz0=zp0=1

    # initial positions
    x[0] = x0
    y[0] = y0
    z[0] = z0

    # initial verlocities
    vx[0] = vx0
    vy[0] = vy0
    vz[0] = vz0

    if direction == 'z':
        x[1] = x[0] + vx0 * h + 0.5 * acc1(w, vy[0]) * h * h  # Make first step
        y[1] = y[0] + vy0 * h + 0.5 * acc2(w, vx[0]) * h * h  # Make first step
        z[1] = z[0] + vz0 * h + 0.5 * acc3(w, vz[0]) * h * h  # Make first step

        vx[1] = vx[0] + h * acc1(w, vy[0])
        vy[1] = vy[0] + h * acc2(w, vx[0])
        vz[1] = vz[0] + h * acc3(w, vz[0])

        for n in range(1, N):

            x[n + 1] = x[n] + vx[n] * h + 0.5 * \
                acc1(w, vy[n]) * h * h  # Make first step
            y[n + 1] = y[n] + vy[n] * h + 0.5 * \
                acc2(w, vx[n]) * h * h  # Make first step
            z[n + 1] = z[n] + vz[n] * h + 0.5 * \
                acc3(w, vz[n]) * h * h  # Make first step

            vx[n + 1] = vx[n] + h * acc1(w, vy[n])
            vy[n + 1] = vy[n] + h * acc2(w, vx[n])
            vz[n + 1] = vz[n] + h * acc3(w, vz[n])

            vx[n + 1] = vx[n] + 0.5 * (acc1(w, vy[n]) + acc1(w, vy[n + 1])) * h
            vy[n + 1] = vy[n] + 0.5 * (acc2(w, vx[n]) + acc2(w, vx[n + 1])) * h
            vz[n + 1] = vz[n] + 0.5 * (acc3(w, vz[n]) + acc3(w, vz[n + 1])) * h

    elif direction == 'y':
        x[1] = x[0] + vx0 * h + 0.5 * acc1(w, vz[0]) * h * h  # Make first step
        y[1] = y[0] + vy0 * h + 0.5 * acc3(w, vy[0]) * h * h  # Make first step
        z[1] = z[0] + vz0 * h + 0.5 * acc2(w, vx[0]) * h * h  # Make first step

        vx[1] = vx[0] + h * acc1(w, vz[0])
        vy[1] = vy[0] + h * acc3(w, vy[0])
        vz[1] = vz[0] + h * acc2(w, vx[0])

        for n in range(1, N):

            x[n + 1] = x[n] + vx[n] * h + 0.5 * \
                acc1(w, vz[n]) * h * h  # Make first step
            y[n + 1] = y[n] + vy[n] * h + 0.5 * \
                acc3(w, vy[n]) * h * h  # Make first step
            z[n + 1] = z[n] + vz[n] * h + 0.5 * \
                acc2(w, vx[n]) * h * h  # Make first step

            vx[n + 1] = vx[n] + h * acc1(w, vz[n])
            vy[n + 1] = vy[n] + h * acc3(w, vy[n])
            vz[n + 1] = vz[n] + h * acc2(w, vx[n])

            vx[n + 1] = vx[n] + 0.5 * (acc1(w, vz[n]) + acc1(w, vz[n + 1])) * h
            vy[n + 1] = vy[n] + 0.5 * (acc3(w, vy[n]) + acc3(w, vy[n + 1])) * h
            vz[n + 1] = vz[n] + 0.5 * (acc2(w, vx[n]) + acc2(w, vx[n + 1])) * h

    elif direction == 'x':
        x[1] = x[0] + vx0 * h + 0.5 * acc3(w, vx[0]) * h * h  # Make first step
        y[1] = y[0] + vy0 * h + 0.5 * acc1(w, vz[0]) * h * h  # Make first step
        z[1] = z[0] + vz0 * h + 0.5 * acc2(w, vy[0]) * h * h  # Make first step

        vx[1] = vx[0] + h * acc1(w, vx[0])
        vy[1] = vy[0] + h * acc3(w, vz[0])
        vz[1] = vz[0] + h * acc2(w, vy[0])

        for n in range(1, N):

            x[n + 1] = x[n] + vx[n] * h + 0.5 * \
                acc3(w, vx[n]) * h * h  # Make first step
            y[n + 1] = y[n] + vy[n] * h + 0.5 * \
                acc1(w, vz[n]) * h * h  # Make first step
            z[n + 1] = z[n] + vz[n] * h + 0.5 * \
                acc2(w, vy[n]) * h * h  # Make first step

            vx[n + 1] = vx[n] + h * acc3(w, vx[n])
            vy[n + 1] = vy[n] + h * acc1(w, vz[n])
            vz[n + 1] = vz[n] + h * acc2(w, vy[n])

            vx[n + 1] = vx[n] + 0.5 * (acc3(w, vx[n]) + acc3(w, vx[n + 1])) * h
            vy[n + 1] = vy[n] + 0.5 * (acc1(w, vz[n]) + acc1(w, vz[n + 1])) * h
            vz[n + 1] = vz[n] + 0.5 * (acc2(w, vy[n]) + acc2(w, vy[n + 1])) * h
    return x, y, z


def bounce(h0, vver, vhi, grav, airr, rho, w, r, af, ccw):
    # h0 = initial height [0,10]
    # vver = initial vertical velocity [-50, 50]
    # grav = gravitational field [0.1,100]
    # airr = air resistance coefficient [0, grav-0.1]
    # rho = coefficient of restitution [0, 0.99]
    # w = initial angular velocity [0,90]
    # r = radius of the ball [0.1, 1.0]
    # af = friction coefficient [0, 200]
    # ccw = counterclockwise 'clockwise' or 'cclockwise
    g = (grav - airr)  # applied acceleration         # m/s/s
    t = 0          # starting time
    if h0 < 5:
        dt = 0.01     # time step
    else:
        dt = 0.1
    tau = 0.0001     # contact time for bounce
    hmax = h0      # keep track of the maximum height
    h = h0
    hstop = 0.0001   # stop when bounce is less than 1 cm
    freefall = True  # state: freefall or in contact
    # t_last = -np.sqrt(2*h0/g) # time we would have launched to get to h0 at t=0
    t_last = (-vver - np.sqrt(vver**2 + 2 * h0 * g)) / g
    vmax = np.sqrt(2 * hmax * g)
    H = []
    T = []
    V = []          # velocity list
    W = []
    D = []

    H.append(h0)
    T.append(0)
    V.append(vhi)
    W.append(w)
    D.append(0)
    a = 0           # a is for couting the first impact
    while(hmax > hstop):
        if(freefall):
            hnew = h + vver * dt - 0.5 * g * dt * dt
            if(hnew < 0):
                if a == 0:
                    freefall = False
                    t_last = t + tau
                    h = 0
                    a = t
                else:
                    t = t_last + 2 * np.sqrt(2 * hmax / g)
                    freefall = False
                    t_last = t + tau
                    h = 0
                w = w - af * tau / r - grav * tau / r
            else:
                t = t + dt
                vver = vver - g * dt
                h = hnew
        else:
            t = t + tau
            vmax = vmax * rho
            vver = vmax
            freefall = True
            h = 0
        if a == 0:
            vhf = vhi
            d = vhf * t
        else:
            if ccw == 'clockwise':
                vhf = vhi + w * r
                d = vhf * t - w * r * a
            else:
                vhf = vhi - w * r
                d = vhf * t + w * r * a
        hmax = 0.5 * vmax * vmax / g
        H.append(h)
        T.append(t)
        V.append(vhf)
        W.append(w)
        D.append(d)
    v = V[-1]
    d = D[-1]
    mark = len(W)
    y0 = W[-1]
    x0 = T[-1]
    while(v > 0):
        t = t + dt
        v = v - af * dt  # + (w*r)
        d = d + v * dt
        H.append(0)
        T.append(t)
        D.append(d)
        V.append(v)
    while(v < 0):
        t = t + dt
        v = v + af * dt  # + (w*r)
        d = d + v * dt
        H.append(0)
        T.append(t)
        D.append(d)
        V.append(v)
    x1 = T[-1]
    tt = mark - 1
    aa = np.array(T[tt:-1])
    if len(V) != len(W):
        B = np.log(y0 / 0.00001) / (x0 - x1)
        A = 0.00001 / np.exp(B * x1)
        y = A * np.exp(B * aa)
        if np.exp(B * x1) == 0:
            B = -x1
            A = y0 / (x0 + B)**2
            y = A * (aa + B)**2
        for item in y:
            W.append(item)
    W[-1] = 0
    for j in range(30):
        t = t + dt
        H.append(H[-1])
        D.append(D[-1])
        W.append(W[-1])
        T.append(t)
    return D, H, W, T
