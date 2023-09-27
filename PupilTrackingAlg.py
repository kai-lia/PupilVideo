import numpy as np
from scipy.signal import convolve2d
from matplotlib import pyplot as plt
import cv2
import datetime
from datetime import datetime
import time

def PupilTrackingAlg(frame, PupilParam, SYSPARAMS, display):
    DEPTH_OF_BUFFER = 5
    # frame properties 
    frame_size = frame.shape[:2]
    ycBE = frame_size[0]
    xcBE = frame_size[1]
    half_kernel = frame_size[0] / 2
    
    # redundant? RBE = calculate_RBE(half_kernel, PupilParam.pixel_calibration) # sets RBE based on half kernel
        
    """" TODO: hps=get(get(get(himage,'Parent'),'Parent'),'Children'); """
    col1 = [1, 0.5, 0] # were hardcoded in original
    if PupilParam.tracking:
        # Runs tracking function
        PupilParam.x1, PupilParam.x2, PupilParam.y1, PupilParam.y2, PupilParam.track_error = track_pupil_extquarter_reflection(frame, 0) 
    else:
        PupilParam.x1, PupilParam.x2, PupilParam.y1, PupilParam.y2 = [-1, -1, -1, -1]
        PupilParam.track_error = -10
    # Calculate average pupil coordinates
    x0 = np.mean([PupilParam.x1, PupilParam.x2]) # if tracking is not engaged it will be -1
    y0 = np.mean([PupilParam.y1, PupilParam.y2])

    # Initialize recording details
    current_time = datetime.now()
    block_fps = [current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second + current_time.microsecond / 1e6]
    recording = [PupilParam.x1 / PupilParam.pixel_calibration,
                 PupilParam.x2 / PupilParam.pixel_calibration,
                 PupilParam.y1 / PupilParam.pixel_calibration,
                 PupilParam.y2 / PupilParam.pixel_calibration,
                 PupilParam.track_error,
                 block_fps]

    if PupilParam.PTFlag:
        PupilParam.PTData.append(recording)
        
    """ TODO: line 81-93 no idea what the purpose of this code is probabbly irrelavent ****
if PupilParam.Sync==1 & etime(clock,[2000 1 1 0 0 0]) - SYSPARAMS.pupil_duration < 0 cmp"""
    display_tracking_data(PupilParam)
    # Handle FPS counting
    current_fps = handle_fps_counting(PupilParam, block_fps)
    SYSPARAMS.PupilCamerafps = current_fps
    # Handle boundary error visualization
    handle_boundary_error(PupilParam, frame_size, xcBE, ycBE)
    # Handle TCA computation and visualization
    StimParams = 0
    handle_TCA_computation(PupilParam, StimParams, SYSPARAMS, x0, y0, xcBE, ycBE)
    # Handle video saving mechanism
    handle_video_saving(PupilParam)

    PupilParam.Ltotaloffx += 1
    if PupilParam.Ltotaloffx >= (DEPTH_OF_BUFFER - 1): #filter through buffer 5 times
        PupilParam.Ltotaloffx = 0
    
    handle_TCA_computation(PupilParam, StimParams, SYSPARAMS, x0, y0, xcBE, ycBE)

    handle_video_saving(PupilParam)
    
    handle_focus_measure(PupilParam, frame, frame_size)

    PupilParam.idx_reftime += 1 # increments each run


def calculate_RBE(half_kernel, pixel_calibration):
    """  Calcs RBE 
        Note: RBE: Region of Pupil Boundary Error 
        The values of RBE determine the size of the region used for pupil tracking,
        and they are calculated based on the pixel calibration.
    """
    RBE = [5 * pixel_calibration, 10 * pixel_calibration, 15 * pixel_calibration]
    if RBE[2] > half_kernel:
        RBE[2] = 0
    if RBE[1] > half_kernel:
        RBE[1] = 0
    if RBE[0] > half_kernel:
        RBE[0] = 0
    return RBE

