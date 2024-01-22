import numpy as np
from matplotlib import pyplot as plt
import cv2
import datetime
import datetime
from datetime import datetime
import time

def PupilTrackingAlg(frame, PupilParam, SYSPARAMS, display, ax):
    DEpupil_tracking_H_OF_BUFFER = 5
    # frame properties 
    frame_size = frame.shape[:2]
    PupilParam.frame_width = frame_size[1]
    PupilParam.frame_height  = frame_size[0]
    # redundant? RBE = calculate_RBE(half_kernel, PupilParam.pixel_calibration) # sets RBE based on half kernel
    
    """" TODO: hps=get(get(get(himage,'Parent'),'Parent'),'Children'); """
    if PupilParam.tracking:
        # Runs tracking function
        PupilParam.x1, PupilParam.x2, PupilParam.y1, PupilParam.y2, PupilParam.track_error = track_pupil_extquarter_reflection(frame, 0) 
    else:
        PupilParam.x1, PupilParam.x2, PupilParam.y1, PupilParam.y2 = [-1, -1, -1, -1]
        PupilParam.track_error = -10
    # Calculate average pupil coordinates
    PupilParam.center_x = np.mean([PupilParam.x1, PupilParam.x2]) # if tracking is not engaged it will be -1
    PupilParam.center_y = np.mean([PupilParam.y1, PupilParam.y2])

    # Initialize recording details
    current_time = datetime.now()
    block_fps = [current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second + current_time.microsecond / 1e6]
    recording = [PupilParam.x1 / PupilParam.pixel_calibration,
                 PupilParam.x2 / PupilParam.pixel_calibration,
                 PupilParam.y1 / PupilParam.pixel_calibration,
                 PupilParam.y2 / PupilParam.pixel_calibration,
                 PupilParam.track_error,
                 block_fps]
  
    """ TODO: line 81-93 no idea what the purpose of this code is probabbly irrelavent ****
if PupilParam.Sync==1 & etime(clock,[2000 1 1 0 0 0]) - SYSPARAMS.pupil_duration < 0 cmp"""
    #display_tracking_data(PupilParam, ax)
    # Handle FPS counting
    current_fps = handle_fps_counting(PupilParam, block_fps)
    SYSPARAMS.PupilCamerafps = current_fps
    # Handle boundary error visualization
    handle_boundary_error(PupilParam, frame_size)
    # Handle TCA computation and visualization
    StimParams = 0
    handle_TCA_computation(PupilParam, StimParams, SYSPARAMS)
    # Handle video saving mechanism
    #handle_video_saving(PupilParam)

    PupilParam.Ltotaloffx += 1
    if PupilParam.Ltotaloffx >= (DEpupil_tracking_H_OF_BUFFER - 1): #filter through buffer 5 times
        PupilParam.Ltotaloffx = 0
    
    handle_TCA_computation(PupilParam, StimParams, SYSPARAMS)
    
    handle_focus_measure(PupilParam, frame, frame_size)

    PupilParam.idx_reftime += 1 # increments each run


"""def calculate_RBE(half_kernel, pixel_calibration):
     # Calcs RBE 
        #Note: RBE: Region of Pupil Boundary Error 
       # The values of RBE determine the size of the region used for pupil tracking,
       # and they are calculated based on the pixel calibration.
    
    RBE = [5 * pixel_calibration, 10 * pixel_calibration, 15 * pixel_calibration]
    if RBE[2] > half_kernel:
        RBE[2] = 0
    if RBE[1] > half_kernel:
        RBE[1] = 0
    if RBE[0] > half_kernel:
        RBE[0] = 0
    return RBE"""

"""def display_tracking_data(PupilParam, ax):

    #Display tracking data on the UI or console

    if PupilParam.track_error > -1:
        rx = [PupilParam.x1, PupilParam.x2]
        ry = [PupilParam.y1, PupilParam.y2]

        PupilParam.p1 = [rx, ry]
    else:
        PupilParam.p1 = [1, 1]

    if PupilParam.show_reference:
        rx = [PupilParam.ref_x1, PupilParam.ref_x2]
        ry = [PupilParam.ref_y1, PupilParam.ref_y2]
        
        PupilParam.l3 = [rx, ry]
    else:
        PupilParam.l3 = [1, 1]
    """
        

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
    

