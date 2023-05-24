import numpy as np
import matplotlib.pyplot as plt


def TrackPupilV2020_ExtQuarter_Reflection(Vt, Graphic):
    # Initialize variables

    xc = -1
    yc = -1
    Error = -1

    if Graphic == 1:
        plt.figure(30)
        plt.imshow(Vt, cmap='gray')
        plt.axis('image')
        plt.hold(True)

    TH_255 = 10
    S = Vt.shape
    idx255_v = np.where(np.sum(Vt == 255, axis=1) > TH_255)[0]

    if len(idx255_v) == 0:
        return

    idx255_h = np.where(np.sum(Vt == 255, axis=0) > TH_255)[0]
    idx255_h = np.mean(idx255_h)
    h0 = max(1, int(idx255_h - 50))
    h1 = min(int(idx255_h + 50), S[1])

    ver = np.sum(Vt[:, h0:h1] == 255, axis=1)

    if np.sum(ver) == 0:
        return

    R0 = 10
    R1 = 30

    for v in idx255_v:
        if v > (R1 + 1) and v < (S[0] - R1):
            v0 = np.mean(ver[v - R0 + 1:v + R0 - 1])
            vl = np.mean(ver[v - R1:v - R0])
            vr = np.mean(ver[v + R0:v + R1])
            if v0 > vl and v0 > vr:
                break

    h = np.where(Vt[v, :] == 255)[0]

    R = 30
    x1 = h[0]
    x2 = h[-1]
    y1 = v - R
    y2 = v + R
    xc = int(x1 * 0.5 + x2 * 0.5)
    yc = v
    x1 = xc - R
    x2 = xc + R

    if Graphic == 1:
        plt.plot([x1, x1], [y1, y2], linewidth=2, color='r')
        plt.plot([x2, x2], [y1, y2], linewidth=2, color='r')
        plt.plot([x1, x2], [y1, y1], linewidth=2, color='r')
        plt.plot([x1, x2], [y2, y2], linewidth=2, color='r')

    return xc, yc, Error