def display_tracking_data(PupilParam):
    """
    Display tracking data on the UI or console
    """
    if PupilParam.track_error > -1: # TODO: check running value
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
    

def handle_fps_counting(PupilParam, block_fps):
    """ Manage FPS counting for the pupil tracking.
    Updates FPS values in a buffer and resets the reference index
    when the end of the buffer is reached. The difference between the current time
    and the previous reference time is calculated to determine the FPS for the
    current frame.
    """
    # Calculate FPS for the current frame and update buffer
    if PupilParam.idx_reftime >= 10:
        PupilParam.idx_reftime = 0
    #time dif
    PupilParam.fps[PupilParam.idx_reftime] = etime(block_fps, PupilParam.reftime)
    # Update reference time for the next frame
    PupilParam.reftime = block_fps
    # Calculate current FPS
    if np.sum(PupilParam.fps == 0) == 0:
        current_fps = np.round(1 / np.mean(PupilParam.fps))
    else:
        current_fps = 0
    # Update index for reference time
    return current_fps

def etime(end, start):
     # Convert to datetime objects
    dt_start = datetime(start[0], start[1], start[2], start[3], start[4], int(start[5]), int((start[5] % 1) * 1e6))
    dt_end = datetime(end[0], end[1], end[2], end[3], end[4], int(end[5]), int((end[5] % 1) * 1e6))
    # Calculate the difference
    time_difference = dt_end - dt_start
    # Get the difference in seconds (including fractional seconds)
    diff_seconds = time_difference.total_seconds()
    return diff_seconds
    

def handle_boundary_error(PupilParam,frame_size, xcBE, ycBE):
    """
    Handle boundary errors and visualize accordingly.
    """
    # Determine the center of the frame
    half_frame_height = round(frame_size[0] / 2)
    half_frame_width = round(frame_size[1] / 2)
    calibration_distance = PupilParam.pixel_calibration
    
     # Check for boundary error flag
    if PupilParam.BEFlag == 1:

        # Set vertical centerline visualization
        PupilParam.r1.set_xdata([half_frame_width] * frame_size[0])
        PupilParam.r1.set_ydata(range(1, frame_size[0] + 1))
        PupilParam.r1.set_linewidth(6)
        PupilParam.r1.set_color([1, 0, 0])
        
        # Set additional vertical markers visualization
        vertical_markers_ydata = np.concatenate([
            np.arange(half_frame_height - calibration_distance, -calibration_distance, -calibration_distance),
            np.arange(half_frame_height + calibration_distance, frame_size[0] + calibration_distance, calibration_distance)
        ])
        PupilParam.r2.set_xdata([half_frame_width] * len(vertical_markers_ydata))
        PupilParam.r2.set_ydata(vertical_markers_ydata)
        PupilParam.r2.set_linewidth(2)
        PupilParam.r2.set_color([1, 0, 0])

        # Set horizontal centerline visualization
        PupilParam.r3.set_xdata(range(1, frame_size[1] + 1))
        PupilParam.r3.set_ydata([half_frame_height] * frame_size[1])
        PupilParam.r3.set_linewidth(6)
        PupilParam.r3.set_color([1, 0, 0])

        # Set additional horizontal markers visualization
        horizontal_markers_xdata = np.concatenate([
            np.arange(half_frame_width - calibration_distance, -calibration_distance, -calibration_distance),
            np.arange(half_frame_width + calibration_distance, frame_size[1] + calibration_distance, calibration_distance)
        ])
        PupilParam.r4.set_xdata(horizontal_markers_xdata)
        PupilParam.r4.set_ydata([half_frame_height] * len(horizontal_markers_xdata))
        PupilParam.r4.set_linewidth(2)
        PupilParam.r4.set_color([1, 0, 0])

    # Reset the visualizations if no boundary error
    else:
        for r in [PupilParam.r1, PupilParam.r2, PupilParam.r3, PupilParam.r4]:
            r.set_xdata([1])
            r.set_ydata([1])