def handle_boundary_error(PupilParam,frame_size):
    """
    Handle boundary errors and visualize accordingly.
    """
    # Determine the center of the frame
    half_frame_height = round(frame_size[0] / 2)
    half_frame_width = round(frame_size[1] / 2)
    calibration_distance = PupilParam.pixel_calibration
    
    # Check for boundary error flag
    if PupilParam.BEflag:
        # Set vertical centerline visualization
        PupilParam.r1 = [[half_frame_width] * frame_size[0], range(1, frame_size[0] + 1)]
     
        # Set additional vertical markers visualization
        vertical_markers_ydata = np.concatenate([
            np.arange(half_frame_height - calibration_distance, -calibration_distance, -calibration_distance),
            np.arange(half_frame_height + calibration_distance, frame_size[0] + calibration_distance, calibration_distance)
        ])
        PupilParam.r2 = [[half_frame_width] * len(vertical_markers_ydata), vertical_markers_ydata]

        # Set horizontal centerline visualization
        PupilParam.r3 = [range(1, frame_size[1] + 1), [half_frame_height] * frame_size[1]]

        # Set additional horizontal markers visualization
        horizontal_markers_xdata = np.concatenate([
            np.arange(half_frame_width - calibration_distance, -calibration_distance, -calibration_distance),
            np.arange(half_frame_width + calibration_distance, frame_size[1] + calibration_distance, calibration_distance)
        ])
        PupilParam.r4 = [horizontal_markers_xdata, [half_frame_height] * len(horizontal_markers_xdata)]

    # Reset the visualizations if no boundary error
    else:
        for r in [PupilParam.r1, PupilParam.r2, PupilParam.r3, PupilParam.r4]:
            r = [0,0]

def handle_TCA_computation(PupilParam, StimParams, SYSPARAMS):
    """
    Handle TCA computation and visualization
    """
    # TCA computation logic goes here
    if PupilParam.track_error >= -1:
        # Style the reference line
        difx, dify = calculate_line_dif(PupilParam)
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
        
    else: # Handle the case when tracking is not happening
        TCA_no_tracking(PupilParam, SYSPARAMS)
        
        
def calculate_line_dif(PupilParam):
    if PupilParam.show_reference:
        difx = PupilParam.ref_center_x - PupilParam.center_x
        dify = PupilParam.ref_center_y  - PupilParam.center_y
    else:

        PupilParam.l4 = None
        
        difx = round(PupilParam.frame_width / 2 - PupilParam.center_x)
        dify = round(PupilParam.frame_height / 2 - PupilParam.center_y)
    return difx, dify

def calculate_TCA(SYSPARAMS, PupilParam, difx, dify):
    SYSPARAMS.pupil_TCA_x = PupilParam.TCAmmX * difx / PupilParam.pixel_calibration
    SYSPARAMS.pupil_TCA_y = PupilParam.TCAmmY * dify / PupilParam.pixel_calibration
    
def TCA_compensation(PupilParam, SYSPARAMS, StimParams):
    """
    TCA Compensation refers to methods used to correct for this aberration, 
    ensuring that image focus at the same point and overlap as intended.
    """
    if PupilParam.TCA_comp:
        # Compute the arcmn of TCA based on subject's own ratio
        pix_per_arcmin = SYSPARAMS.pixel_per_deg / 60
        x_offset = round(SYSPARAMS.pupil_TCA_x * pix_per_arcmin)  # in pixels
        y_offset = round(SYSPARAMS.pupil_TCA_y * pix_per_arcmin)  # in pixels

        if (abs(x_offset) > 0 or abs(y_offset) > 0) and PupilParam.show_reference:
            PupilParam.totaloffx = StimParams.aomoffs[0, 0] + x_offset
            PupilParam.totaloffy = StimParams.aomoffs[0, 1] - y_offset

            if SYSPARAMS.real_system == 1:
                aligncommand = f'UpdateOffset#{PupilParam.totaloffx}#{PupilParam.totaloffy}#' \
                               f'{StimParams.aomoffs[1, 0]}#{StimParams.aomoffs[1, 1]}#' \
                               f'{StimParams.aomoffs[2, 0]}#{StimParams.aomoffs[2, 1]}#'
                if SYSPARAMS.board == 'm':
                    MATLABAomControl32(aligncommand) #does not exist 
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
    PupilParam.l4 = None
    
    # Construct tracking message
    focus_measure_msg  = f'fps={SYSPARAMS.PupilCamerafps} no tracking'

    # Set tracking and difference parameters to default values
    SYSPARAMS.pupil_TCA_x = -10000
    SYSPARAMS.puPupilParam.BEflagpil_TCA_y = -10000
    SYSPARAMS.pupil_diff_x[PupilParam.Ltotaloffx] = -10000
    SYSPARAMS.pupil_diff_y[PupilParam.Ltotaloffx] = -10000

