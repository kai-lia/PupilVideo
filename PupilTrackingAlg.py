import numpy as np
from scipy.signal import convolve2d
from matplotlib import pyplot as plt
import cv2
import datetime
import time

def PupilTrackingAlg(frame, PupilParam, SYSPARAMS):
    DEPTH_OF_BUFFER = 5
    
    frame_size = frame.shape[:2]
    print(frame_size)
    ycBE = frame_size[0]
    xcBE = frame_size[1]
    
    #fps =17
    half_kernel = ycBE /2
    
    # RBE: Region of Pupil Boundary Error
    # The values of RBE determine the size of the region used for pupil tracking,
    # and they are calculated based on the pixel calibration.
    RBE = [5 * PupilParam.pixel_calibration, 10 * PupilParam.pixel_calibration, 15 * PupilParam.pixel_calibration]
    if RBE[2] > half_kernel:
        RBE[2] = 0
    if RBE[1] > half_kernel:
        RBE[1] = 0
    if RBE[0] > half_kernel:
        RBE[0] = 0
        
    """" TODO: hps=get(get(get(himage,'Parent'),'Parent'),'Children'); 
    something regarding the ui control !!
    intese struct"""

    col1 = [1, 0.5, 0]

    if not PupilParam.get_tracking(): # to run our actual trackign alg
        PupilParam.x1, PupilParam.x2, PupilParam.y1, PupilParam.y2, PupilParam.TrackError = 0 #TrackPupilV2020_ExtQuarter_Reflection_3(double(event.Data),0);track_pupil(frame, 0) 
    else:
        Error = 0
        PupilParam.x1 = -1
        PupilParam.x2 = -1
        PupilParam.y1 = -1
        PupilParam.y2 = -1
        PupilParam.TrackError = -10

    x0 = np.mean([PupilParam.x1, PupilParam.x2]) # if tracking is not engaged it will be -1
    y0 = np.mean([PupilParam.y1, PupilParam.y2])

    block_fps = 0 #time.localtime() note set to clock
    recording = [PupilParam.x1 / PupilParam.pixel_calibration,
                 PupilParam.x2 / PupilParam.pixel_calibration,
                 PupilParam.y1 / PupilParam.pixel_calibration,
                 PupilParam.y2 / PupilParam.pixel_calibration,
                 PupilParam.TrackError,
                 block_fps]

    if PupilParam.get_PTFlag():
        PupilParam.PTData.append(recording)
        
    """ TODO: line 81-93 no idea what the purpose of this code is probabbly irrelavent ****
if PupilParam.Sync==1 & etime(clock,[2000 1 1 0 0 0]) - SYSPARAMS.pupil_duration < 0 cmp"""