def handle_TCA_computation(PupilParam, StimParams, SYSPARAMS, x0, y0, xcBE, ycBE):
    """
    Handle TCA computation and visualization
    """
    # TCA computation logic goes here
    if PupilParam.track_error > -1:
        gray_color = [0.75, 0.75, 0.75] # color defintion to gray
        difx, dify = calculate_line_dif(PupilParam, x0, y0, xcBE, ycBE)
            
        # Style the reference line
        PupilParam.l4.set_color(gray_color)
        PupilParam.l4.set_linewidth(2)
            
        # Calculate the distance and TCA values
        distance = np.sqrt(difx ** 2 + dify ** 2) / PupilParam.pixel_calibration
        calculate_TCA(SYSPARAMS, PupilParam, difx, dify)
        
        SYSPARAMS.pupil_TCA_x = PupilParam.TCAmmX * difx / PupilParam.pixel_calibration
        SYSPARAMS.pupil_TCA_y = PupilParam.TCAmmY * dify / PupilParam.pixel_calibration
        
        TCA_compensation(PupilParam, SYSPARAMS, StimParams)
       
        SYSPARAMS.pupil_diff_x[PupilParam.Ltotaloffx - 1] = difx / PupilParam.pixel_calibration
        SYSPARAMS.pupil_diff_y[PupilParam.Ltotaloffx - 1] = dify / PupilParam.pixel_calibration
         # Handle message display based on FPS
        message = TCA_message(SYSPARAMS.PupilCamerafps, difx, dify, SYSPARAMS.pupil_TCA_x, SYSPARAMS.pupil_TCA_y, PupilParam.pixel_calibration)
        print(message)
        
        # print "stop help.." if distance exceeds threshold
        if distance > PupilParam.tolerated_pupil_dist:
            print("stop help distance exceeds threshold")
    else: # Handle the case when tracking is not happening
        TCA_no_tracking(PupilParam, SYSPARAMS)
        
        
def calculate_line_dif(PupilParam, x0, y0, xcBE, ycBE):
    rx0Ref=(PupilParam.Refx2 + PupilParam.Refx1)/2;
    ry0Ref=(PupilParam.Refy2 + PupilParam.Refy1)/2;
    if PupilParam.show_reference:
        PupilParam.l4.set_xdata([rx0Ref, x0])
        PupilParam.l4.set_ydata([ry0Ref, y0])
        difx = rx0Ref - x0
        dify = ry0Ref - y0
    else:
        PupilParam.l4.set_xdata([xcBE / 2, x0])
        PupilParam.l4.set_ydata([ycBE / 2, y0])
        difx = round(xcBE / 2 - x0)
        dify = round(ycBE / 2 - y0)
    return difx, dify

def calculate_TCA(SYSPARAMS, PupilParam, difx, dify):
    SYSPARAMS.pupil_TCA_x = PupilParam.TCAmmX * difx / PupilParam.pixel_calibration
    SYSPARAMS.pupil_TCA_y = PupilParam.TCAmmY * dify / PupilParam.pixel_calibration
    
def TCA_compensation(PupilParam, SYSPARAMS, StimParams):
    """
    TCA Compensation refers to methods used to correct for this aberration, 
    ensuring that all colors in an image focus at the same point and overlap as intended.
    """
    if PupilParam.EnableTCAComp == 1:
        # Compute the arcmn of TCA based on subject's own ratio
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
                    
def TCA_message(current_fps, difx, dify, pupil_TCA_x, pupil_TCA_y, pixel_calibration):
    """
    Handle message display based on FPS.
    """
    if current_fps < 10:
        message = f'Hz= {current_fps}fps mm({difx / pixel_calibration:.1f}, ' \
                  f'{dify / pixel_calibration:.1f}) TCA=' \
                  f'{np.sqrt(pupil_TCA_x ** 2 + pupil_TCA_y ** 2):.1f}'
    else:
        message = f'Hz={current_fps}fps mm({difx / pixel_calibration:.1f}, ' \
                  f'{dify / pixel_calibration:.1f}) TCA=' \
                  f'{np.sqrt(pupil_TCA_x ** 2 + pupil_TCA_y ** 2):.1f}'

    return message
                    
