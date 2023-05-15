import numpy as np
import PupilParam
import TrackPupil_Quarter_Reflection_3 as Track_QR_3
import time


def PupilTrackingAlg(obj, event, himage):
    DEPTH_OF_BUFFER = 5

    # global variables
    global SysParams, StimParams
    global PupilParams
    global VideoToSave

    kernel_size = event.Data.shape # size of the structuring element for morphological operations

    #set image data in himage object
    himage.set_array(event.Data)

    xcBE = kernel_size[1]
    ycBE = kernel_size[0]

    RBE = [5 * PupilParam.Pixel_calibration, 10 * PupilParam.Pixel_calibration, 15 * PupilParam.Pixel_calibration]
    if RBE[2] > (kernel_size[0] / 2):
        RBE[2] = 0
    if RBE[1] > (kernel_size[0] / 2):
        RBE[1] = 0
    if RBE[0] > (kernel_size[0] / 2):
        RBE[0] = 0

    hps = himage.axes.get_children()
    col1 = [1, 0.5, 0]

    if PupilParam.DisableTracking == 0:
        PupilParam.x1, PupilParam.x2, PupilParam.y1, \
        PupilParam.y2, PupilParam.TrackError = Track_QR_3.TrackPupil_Quarter_Reflection(event.Data.astype(np.double), 0)
    else:
        Error = 0
        PupilParam.x1 = -1
        PupilParam.x2 = -1
        PupilParam.y1 = -1
        PupilParam.y2 = -1
        PupilParam.TrackError = -10

    x0 = np.mean([PupilParam.x1, PupilParam.x2])
    y0 = np.mean([PupilParam.y1, PupilParam.y2])

    Block_fps = np.array(time.clock())
    Recording = np.array(
        [PupilParam.x1 / PupilParam.Pixel_calibration, PupilParam.x2 / PupilParam.Pixel_calibration,
         PupilParam.y1 / PupilParam.Pixel_calibration, PupilParam.y2 / PupilParam.Pixel_calibration,
         PupilParam.TrackError, Block_fps])

    if PupilParam.PTFlag == 1:
        PupilParam.PTData = np.vstack((PupilParam.PTData, Recording))

    gc = get(hps[6], 'BackgroundColor')
    if PupilParam.Sync == 1 and time.etime(time.clock(), [2000, 1, 1, 0, 0, 0]) - SysParams.PupilDuration < 0:
        if gc[0] == 0.75:
            set(hps[6], 'String', 'Recording ...')
            set(hps[6], 'BackgroundColor', [1, 0.5, 0])
        PupilParam.DataSync = np.vstack((PupilParam.DataSync, Recording))
    else:
        if gc[0] == 1:
            set(hps[6], 'String', 'Wait for Sync')
            set(hps[6], 'BackgroundColor', [0.75, 0, 0])
    h = get(himage, 'Parent')
    set(h, 'NextPlot', 'add')

    # Update GUI
    set(hps[0], 'String', 'X1: ' + str(int(PupilParam.x1)) + ' Y1: ' + str(int(PupilParam.y1)))
    set(hps[1], 'String', 'X2: ' + str(int(PupilParam.x2)) + ' Y2: ' + str(int(PupilParam.y2)))
    set(hps[2], 'String', 'Tracking Error: ' + str(int(PupilParam.TrackError)))

    # Update StimParams struct
    StimParams.CurrentFrame = StimParams.CurrentFrame + 1

    # Save video frames
    if PupilParam.SaveVideo == 1:
        if PupilParam.VideoCount == 1:
            VideoToSave = np.zeros((PupilParam.MaxFrames, int(PupilParam.VideoSize[0]), int(PupilParam.VideoSize[1])))
        VideoToSave[PupilParam.VideoCount - 1, :, :] = event.Data
        if PupilParam.VideoCount >= PupilParam.MaxFrames:
            PupilParam.SaveVideo = 0
            np.save(PupilParam.VideoName, VideoToSave)

        # Update buffers for circular average of pupil parameters
    if PupilParam.PTFlag == 1:
        PupilParam.PTCount = PupilParam.PTCount + 1
        PupilParam.PTMean = PupilParam.PTMean + Recording
        if PupilParam.PTCount >= PupilParam.PTDuration:
            PupilParam.PTData[PupilParam.PTCurrent, :] = PupilParam.PTMean / PupilParam.PTCount
            PupilParam.PTCurrent = np.mod(PupilParam.PTCurrent + 1, PupilParam.PTNumBlocks)
            PupilParam.PTCount = 0
            PupilParam.PTMean = np.zeros(Recording.shape)

        # Update gaze history buffers
    if PupilParam.PTFlag == 1:
        PupilParam.HistCount = PupilParam.HistCount + 1
        PupilParam.HistData[PupilParam.HistCurrent, :] = Recording
        PupilParam.HistCurrent = np.mod(PupilParam.HistCurrent + 1, PupilParam.HistNumBlocks)
        if PupilParam.HistCount >= PupilParam.HistDuration:
            PupilParam.HistCount = 0

        # Update time elapsed since last recording
    PupilParam.CurrentTime = time.clock()
    PupilParam.TimeElapsed = PupilParam.CurrentTime - PupilParam.LastTime

    # Check for pupil size change to update dilation filter
    PupilParam.PupilSize = np.mean([PupilParam.x2 - PupilParam.x1, PupilParam.y2 - PupilParam.y1])
    if PupilParam.PupilSize != PupilParam.LastPupilSize:
        PupilParam.DilateFilter = dilationFilter(PupilParam.PupilSize, PupilParam.DilateFilterSize)
        PupilParam.LastPupilSize = PupilParam.PupilSize

    # Update last time for time elapsed calculation
    PupilParam.LastTime = PupilParam.CurrentTime

    # Update display

    # Return updated values
    return PupilParam.x1, PupilParam.x2, PupilParam