#error checking around line 85
    if PupilParam.track_error > -1:
        rx = [PupilParam.x1, PupilParam.x2, PupilParam.x2, PupilParam.x1, PupilParam.x1]
        ry = [PupilParam.y1, PupilParam.y1, PupilParam.y2, PupilParam.y2, PupilParam.y1]

        PupilParam.p1.set_xdata(rx)
        PupilParam.p1.set_ydata(ry)
        PupilParam.p1.set_linewidth(2)
        PupilParam.p1.set_color(col1)
    else:
        PupilParam.p1.set_xdata([1])
        PupilParam.p1.set_ydata([1])

    if PupilParam.show_reference == 1:
        c = [0.75, 0, 0]
        rx0Ref = (PupilParam.Refx2 + PupilParam.Refx1) / 2
        ry0Ref = (PupilParam.Refy2 + PupilParam.Refy1) / 2
        rx = [PupilParam.Refx1, PupilParam.Refx2, PupilParam.Refx2, PupilParam.Refx1, PupilParam.Refx1]
        ry = [PupilParam.Refy1, PupilParam.Refy1, PupilParam.Refy2, PupilParam.Refy2, PupilParam.Refy1]

        PupilParam.l3.set_xdata(rx)
        PupilParam.l3.set_ydata(ry)
        PupilParam.l3.set_color(c)
        PupilParam.l3.set_linewidth(2)
    else:
        PupilParam.l3.set_xdata([1])
        PupilParam.l3.set_ydata([1])

    PupilParam.idx_reftime += 1
    
    
    
    #why??
    if PupilParam.idx_reftime > 10:
        PupilParam.idx_reftime = 1
    else:
        PupilParam.idx_reftime += 1
        
        
    print(type(block_fps))
    print(type(PupilParam.reftime))

    # Second part
    PupilParam.fps[PupilParam.idx_reftime] = block_fps - PupilParam.reftime # (block_fps - PupilParam.reftime).total_seconds()
    PupilParam.reftime = block_fps

    # Third part
    if np.sum(PupilParam.fps == 0) == 0:
        Current_fps = np.round(1 / np.mean(PupilParam.fps))
    else:
        Current_fps = 0

    # Fourth part
    SYSPARAMS.pupil_camera_fps = Current_fps
    

    if PupilParam.BEFlag == 1:
        H1 = round(s[0] / 2)
        V1 = round(s[1] / 2)
        Dmm = 1 * PupilParam.Pixel_calibration

        PupilParam.r1.set_xdata([V1] * s[0])
        PupilParam.r1.set_ydata(range(1, s[0] + 1))
        PupilParam.r1.set_linewidth(6)
        PupilParam.r1.set_color([1, 0, 0])

        PupilParam.r2.set_xdata([V1] * (2 * R + 1))
        PupilParam.r2.set_ydata(np.concatenate([np.arange(H1 - Dmm, -Dmm, -Dmm),
                                                 np.arange(H1 + Dmm, s[0] + Dmm, Dmm)]))
        PupilParam.r2.set_linewidth(2)
        PupilParam.r2.set_color([1, 0, 0])

        PupilParam.r3.set_xdata(range(1, s[1] + 1))
        PupilParam.r3.set_ydata([H1] * s[1])
        PupilParam.r3.set_linewidth(6)
        PupilParam.r3.set_color([1, 0, 0])

        PupilParam.r4.set_xdata(np.concatenate([np.arange(V1 - Dmm, -Dmm, -Dmm),
                                                np.arange(V1 + Dmm, s[1] + Dmm, Dmm)]))
        PupilParam.r4.set_ydata([H1] * (2 * R + 1))
        PupilParam.r4.set_linewidth(2)
        PupilParam.r4.set_color([1, 0, 0])
    else:
        PupilParam.r1.set_xdata([1])
        PupilParam.r1.set_ydata([1])
        PupilParam.r2.set_xdata([1])
        PupilParam.r2.set_ydata([1])
        PupilParam.r3.set_xdata([1])
        PupilParam.r3.set_ydata([1])
        PupilParam.r4.set_xdata([1])
        PupilParam.r4.set_ydata([1])

    PupilParam.Ltotaloffx += 1
    if PupilParam.Ltotaloffx > DEPTH_OF_BUFFER:
        PupilParam.Ltotaloffx = 1

    if PupilParam.TrackError > -1:
        c = [0.75, 0.75, 0.75]
        if PupilParam.show_reference == 1:
            PupilParam.l4.set_xdata([rx0Ref, x0])
            PupilParam.l4.set_ydata([ry0Ref, y0])
            PupilParam.l4.set_color(c)
            PupilParam.l4.set_linewidth(2)
            difx = rx0Ref - x0
            dify = ry0Ref - y0
        else:
            PupilParam.l4.set_xdata([xcBE / 2, x0])
            PupilParam.l4.set_ydata([ycBE / 2, y0])
            PupilParam.l4.set_color(c)
            PupilParam.l4.set_linewidth(2)
            difx = round(xcBE / 2 - x0)
            dify = round(ycBE / 2 - y0)
        Distance = np.sqrt(difx ** 2 + dify ** 2) / PupilParam.Pixel_calibration
        SYSPARAMS.pupil_TCA_x = PupilParam.TCAmmX * difx / PupilParam.Pixel_calibration
        SYSPARAMS.pupil_TCA_y = PupilParam.TCAmmY * dify / PupilParam.Pixel_calibration
        # *********************************************************************
        if PupilParam.EnableTCAComp == 1:
            # if automatic TCA control is enabled
            # SYSPARAMS.pupil_TCA_x and SYSPARAMS.pupil_TCA_y is arcmn of TCA based on
            # subject's own ratio
            pixperarcmin = SYSPARAMS.pixel_per_deg / 60
            xoffset = round(SYSPARAMS.pupil_TCA_x * pixperarcmin)  # in pixels
            yoffset = round(SYSPARAMS.pupil_TCA_y * pixperarcmin)  # in pixels

            if (abs(xoffset) > 0 or abs(yoffset) > 0) and PupilParam.show_reference == 1:
                PupilParam.totaloffx = StimParams.aomoffs[0, 0] + xoffset
                PupilParam.totaloffy = StimParams.aomoffs[0, 1] - yoffset

                if SYSPARAMS.real_system == 1:
                    aligncommand = f'UpdateOffset#{PupilParam.totaloffx}#{PupilParam.totaloffy}#' \
                                   f'{StimParams.aomoffs[1, 0]}#{StimParams.aomoffs[1, 1]}#' \
                                   f'{StimParams.aomoffs[2, 0]}#{StimParams.aomoffs[2, 1]}#'
                    if SYSPARAMS.board == 'm':
                        MATLABAomControl32(aligncommand)
                    else:
                        netcomm('write', SYSPARAMS.netcommobj, int8(aligncommand))
        # *********************************************************************

        SYSPARAMS.pupil_diff_x[PupilParam.Ltotaloffx - 1] = difx / PupilParam.Pixel_calibration
        SYSPARAMS.pupil_diff_y[PupilParam.Ltotaloffx - 1] = dify / PupilParam.Pixel_calibration
        if Current_fps < 10:
            Stringhps9 = f'Hz= {Current_fps}fps mm({difx / PupilParam.Pixel_calibration:.1f}, ' \
                         f'{dify / PupilParam.Pixel_calibration:.1f}) TCA=' \
                         f'{np.sqrt(SYSPARAMS.pupil_TCA_x ** 2 + SYSPARAMS.pupil_TCA_y ** 2):.1f}'
        else:
            Stringhps9 = f'Hz={Current_fps}fps mm({difx / PupilParam.Pixel_calibration:.1f}, ' \
                         f'{dify / PupilParam.Pixel_calibration:.1f}) TCA=' \
                         f'{np.sqrt(SYSPARAMS.pupil_TCA_x ** 2 + SYSPARAMS.pupil_TCA_y ** 2):.1f}'
        if Distance > PupilParam.TolleratedPupilDistance:
            beep()
    else:
        PupilParam.l4.set_xdata([1])
        PupilParam.l4.set_ydata([1])
        if Current_fps < 10:
            Stringhps9 = f'fps= {Current_fps} no tracking'
        else:
            Stringhps9 = f'fps={Current_fps} no tracking'
        SYSPARAMS.pupil_TCA_x = -10000
        SYSPARAMS.pupil_TCA_y = -10000
        
        print(SYSPARAMS.pupil_diff_x)
        print(PupilParam.Ltotaloffx)
        
        #SYSPARAMS.pupil_diff_x[PupilParam.Ltotaloffx] = -10000
        #SYSPARAMS.pupil_diff_y[PupilParam.Ltotaloffx] = -10000

    if PupilParam.SavingVideo == 1 and PupilParam.FrameCount < PupilParam.MAX_NUM_OF_SAVABLE_FRAMES and \
            time.time() - PupilParam.toc > PupilParam.SAVING_FREQUENCY:
        VideoToSave.append(event.Data)
        PupilParam.FrameCount += 1
        PupilParam.tic()
    else:
        if PupilParam.SavingVideo == 1 and PupilParam.FrameCount >= PupilParam.MAX_NUM_OF_SAVABLE_FRAMES:
            PupilParam.SavingVideo = 0
            # hps[11].set_text('Saving ...')
            # Prefix = hps[7].get_text()
            DateString = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
            np.savez(f'./VideoAndRef/{Prefix}VideoPupil_{DateString}.npz', VideoToSave)
            VideoToSave = []
            # hps[11].set_text('Save Video')
            # hps[11].set_backgroundcolor([0.941176, 0.941176, 0.941176])
            # hps[11].set_foregroundcolor([0, 0, 0])
            if PupilParam.PTFlag == 1:
                PupilParam.PTFlag = 0
                # hps[8].set_text('Save Pupil Tracking')
                # hps[8].set_backgroundcolor([0.941176, 0.941176, 0.941176])
                # hps[8].set_foregroundcolor([0, 0, 0])
                DateString = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
                PupilData = {'Data': PupilParam.PTData, 'Pixel_calibration': PupilParam.Pixel_calibration}
                np.savez(f'./VideoAndRef/{Prefix}DataPupil_{DateString}.npz', PupilData)
                PupilParam.PTData = []

    if PupilParam.show_focus == 1:
        FM = np.mean(np.square(cv2.cvtColor(event.Data[round(s[0] / 2) - 30:round(s[0] / 2) + 30, 0:s[1]], cv2.COLOR_RGB2GRAY)))
        Stringhps9 = f'{Stringhps9} F={FM}'
    # hps[9].set_text(Stringhps9)
    # hps[9].set_horizontalalignment('left')
    
    
    