def TCA_no_tracking(PupilParam, SYSPARAMS):
    PupilParam.l4.set_xdata([1])
    PupilParam.l4.set_ydata([1])
    
    # Construct tracking message
    focus_measure_msg  = f'fps={SYSPARAMS.PupilCamerafps} no tracking'
    print(focus_measure_msg)

    # Set tracking and difference parameters to default values
    SYSPARAMS.pupil_TCA_x = -10000
    SYSPARAMS.pupil_TCA_y = -10000
    SYSPARAMS.pupil_diff_x[PupilParam.Ltotaloffx] = -10000
    SYSPARAMS.pupil_diff_y[PupilParam.Ltotaloffx] = -10000

def handle_video_saving(PupilParam):
    """
    Manage the video saving mechanism
    """
    # The exact logic for this needs to be confirmed
    # This is just a skeleton of the function
    if PupilParam.saving_video and PupilParam.FrameCount < PupilParam.MAX_NUM_OF_SAVABLE_FRAMES and \
            time.time() - PupilParam.toc > PupilParam.SAVING_FREQUENCY:
        VideoToSave.append(event.Data)
        PupilParam.FrameCount += 1
        PupilParam.tic()
    else:
        if PupilParam.saving_video and PupilParam.FrameCount >= PupilParam.MAX_NUM_OF_SAVABLE_FRAMES:
            PupilParam.saving_video = False
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
                PupilData = {'Data': PupilParam.PTData, 'Pixel_calibration': PupilParam.pixel_calibration}
                np.savez(f'./VideoAndRef/{Prefix}DataPupil_{DateString}.npz', PupilData)
                PupilParam.reset_PTData()
    pass

def handle_focus_measure(PupilParam, event, frame_size):
    """
    Computes the focus measure of a region of interest (ROI) in an image 
    based on the Laplacian filter and then appends it to a provided string.
    """
    focus_measure_msg = ""
    # Check if the show_focus attribute is set to 1
    if PupilParam.show_focus == 1:
        # Extract the region of interest from the image
        roi = event.Data[round(frame_size[0]/2)-30 : round(frame_size[0]/2)+30, 0:frame_size[1]]
        # Convert the region to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        # Apply the Laplacian filter to the grayscale region
        FM = cv2.filter2D(np.float64(gray_roi), -1, PupilParam.LAP, borderType=cv2.BORDER_REPLICATE)
        # Compute the square of the filtered image and then its mean value
        FM = round(np.mean(FM**2))
        # Update the focus_measure_msg  variable
        focus_measure_msg = f"{focus_measure_msg} F={FM}"
    
    return focus_measure_msg 

# """ Finding the elipse in the pupil"""
# def track_pupil_extquarter_reflection(A, Graphic):
#     Error = 0
#     x1, x2, y1, y2 = -1, -1, -1, -1
#     Vt = np.round((A[:,:,0] + A[:,:,1] + A[:,:,2])/3)
#     if Graphic == 1:
#         plt.figure(30)
#         plt.imshow(Vt, cmap='gray')
#         plt.axis('image')
    
#     TH_255 = 10
#     S = Vt.shape
#     idx255_v = np.where(np.sum(Vt.T == 255, axis=0) > TH_255)
#     if len(idx255_v) == 0:
#         Error = -1
#         return x1, x2, y1, y2, Error

# ### Work here
#     idx255_h = np.where(np.sum(Vt == 255, axis=0) > TH_255)
#     idx255_h = np.mean(idx255_h)
#     h0 = round(max(1, idx255_h-50))
#     h1 = round(min(idx255_h+50, S[1]))