def handle_video_saving(PupilParam):
    """
    Manage the video saving mechanism
    """
    # The exact logic for this needs to be confirmed
    # This is just a skeleton of the function
    if PupilParam.saving_video and PupilParam.frame_count < PupilParam.MAX_NUM_OF_SAVABLE_FRAMES:
        current_time = datetime.now()
        time_difference = current_time - PupilParam.start_save_time
        if time_difference.total_seconds() > PupilParam.saving_frequency:
            VideoToSave.append(event.Data)
            PupilParam.frame_countt += 1
            PupilParam.start_save_time = current_time
        
    else:
        if PupilParam.saving_video and PupilParam.frame_count >= PupilParam.MAX_NUM_OF_SAVABLE_FRAMES:
            PupilParam.saving_video = False
            DateString = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
            np.savez(f'./VideoAndRef/{Prefix}VideoPupil_{DateString}.npz', VideoToSave)
            VideoToSave = []
            if PupilParam.pupil_tracking_flag == True:
                PupilParam.pupil_tracking_flag = False
                DateString = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
                PupilData = {'Data': PupilParam.pupil_tracking_Data, 'Pixel_calibration': PupilParam.pixel_calibration}
                np.savez(f'./VideoAndRef/{Prefix}DataPupil_{DateString}.npz', PupilData)
                PupilParam.reset_pupil_tracking_Data()
    pass

def handle_focus_measure(PupilParam, frame, frame_size):
    """
    Computes the focus measure of a region of interest (ROI) in an image 
    based on the Laplacian filter and then appends it to a provided string.
    """
    focus_measure_msg = ""
    # Check if the show_focus attribute is set to 1
    if PupilParam.show_focus:
        # Extract the region of interest from the image
        roi = frame[round(frame_size[0]/2)-30 : round(frame_size[0]/2)+30, 0:frame_size[1]]
        # Convert the region to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        # Apply the Laplacian filter to the grayscale region
        laplacian = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)) - 1
        FM = cv2.filter2D(np.float64(gray_roi), -1, laplacian, borderType=cv2.BORDER_REPLICATE)
        # Compute the square of the filtered image and then its mean value
        FM = round(np.mean(FM**2))
        # Update the focus_measure_msg  variable
        focus_measure_msg = f"{focus_measure_msg} F={FM}"
    return focus_measure_msg 

def track_pupil_extquarter_reflection(image, is_graph):

    """Finding the coordinates of 2 elipse reflections in the pupil.
    Args:
        image (_type_): Input image to find reflection on.
        is_graph (bool): True if we want to display the image while the process is running.

    Returns:
        Tuple: (x1, x2, y1, y2, error) where x1, y1 represents center of first elipse and vice versa.
        (error = -1 if there are no white pixel group found, and 0 if no errors)
    """
    assert len(image.shape) == 3 and image.shape[2] >= 3, "Image has wrong dimensions! It has to be in"
    if len(image.shape) == 3 and image.shape[2] >= 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if is_graph:
        plt.figure(30)
        plt.imshow(image, cmap='gray')
        plt.axis('image')
        
    image = cv2.GaussianBlur(image, (5, 5), 0)
    
    white_pixel_threshold = 252
    _, binarized_image = cv2.threshold(image, white_pixel_threshold, 255, cv2.THRESH_BINARY)
    
    # Apply connected component analysis
    num_white_pixel_groups, white_pixel_groups_labels, white_pixel_group_info, white_pixel_group_center_coords = cv2.connectedComponentsWithStats(binarized_image, connectivity=8)
    
    if num_white_pixel_groups > 1:
        # Find the largest connected component (excluding the background)
        largest_label = np.argmax(white_pixel_group_info[1:, cv2.CC_STAT_AREA]) + 1
        # Get the bounding box coordinates of the largest connected component
        x, y, w, h = white_pixel_group_info[largest_label, cv2.CC_STAT_LEFT], white_pixel_group_info[largest_label, cv2.CC_STAT_TOP], \
                    white_pixel_group_info[largest_label, cv2.CC_STAT_WIDTH], white_pixel_group_info[largest_label, cv2.CC_STAT_HEIGHT]
        
        return x, x + w, y, y + h, 0
    
    return 0, 0, 0, 0, -1
    
    
    