def track_pupil(A, Graphic):
    Error = 0
    x1, x2, y1, y2 = -1, -1, -1, -1
    Vt = np.round((A[:,:,0] + A[:,:,1] + A[:,:,2])/3)
    if Graphic == 1:
        plt.figure(30)
        plt.imshow(Vt, cmap='gray')
        plt.axis('image')
    
    TH_255 = 10
    S = Vt.shape
    idx255_v = np.where(np.sum(Vt.T == 255, axis=0) > TH_255)
    if len(idx255_v[0]) == 0:
        Error = -1
        return x1, x2, y1, y2, Error

    idx255_h = np.where(np.sum(Vt == 255, axis=0) > TH_255)
    idx255_h = np.mean(idx255_h)
    h0 = round(max(1, idx255_h-50))
    h1 = round(min(idx255_h+50, S[1]))

    ver = np.sum(Vt[:,h0:h1].T == 255, axis=0)
    if np.sum(ver) == 0:
        Error = -2
        return x1, x2, y1, y2, Error

    R0 = 10
    R1 = 30
    for v in idx255_v[0]:
        if v > (R1+1) and v < (S[0]-R1):
            v0 = np.mean(ver[v-R0+1:v+R0-1])
            vl = np.mean(ver[v-R1:v-R0])
            vr = np.mean(ver[v+R0:v+R1])
            if v0 > vl and v0 > vr:
                break

    h = np.where(Vt[v,:] == 255)
    R = 30
    x1 = h[0][0]
    x2 = h[0][-1]
    y1 = v-R
    y2 = v+R
    xc = x1*0.5 + x2*0.5
    yc = v
    x1 = xc-R
    x2 = xc+R

    if Graphic == 1:
        plt.plot([x1, x1], [y1, y2], linewidth=2, color=[0.75, 0, 0])
        plt.plot([x2, x2], [y1, y2], linewidth=2, color=[0.75, 0, 0])
        plt.plot([x1, x2], [y1, y1], linewidth=2, color=[0.75, 0, 0])
        plt.plot([x1, x2], [y2, y2], linewidth=2, color=[0.75, 0, 0])

    return x1, x2, y1, y2, Error