#     ver = np.sum(Vt[:,h0:h1].T == 255, axis=0)
#     if np.sum(ver) == 0:
#         Error = -2
#         return x1, x2, y1, y2, Error

#     R0 = 10
#     R1 = 30
#     for v in idx255_v[0]:
#         if v > (R1+1) and v < (S[0]-R1):
#             v0 = np.mean(ver[v-R0+1:v+R0-1])
#             vl = np.mean(ver[v-R1:v-R0])
#             vr = np.mean(ver[v+R0:v+R1])
#             if v0 > vl and v0 > vr:
#                 break

#     h = np.where(Vt[v,:] == 255)[0]
#     R = 30
#     x1 = h[0]
#     x2 = h[-1]
#     y1 = v-R
#     y2 = v+R
#     xc = x1*0.5 + x2*0.5
#     x1 = xc-R
#     x2 = xc+R
    
#     """TODO: learn how to display graphic on cur frame"""
#     return x1, x2, y1, y2, Error


def track_pupil_extquarter_reflection(image, is_graph):
    """Finding the coordinates of 2 elipse reflections in the pupil.

    Args:
        image (_type_): Input image to find reflection on.
        is_graph (bool): True if we want to display the image while the process is running.

    Returns:
        Tuple: (x1, x2, y1, y2, error) where x1, y1 represents center of first elipse and vice versa.
        (error = -1 if no verticle reflection is found, -2 if no horizontal reflection is found and 0 if no errors)
    """
    assert len(image.shape) == 3 and image.shape[2] >= 3, "Image has wrong dimensions! It has to be in"
    if len(image.shape) == 3 and image.shape[2] >= 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    if is_graph:
        plt.figure(30)
        plt.imshow(image, cmap='gray')
        plt.axis('image')
    
    occurence_over255_threshold = 10
    x1=-1; x2=-1; y1=-1; y2=-1;
    search_range = 50 # How much we are searching around center of white pixels
    
    # Check for verticle reflections
    verticle_reflections_coords = np.where(np.sum(image == 255, axis=0) > occurence_over255_threshold)
    if len(verticle_reflections_coords) == 0:
        return x1, x2, y1, y2, -1
    center_y = np.mean(verticle_reflections_coords)
    
    # Check for horizontal reflections
    horizontal_reflections_coords = np.where(np.sum(image == 255, axis=1) > occurence_over255_threshold)
    if len(horizontal_reflections_coords) == 0:
        return x1, x2, y1, y2, -2
    center_x = np.mean(horizontal_reflections_coords)
    
    search_start = round(max(0, center_x - search_range))
    search_end = round(min(center_x + search_range, image.shape[1]))
    
    summed_verticle_reflections_row = np.sum(image[:, search_start:search_end].T == 255, axis=1)
    
    r0, r1 = 10, 30
    
    for verticle_index in verticle_reflections_coords:
        if not (verticle_index > (r1 + 1) and verticle_index < (image.shape[0] - r1)):
            continue
        
        # Compute the means v0, vl, and vr
        v0 = np.mean(summed_verticle_reflections_row[verticle_index - r0 + 1 : verticle_index + r0])
        vl = np.mean(summed_verticle_reflections_row[verticle_index - r1 : verticle_index - r0])
        vr = np.mean(summed_verticle_reflections_row[verticle_index + r0 : verticle_index + r1 + 1])  # Include the stop index in Python
        
        # Check if v0 is greater than both vl and vr
        if v0 > vl and v0 > vr:
            break  # Exit the loop if the condition is met
        
        
    h = np.where(image[verticle_index,:] == 255)[0]
    print(verticle_index)
    R = 30
    x1 = h[0]
    x2 = h[-1]
    y1 = verticle_index-R
    y2 = verticle_index+R
    xc = x1*0.5 + x2*0.5
    x1 = xc-R
    x2 = xc+R
    
    """TODO: learn how to display graphic on cur frame"""
    return x1, x2, y1, y2, 0