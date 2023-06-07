import numpy as np
import TrackPupil_Quarter_Reflection_3 as Track_QR_3
import time
global SysParams, StimParams
global PupilParams
global VideoToSave


def PupilTrackingAlg(self, PupilParam, CalibrationSettings, CameraSettings):
    self.PupilParam = PupilParam
    self.CalibrationSettings = CalibrationSettings
    self.CameraSettings = CameraSettings
    DEPTH_OF_BUFFER = 5

    kernel_size = event.Data.shape # size of the structuring element for morphological operations

    # set image data in himage object
    himage.set_array(event.Data)

    xcBE = kernel_size[1]
    ycBE = kernel_size[0]

    # colors for lines
    orange = [1, 0.5, 0]
    red = [0.75, 0, 0]

    """ RBE: Region of Pupil Boundary Error
    The values of RBE determine the size of the region used for pupil tracking,
    and they are calculated based on the pixel calibration."""
    half_kernel = kernel_size[0] / 2

    RBE = [5 * self.PupilParam.get_Pixel_calibration(), 10 * self.PupilParam.get_Pixel_calibration(), 15 * self.PupilParam.get_Pixel_calibration()]
    if RBE[2] > half_kernel:
        RBE[2] = 0
    if RBE[1] > half_kernel:
        RBE[1] = 0
    if RBE[0] > half_kernel:
        RBE[0] = 0
    hps = himage.axes.get_children()

    """This part of the code performs the following actions:

        hps = himage.axes.get_children(): This line retrieves the children of the himage.axes object and assigns them to the hps
         variable. It seems like h-image is an object representing an image, and himage.axes represents the axes of the image.
          The children of the axes are typically the plot elements associated with the image, such as labels, legends, etc.
        
        if not self.PupilParam.get_DisableTracking(): ... else: ...: This block of code checks whether tracking is disabled 
        (DisableTracking flag is set). If tracking is not disabled, it calls the TrackPupil_Quarter_Reflection function with 
        event.Data as an argument to track the pupil. The returned values (x1, x2, y1, y2, TrackError) are assigned to the 
        corresponding attributes of self.PupilParam. If tracking is disabled, the values are reset to default values 
        (0 in this case)."""
    if not self.PupilParam.get_DisableTracking():
        """If we are not tracking set the x1-y2 to the Quarter reflection coords 
            aka: drawing the box"""
        quarter = Track_QR_3.TrackPupil_Quarter_Reflection(event.Data.astype(np.double), 0)
        self.PupilParam.set_x1(quarter[0])
        self.PupilParam.set_x2(quarter[1])
        self.PupilParam.set_y1(quarter[2])
        self.PupilParam.set_y2(quarter[3])
        self.PupilParam.set_TrackError([4])

    else:
        error = 0
        self.PupilParam.reset_x1()
        self.PupilParam.reset_x2()
        self.PupilParam.reset_y1()
        self.PupilParam.reset_y2()

        self.PupilParam.reset_TrackError()

    x0 = np.mean([self.PupilParam.get_x1(), self.PupilParam.get_x2()]) # mean
    y0 = np.mean([self.PupilParam.get_y1(), self.PupilParam.get_y2()]) # mean

    block_fps = np.array(time.clock())
    recording = np.array(
        [self.PupilParam.get_x1() / self.PupilParam.get_Pixel_calibration(), self.PupilParam.get_x2() / self.PupilParam.get_pixel_calibration(),
         self.PupilParam.get_y1() / self.PupilParam.get_Pixel_calibration(), self.PupilParam.get_y2() / self.PupilParam.get_pixel_calibration(),
         self.PupilParam.get_TrackError(), block_fps])

    if self.PupilParam.get_PTFlag():
        self.PupilParam.set_PTData(np.vstack((self.PupilParam.get_PTData, recording)))

    gc = get(hps[6], 'BackgroundColor')
    if self.PupilParam.get_Sync() and time.etime(time.clock(), [2000, 1, 1, 0, 0, 0]) - SysParams.PupilDuration < 0:
        if gc[0] == 0.75:
            set(hps[6], 'String', 'Recording ...')
            set(hps[6], 'BackgroundColor', orange)
        self.PupilParam.set_DataSync(np.vstack((self.PupilParam.get_DataSync, recording)))
    else:
        if gc[0] == 1:
            set(hps[6], 'String', 'Wait for Sync')
            set(hps[6], 'BackgroundColor', red)
    h = get(himage, 'Parent')
    set(h, 'NextPlot', 'add')

    # Update GUI
    set(hps[0], 'String', 'X1: ' + str(int(self.PupilParam.get_x1())) + ' Y1: ' + str(int(self.PupilParam.get_y1())))
    set(hps[1], 'String', 'X2: ' + str(int(self.PupilParam.get_x2())) + ' Y2: ' + str(int(self.PupilParam.get_y2())))
    set(hps[2], 'String', 'Tracking Error: ' + str(int(self.PupilParam.get_TrackError())))

    # Update StimParams struct
    StimParams.CurrentFrame = StimParams.CurrentFrame + 1

    # Save video frames
    if self.PupilParam.get_SaveVideo():
        if self.PupilParam.get_VideoCount():
            VideoToSave = np.zeros((self.PupilParam.get_MaxFrames(), int(self.PupilParam.get_VideoSize()[0]), int(self.PupilParam.get_VideoSize()[1])))
        VideoToSave[self.PupilParam.get_VideoCount() - 1, :, :] = event.Data
        if self.PupilParam.get_VideoCount() >= self.PupilParam.get_MaxFrames():
            self.PupilParam.set_SaveVideo(False)
            np.save(self.PupilParam.get_VideoName(), VideoToSave)

    # Update buffers for circular average of pupil parameters
    if self.PupilParam.get_PTFlag():
        self.PupilParam.set_PTCount(self.PupilParam.get_PTCount() + 1)
        self.PupilParam.set_PTMean(self.PupilParam.get_PTMean() + recording)
        if self.PupilParam.get_PTCount() >= self.PupilParam.get_PTDuration():
            self.PupilParam.set_PTData[self.PupilParam.get_PTCurrent(), :] = self.PupilParam.get_PTMean() / self.PupilParam.get_PTCount()
            self.PupilParam.set_PTCurrent(np.mod(self.PupilParam.get_PTCurrent() + 1, self.PupilParam.get_PTNumBlocks))
            self.PupilParam.set_PTCount(0)
            self.PupilParam.set_PTMean(np.zeros(recording.shape))

    # Update gaze history buffers
    if self.PupilParam.get_PTFlag():
        self.PupilParam.set_HistCount(self.PupilParam.get_HistCount + 1)
        self.PupilParam.get_HistData[self.PupilParam.get_HistCurrent, :] = recording
        self.PupilParam.get_HistCurrent = np.mod(self.PupilParam.get_HistCurrent() + 1, self.PupilParam.get_HistNumBlocks())
        if self.PupilParam.get_HistCount() >= self.PupilParam.get_HistDuration():
            self.PupilParam.set_HistCount(0)

    # Update time elapsed since last recording
    self.PupilParam.get_CurrentTime = time.clock()
    self.PupilParam.get_TimeElapsed = self.PupilParam.get_CurrentTime - self.PupilParam.get_LastTime

    # Check for pupil size change to update dilation filter
    self.PupilParam.set_PupilSize(np.mean([self.PupilParam.get_x2() - self.PupilParam.get_x1(), self.PupilParam.get_y2 - self.PupilParam.get_y1]))
    if self.PupilParam.get_PupilSize() != self.PupilParam.get_LastPupilSize():
        self.PupilParam.set_DilateFilter(dilationFilter(self.PupilParam.get_PupilSize(), self.PupilParam.get_DilateFilterSize()))
        self.PupilParam.set_LastPupilSize(self.PupilParam.get_PupilSize())

    # Update last time for time elapsed calculation
    self.PupilParam.set_LastTime(self.PupilParam.get_CurrentTime())

    # Return updated values
    return self.PupilParam.get_x1(), self.PupilParam.get_x2()