
import numpy as np

def TrackPupil_Quarter_Reflection(A, Graphic):
    # TrackPupilV2020_ExtQuarter_Reflection3 - looking bottom part of the pupil
    # and fit an ellipse (circle)
    # ...
    # (Your function comments here)

    Error = 0
    x1 = -1
    x2 = -1
    y1 = -1
    y2 = -1
    Vt = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
    if Graphic == 1:
        cv2.imshow('Vt', Vt)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    TH_255 = 10
    S = Vt.shape
    idx255_v = np.where(np.sum(Vt == 255, axis=1) > TH_255)[0]
    if idx255_v.size == 0:
        Error = -1
        return x1, x2, y1, y2, Error

    idx255_h = np.where(np.sum(Vt == 255, axis=0) > TH_255)[0]
    idx255_h = np.mean(idx255_h)
    h0 = max(1, idx255_h - 50)
    h1 = min(idx255_h + 50, S[1])

    ver = np.sum(Vt[:, h0:h1] == 255, axis=1)
    if np.sum(ver) == 0:
        Error = -2
        return x1, x2, y1, y2, Error

    R0 = 10
    R1 = 30
    for v in idx255_v:
        if (v > (R1 + 1) and v < (S[0] - R1)):
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
    xc = x1 * 0.5 + x2 * 0.5
    yc = v
    x1 = xc - R
    x2 = xc + R

    if Graphic == 1:
        cv2.rectangle(A, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return x1, x2, y1, y2, Error






