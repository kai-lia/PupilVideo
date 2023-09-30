import cv2
import numpy as np
import matplotlib.patches as patches

# Implement the default Matplotlib key bindings.
from PIL import ImageTk

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

import tkinter as tk
from PIL import ImageTk, Image
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from data_structures import CameraSettings
from data_structures import CalibrationSettings
import os
from PupilTrackingAlg import PupilTrackingAlg
from tkinter import simpledialog
import sys
import datetime
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
from matplotlib.widgets import Slider
from PupilParam import *
from SYSPARAMS import *
import datetime
from datetime import datetime

import tkinter.filedialog
import tkinter.messagebox
import traceback
import json
import scipy.io as sio
from pathlib import Path
import io

import base64

"""  displaying error messages in GUI"""
def exception_troubleshoot(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            traceback.print_exception(*sys.exc_info())
            tkinter.messagebox.showerror(message=str(e) + '\n (Full traceback printed in console.)')

    return wrapper


class ProjectorGUI:
    def __init__(self):
        self.tk_root = tk.Tk()
        self.tk_root.geometry('1100x600')
        self.tk_root.title('PupilVideoTrackingV2')
        self.type_pupil_file_name_prefix = ""
        self.PupilParam = PupilParam()
        self.SYSPARAMS = SYSPARAMS()
        self.CalibrationSettings = CalibrationSettings()
        self.CameraSettings = CameraSettings()
        self.PupilTracker = None
        self.video_frame = None
        self.ax = None
        self.camera = None # setting camera for my mac is 0
        current_time = datetime.now()
        self.PupilParam.reftime= [current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second + current_time.microsecond / 1e6]

        # Create top, left, middle, and right frames formatting
        top_frame = tk.Frame(self.tk_root)
        top_frame.pack(side="top", fill="both")
        self.make_top_frame(top_frame)

        # left frame creation
        left_frame = tk.Frame(self.tk_root)
        left_frame.pack(side="left", expand=True, fill='both')
        self.make_left_frame(left_frame)

        # middle frame creation
        middle_frame = tk.Frame(self.tk_root)
        middle_frame.pack(side="left", expand=True, fill='both')
        self.make_middle_frame(middle_frame)

        # right frame creation
        right_frame = tk.Frame(self.tk_root)
        right_frame.pack(side="left", expand=True, fill='both')
        self.make_right_frame(right_frame)
       
    def make_top_frame(self, top_frame):
        """makes the top button bar, horizontal layout
        buttons : Quit, Start Video, Set Refernce, Load Refernce, Disable Tracking, Zoom In, Draw BE
        """
        # buttons
        self.tk_quit_button = tk.Button(top_frame, text="Quit", command=self.tk_quit)
        self.tk_quit_button.pack(side='left', expand=True, fill='both')
        self.tk_start_video_button = tk.Button(top_frame, text="Start Video", command=self.tk_start_video)
        self.tk_start_video_button.pack(side='left', expand=True, fill='both')
        self.tk_reference_button = tk.Button(top_frame, text="Set Reference", command=self.tk_set_reference)
        self.tk_reference_button.pack(side='left', expand=True, fill='both')
        self.tk_load_reference_button = tk.Button(top_frame, text="Load Reference", command=self.tk_load_reference)
        self.tk_load_reference_button.pack(side='left', expand=True, fill='both')
        self.tk_tracking_button = tk.Button(top_frame, text="Disable Tracking",
                                                    command=self.tk_disable_tracking)
        self.tk_tracking_button.pack(side='left', expand=True, fill='both')
        self.tk_zoom_in_button = tk.Button(top_frame, text="Zoom In", command=self.tk_zoom_in)
        self.tk_zoom_in_button.pack(side='left', expand=True, fill='both')
        self.tk_draw_be_button = tk.Button(top_frame, text="Draw BE", command=self.tk_draw_be)
        self.tk_draw_be_button.pack(side='left', expand=True, fill='both')

    def make_left_frame(self, left_frame):
        """makes the left side of screen, vertical layout
        buttons: Sync Save, Save Video
        box for Save Video Settings:
          entries: secs, fps
        button: Save Pupil Tracking
        entry: Type Pupil File Name"""
        # buttons
        self.tk_sync_button = tk.Button(left_frame, text="Sync Save", command=self.tk_sync_save)
        self.tk_sync_button.pack(expand=True)
        self.tk_save_video_button = tk.Button(left_frame, text="Save Video", command=self.tk_save_video)
        self.tk_save_video_button.pack(expand=True)

        # Box for Save Video Settings
        save_video_frame = tk.Frame(left_frame, highlightbackground="black", highlightthickness=2)
        save_video_frame.pack(side="top", expand=True, fill='both')
        self.tk_save_video_settings_label = tk.Label(save_video_frame, text="Save Video Settings")
        self.tk_save_video_settings_label.pack(side="top")
        save_video_frame_left = tk.Frame(save_video_frame)
        save_video_frame_left.pack(side="left", expand=True, fill='both')
        save_video_frame_right = tk.Frame(save_video_frame)
        save_video_frame_right.pack(side="left", expand=True, fill='both')
        # entries
        self.tk_secs_label = tk.Label(save_video_frame_left, text="Secs")
        self.tk_secs_label.pack(side='top', expand=True, fill='both')
        self.tk_secs_entry = tk.Entry(save_video_frame_right, textvariable=self.tk_secs)
        self.tk_secs_entry.pack(side='top', expand=True, fill='both')
        self.tk_fps_label = tk.Label(save_video_frame_left, text="FPS")
        self.tk_fps_label.pack(side='bottom', expand=True, fill='both')
        self.tk_fps_entry = tk.Entry(save_video_frame_right, textvariable=self.tk_FPS)
        self.tk_fps_entry.pack(side='bottom', expand=True, fill='both')

        # button
        self.tk_save_pupil_tracking_button = tk.Button(left_frame, text="Save Pupil Tracking",
                                                       command=self.tk_save_pupil_tracking)
        self.tk_save_pupil_tracking_button.pack(expand=True)
        # entry
        save_fps_label_frame = tk.Frame(left_frame)
        save_fps_label_frame.pack(side="top", expand=True, fill='both')
        self.tk_type_pupil_file_name_prefix_label = tk.Label(save_fps_label_frame, text="Type Pupil File Name Prefix")
        self.tk_type_pupil_file_name_prefix_label.pack(expand=True, fill='both')
        self.tk_type_pupil_file_name_prefix_entry = tk.Entry(save_fps_label_frame,
                                                              textvariable=self.tk_type_pupil_file_name_prefix)
        self.tk_type_pupil_file_name_prefix_entry.pack(side="bottom", expand=True, fill='both')

    def make_right_frame(self, right_frame):
        """makes the right side of screen, vertical layout
        box for Video Camera Settings:
          buttons: auto, reset, save settings, load settings
          sliders: brightness, gamma, exposure, gain
        button: Enable TCA correction
        box for Calibration Settings:
          entry: tollernc(.mm), TCA(X/Y)arcmin/mm
          button: Show Focus"""
        # Box for video camera settings
        video_camera_frame = tk.Frame(right_frame, highlightbackground="black", highlightthickness=2)
        video_camera_frame.pack(side="top", expand=True, fill='both')

        self.tk_video_camera_settings_label = tk.Label(video_camera_frame, text="Video Camera Settings")
        self.tk_video_camera_settings_label.pack(side="top")
        video_camera_frame_top = tk.Frame(video_camera_frame)
        video_camera_frame_top.pack(side="top",expand=True, fill='x')
        # buttons
        self.tk_automatic_button = tk.Button(video_camera_frame_top, text="Auto", command=self.tk_auto)
        self.tk_automatic_button.pack(side="left", expand=True, fill='x')
        self.tk_reset_button = tk.Button(video_camera_frame_top, text="Reset", command=self.tk_reset)
        self.tk_reset_button.pack(side="left", expand=True, fill='x')
        self.tk_save_settings_button = tk.Button(video_camera_frame_top, text="Save Settings", command=self.tk_save_settings)
        self.tk_save_settings_button.pack(side="left", expand=True, fill='x')
        self.tk_load_settings_button = tk.Button(video_camera_frame_top, text="Load Settings", command=self.tk_load_settings)
        self.tk_load_settings_button.pack(side="left", expand=True, fill='x')
        # sliders frame
        video_camera_frame_sliders = tk.Frame(video_camera_frame)
        video_camera_frame_sliders.pack(side="bottom", expand=False, fill='both')

        # sliders
        fig, ax = plt.subplots(figsize=(2, 2))
        ax.axis('off')  # Hide the axes

        # Define the position and size of the sliders
        slider_width = 0.3
        slider_height = 0.02
        slider_left = 0.45
        slider_top = 0.9
        slider_horizontal_pad = 0.2

        # Create the sliders
        brightness_slider_ax = fig.add_axes([slider_left, slider_top - slider_height, slider_width, slider_height])
        brightness_slider = Slider(brightness_slider_ax, 'Brightness', 0, 4095, valinit=240)
       
        gamma_slider_ax = fig.add_axes(
            [slider_left, slider_top - slider_height - 1 * (slider_height + slider_horizontal_pad), slider_width,
             slider_height])
        gamma_slider = Slider(gamma_slider_ax, 'Gamma', 0, 5, valinit=1, valfmt="%0.0f")

        exposure_slider_ax = fig.add_axes(
            [slider_left, slider_top - slider_height - 2 * (slider_height + slider_horizontal_pad), slider_width,
             slider_height])
        exposure_slider = Slider(exposure_slider_ax, 'Exposure', 0, 4, valinit=0.0333)

        gain_slider_ax = fig.add_axes(
            [slider_left, slider_top - slider_height - 3 * (slider_height + slider_horizontal_pad), slider_width,
             slider_height])
        gain_slider = Slider(gain_slider_ax, 'Gain', 0, 48, valinit=0)

        brightness_slider.on_changed(self.tk_brightness_change)
        gamma_slider.on_changed(self.tk_gamma_change)
        exposure_slider.on_changed(self.tk_exposure_change)
        gain_slider.on_changed(self.tk_gain_change)

        video_canvas = FigureCanvasTkAgg(fig, master=video_camera_frame)
        video_canvas.draw()
        video_canvas.get_tk_widget().pack(side="top", fill='x', expand=True)

        self.tk_enable_tca_correction_button = tk.Button(right_frame, text="Enable TCA Correction",
                                                         command=self.tk_enable_tca_correction)
        self.tk_enable_tca_correction_button.pack()
        # calibration settings box
        calibration_frame = tk.Frame(right_frame, highlightbackground="black", highlightthickness=2)
        calibration_frame.pack(side="top", expand=True, fill='both')
        self.tk_calibration_label = tk.Label(calibration_frame, text="Calibration Settings")
        self.tk_calibration_label.pack(side="top")
        # button
        self.tk_focus_button = tk.Button(calibration_frame, text="Show Focus", textvariable=self.tk_show_focus)
        self.tk_focus_button.pack(side="right", expand=True, fill='x')
        # entries framing
        calibration_frame_top = tk.Frame(calibration_frame)
        calibration_frame_top.pack(side="bottom", expand=True, fill='both')
        calibration_frame_bottom = tk.Frame(calibration_frame)
        calibration_frame_bottom.pack(side="bottom", expand=True, fill='both')
        # entries
        self.tk_tollernc_mm_label = tk.Label(calibration_frame_top, text="tollernc.(mm)")
        self.tk_tollernc_mm_label.pack(side="left", expand=True, fill='both')
        self.tk_tollernc_mm_entry = tk.Entry(calibration_frame_top, textvariable=self.tk_tollernc_mm)
        self.tk_tollernc_mm_entry.insert(0, 0.15)
        self.tk_tollernc_mm_entry.pack(side="left", expand=True, fill='both')

        self.tk_TCA_XY_arcmin_mm_label = tk.Label(calibration_frame_bottom, text="TCA(X/Y)arcmin/mm")
        self.tk_TCA_XY_arcmin_mm_label.pack(side="left", expand=True, fill='both')
        self.tk_TCA_XY_arcmin_mm_entry = tk.Entry(calibration_frame_bottom, textvariable=self.tk_TCA_XY_arcmin_mm)
        self.tk_TCA_XY_arcmin_mm_entry.insert(0, "3.5/3.5")
        self.tk_TCA_XY_arcmin_mm_entry.pack(side="left", expand=True, fill='both')

        video_camera_frame.mainloop()


    def make_middle_frame(self, middle_frame):
        # open video source (by default this will try to open the computer webcam)
        # creating figure
        fig, self.ax = plt.subplots(figsize=(5, 5))
        self.ax.tick_params(axis='both', which='major', labelsize=5) # change axis font size bc why not
        self.video_canvas = FigureCanvasTkAgg(fig, master=middle_frame)
        # self.video_canvas.draw() when graphing
        # placing the toolbar on the Tkinter window
        self.video_canvas.get_tk_widget().pack(side="top", fill=None, expand=False)

        self.video_frame = tk.Label(master=middle_frame, height=5, width=5)
        self.video_frame.pack(side="top", fill='both', expand=True)
    
    def tk_quit(self):
        """Button 1: quits and exits program (button 1) if dataScn will save the file"""
        self.set_PupilTracker(0);
        if self.PupilParam.DataSync is not None:
            date_string = time.strftime('%Y-%m-%d_%H-%M-%S')
            pupil_data = self.PupilParam.DataSync
            file = open(f'./VideoAndRef/Trial_DataPupil_{self.get_type_pupil_file_name_prefix()}_{date_string}')
            file.write(pupil_data)
            file.close()
        self.tk_root.destroy()

    def tk_start_video(self):
        """Button 2: starts video
        also layer with existing graph so we can plot on video """
        self.camera = cv2.VideoCapture(0)
        
        # Camera settings
        self.set_camera_values()
        
        # Resolution settings
        width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.PupilParam.vidRes = [width, height]
         
       # sets vid Calibration factors
        self.set_video_calibration()
        # set the plot values for future work
        self.set_plots()
        #start video loop
        self.PupilParam.video = True
        self.video_stream()
        # update button state
        self.tk_start_video_button.configure(text="Stop Video", command=self.tk_stop_video)

    def set_video_calibration(self):
            """Set video calibration factors."""
            self.PupilParam.pixel_calibration = self.CalibrationSettings.get_pixel_calibration()
            self.PupilParam.TCAmmX = self.CalibrationSettings.get_TCAmmX()
            self.PupilParam.TCAmmY = self.CalibrationSettings.get_TCAmmY()
            self.PupilParam.tolerated_pupil_dist = self.CalibrationSettings.get_tolerated_pupil_dist()
        
        
    def tk_stop_video(self):
        """ stops video"""
        self.PupilParam.video = False
        self.camera.release()
        cv2.destroyAllWindows()
        # update button state
        self.tk_start_video_button.configure(text="Start Video", command=self.tk_start_video)

    def video_stream(self):
        " consistent loop until stop vid "
        if not self.PupilParam.video:
            return
        # Read a frame from the video feed
        ret, frame = self.camera.read() 
        # If the frame isn't read correctly, exit
        if not ret:  
            return
        #calls and exicutes our trackign 
        print("before")
        print(self.PupilParam.x1, self.PupilParam.x2, self.PupilParam.y1, self.PupilParam.y2)
        PupilTrackingAlg(frame, self.PupilParam, self.SYSPARAMS, self.video_frame.pack()) # Process the frame for pupil tracking
        print("after")
        print(self.PupilParam.x1, self.PupilParam.x2, self.PupilParam.y1, self.PupilParam.y2)
        
        
        # color fix and storage
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # fixes color
        PupilParam.lap = cv2.Laplacian(frame_rgb, cv2.CV_64F) # laplacian edge detection filter
        #display steps
        self.display_video_frame(frame_rgb)
        #update
        self.video_frame.after(33, self.video_stream) # after is the #fps future edit pls

    def display_video_frame(self, frame_rgb):
        """
        Display the frame on the user interface.
        """
        self.ax.clear() #clear for less storage
        
        if (self.PupilParam.x1 != -1):
            print("hi")
        rect1 = patches.Rectangle((self.PupilParam.x1, self.PupilParam.y1), 40, 30, linewidth=1, edgecolor='r')
        rect2 = patches.Rectangle((self.PupilParam.x2, self.PupilParam.y2), 40, 30, linewidth=1, edgecolor='r')
        
        self.ax.imshow(frame_rgb, aspect='auto')
        self.video_canvas.draw()
        self.video_canvas.get_tk_widget().pack()
        self.video_frame.pack()
    
    def tk_set_reference(self):
        """Button 3: sets reference
        Get mouse coordinates then set reference to it"""
        self.video_canvas.get_tk_widget().config(cursor='cross')
        self.cid = self.video_canvas.mpl_connect('button_press_event', self.tk_set_reference_click)
        
    def tk_set_reference_click(self, event):
        print(f'You clicked at coordinates: ({event.xdata}, {event.ydata})')
        x = event.xdata
        y = event.ydata
        
        ref_x1 = round(x)-30
        ref_x2 = round(x)+30
        ref_y1 = round(y)-30
        ref_y2 = round(y)-30
        
        self.PupilParam.x1 = ref_x1
        self.PupilParam.x2 = ref_x2
        self.PupilParam.y1= ref_y1
        self.PupilParam.y2 = ref_y2
        
        date_string = time.strftime('%Y-%m-%d_%H-%M-%S')
        # TODO: Save reference coordinates like matlab file
        # np.savez('./VideoAndRef/RefPupil_' + date_string, Refx1=ref_x1, Refx2=ref_x2, Refy1=ref_y1, Refy2=ref_y2)
        
        self.video_canvas.get_tk_widget().config(cursor='')
        self.video_canvas.mpl_disconnect(self.cid)
        self.tk_reference_button.configure(text="Unset Reference", command=self.tk_unset_reference)
        

    def tk_load_reference(self):
        """ Button 4: loads then sets reference from a RefPupil_ file
            after, set reference button should now be unset reference
        """
        self.tk_root.withdraw()
        file_name = tk.filedialog.askopenfilename(title='Select RefPupil file', initialdir=os.getcwd())

        if file_name:

            path, file = os.path.split(file_name)
            if file.startswith('RefPupil_'):
                reference_data = sio.loadmat(file_name)

                self.PupilParam.x1 = reference_data['Refx1'][0][0]
                self.PupilParam.x2 = reference_data['Refx2'][0][0]
                self.PupilParam.y1 = reference_data['Refy1'][0][0]
                self.PupilParam.y2 = reference_data['Refy2'][0][0]

                self.tk_reference_button.configure(text="Unset Reference", command=self.tk_unset_reference)
            else:
                print("Invalid file name. File must start with 'RefPupil_'")
        return

    def tk_unset_reference(self):
        """unsets reference
            should only appear as a button option after setting or loading reference"""
        self.PupilParam.reset_x1()
        self.PupilParam.reset_x2()
        self.PupilParam.reset_y1()
        self.PupilParam.reset_y2()
        ##TODO: make sure box is de-initilized
        self.tk_reference_button.configure(text="Set Reference", command=self.tk_set_reference)
        return
    
# BE triggering button
    def tk_draw_be(self):
        """Button 7: draws BE"""
        self.PupilParam.BEFlag = True
        self.tk_draw_be_button.configure(text='Hide BE', command=self.tk_hide_be)

    def tk_hide_be(self):
        """hides BE"""
        self.PupilParam.BEFlag = False
        self.tk_draw_be_button.configure(text='Draw BE',  command=self.tk_draw_be)

    def tk_sync_save(self):
        """Button 9: sync save"""
        if (self.PupilParam.video):
            self.tk_sync_wait()
            return
        self.PupilParam.save_sync()
        self.tk_automatic_button.configure(text="Wait for Sync", command=self.tk_sync_wait)
        if len(self.PupilParam.DataSync):
            date_string = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            # TODO: Prefix = get(handles.edit3, 'String')
            prefix = " "
            pupil_data = self.PupilParam.DataSync
            # Save PupilData to a file
            file_name = f"./VideoAndRef/Trial_DataPupil_{prefix}_{date_string}.txt"
            with open(file_name, 'w') as file:
                file.write(str(pupil_data))
            self.PupilParam.reset_DataSync()
        return

    def tk_sync_wait(self):
        """sync wait"""
        self.PupilParam.wait_sync()
        self.PupilParam.reset_DataSync()
        self.tk_automatic_button.configure(text="Sync Save", command=self.tk_sync_save)
        return

    def tk_save_video(self):
        """Button 5: save video"""
        if self.PupilParam.video and not self.PupilParam.saving_video:
            self.PupilParam.saving_video = True
            self.PupilParam.FrameCount= 1
            VideoToSave = []
            start_time = datetime.datetime.now()

            if not self.PupilParam.PTFlag:
                self.PupilParam.PTFlag = True
                self.PupilParam.PTT0 = datetime.datetime.now()
                self.tk_save_pupil_tracking_button.configure(text='Recording Pupil ...')
                self.PupilParam.reset_PTData()

        else:
            if self.PupilParam.video and self.PupilParam.saving_video:
                self.PupilParam.saving_video =False
                Prefix = input('Enter Prefix: ')  # Get prefix from user
                self.tk_save_video_button.configure(text='Save Video')
                date_string = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                np.save(f"./VideoAndRef/{Prefix}VideoPupil_{date_string}.npy", VideoToSave)
                VideoToSave = []

                if self.PupilParam.PTFlag:
                    self.PupilParam.PTFlag = False
                    self.tk_save_pupil_tracking_button.configure(text='Save Pupil Tracking')
                    PupilData = {
                        'Data': self.PupilParam.PTData,
                        'Pixel_calibration': self.PupilParam.pixel_calibration
                    }
                    np.save(f"./VideoAndRef/{Prefix}DataPupil_{date_string}.npy", PupilData)
                    self.PupilParam.reset_PTData()

    def tk_secs(self):
        """ with new value entry the savable frames/freq changes"""
        secs = self.tk_secs_entry.get()
        fps = self.tk_fps_entry.get()
        self.PupilParam.MAX_NUM_OF_SAVABLE_FRAMES = secs*fps
        self.PupilParam.saving_frequency = 1/fps
        return

    def tk_FPS(self):
        """ with new value entry the savable frames/freq changes"""
        secs = self.tk_secs_entry.get()
        fps = self.tk_fps_entry.get()
        self.PupilParam.MAX_NUM_OF_SAVABLE_FRAMES = secs*fps
        self.PupilParam.saving_frequency = 1/fps
        return

    def tk_save_pupil_tracking(self):
        """ Button 8: values collected nothing functally needed """
        if self.PupilParam.video and not self.PupilParam.PTFlag:
            self.PupilParam.PTFlag = True
            self.PupilParam.PTTO = datetime.datetime.now()
            self.tk_save_pupil_tracking_button.configure(text='Recording Pupil ...')
            block_fps = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.PupilParam.PTData = [0, 0, 0, 0, 0, block_fps]

            if SYSPARAMS.board == 'm':
                MATLABAomControl32('MarkFrame#')
            else:
                # marks the video frame when the subject responds.
                netcomm('write', SYSPARAMS.netcommobj, int8('MarkFrame#'))

        else:
            if self.PupilParam.video and self.PupilParam.PTFlag:
                self.PupilParam.PTFlag = False
                self.tk_save_pupil_tracking_button.configure(text='Save Pupil Tracking')
                date_string = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                PupilData = {
                    'Data': self.PupilParam.PTData,
                    'Pixel_calibration': self.PupilParam.Pixel_calibration
                }
                Prefix = input('Enter Prefix: ')  # Get prefix from user
                np.save(f"./VideoAndRef/{Prefix}DataPupil_{date_string}.npy", PupilData)
                self.PupilParam.reset_PTData()
        return

    def tk_type_pupil_file_name_prefix(self):
        ROOT = tk.Tk()
        ROOT.withdraw()
        self.prefix = simpledialog.askstring(title="Test",
                                            prompt="Enter Prefix:")

    def get_type_pupil_file_name_prefix(self):
        return self.type_pupil_file_name_prefix

    def tk_auto(self):
        """ makes controls of video settings automatic """
        self.CameraSettings.auto_exposure_mode()
        if self.PupilParam.video:
            self.set_camera_values()
            return
        self.tk_automatic_button.configure(text="Manual", command=self.tk_manual)

    def tk_manual(self):
        """Button 10: makes controls of video settings manual """
        self.CameraSettings.manual_exposure_mode()
        if self.PupilParam.video:
            self.set_camera_values()
        self.tk_automatic_button.configure(text="Auto", command=self.tk_auto)
        

    def tk_save_settings(self):
        """Button 11: hmmm"""
        global CameraSetting
        CS = CameraSetting
        np.save('CS.npy', CS)
        return

    def tk_load_settings(self):
        """Button 12: loads from past file of camera settings"""
        try:
            self.CameraSettings = np.load('CS.npy', allow_pickle=True).item()
            print("Settings loaded successfully.")
        except FileNotFoundError:
            print("No settings file found.")

    def tk_reset(self):
        """Button 13: resets camera values to starting values"""
        self.CameraSettings.reset_brightness()
        self.CameraSettings.reset_iris()
        self.CameraSettings.reset_exposure()
        self.CameraSettings.reset_exposure_mode() # sets to manual exposure
        self.CameraSettings.get_gain()
        # TODO: make it so it will work when video is running
        return

    def tk_enable_tca_correction(self):
        """Button 14: """
        original_color = [0.941176, 0.941176, 0.941176]
        self.PupilParam.enable_TCA_comp()
        self.PupilParam.totaloffx = []
        self.PupilParam.totaloffy = []
        
        # Update button properties to indicate TCA correction is enabled
        self.tk_focus_button.configure(text="Disable TCA Correction",
                                       command=self.tk_disable_tca_correction)
        
        """Button 14: """
    
        self.PupilParam.enable_TCA_comp()
        self.PupilParam.totaloffx
        



    def tk_disable_tca_correction(self):
        """Button 14: """
        original_color = [0.941176, 0.941176, 0.941176]
        self.PupilParam.disable_TCA_comp()
         
        if self.SYSPARAMS.realsystem == 1:
            # Equivalent Python code for the MATLAB aligncommand logic
            aligncommand = 'UpdateOffset#'
            
            for i in range(3): # 3 pos 
                x_offset = self.StimParams.aomoffs[i][0]
                y_offset = self.StimParams.aomoffs[i][1]
                aligncommand += f"{x_offset}#{y_offset}#"
            # Check board type and send the command
            if self.SYSPARAMS.board == 'm':
                """TODO: Call to MATLABAomControl32 goes here; however, the exact Python equivalent is unknown""" 
            else:
                """ TODO: Call to netcomm goes here; the exact Python equivalent is unknown"""
                pass
            
        self.PupilParam.disable_TCA_comp()

        # Reset button to original properties
        self.tk_focus_button.configure(text="Enable TCA Correction",
                                       command=self.tk_enable_tca_correction)
        

    def tk_disable_tracking(self):
        """ Button 15 disables tracking"""
        self.PupilParam.disable_tracking()
        self.tk_tracking_button.configure(text="Enable Tracking", command=self.tk_enable_tracking)
        return

    def tk_enable_tracking(self):
        """Button 15 enables tracking"""
        self.PupilParam.enable_tracking()
        self.tk_tracking_button.configure(text="Disable Tracking", command=self.tk_disable_tracking)
        return

    """zooms in"""
    def tk_zoom_in(self):
        """Button 16: zooms in"""
        return
    
    def tk_show_focus(self):
        """Button 21: shows focus """
        self.PupilParam.show_focus()
        self.tk_focus_button.configure(text="Hide Focus", command=self.tk_hide_focus)
        return
    
    def tk_hide_focus(self):
        """Button 21: hides focus """
        self.PupilParam.hide_focus()
        self.tk_focus_button.configure(text="Show Focus", command=self.tk_show_focus)
        return
       
       

    def tk_tollernc_mm(self, val):
        """"""
        self.CalibrationSetting.set_tolerated_pupil_diststr2num(val)
        
        return

    def tk_TCA_XY_arcmin_mm(self, Str):
        idx = Str.find('/')
        if idx != -1:
            self.CalibrationSetting.set_TCAmmX(float(Str[:idx]))
            self.CalibrationSetting.set_TCAmmY(float(Str[idx+1:]))
            print("TCAmmX and TCAmmY updated.")
        else:
            print("Invalid input string.")



    ######## sliders ###########

    def tk_brightness_change(self, val):
        """Slider 3: brightness slider moved"""
        self.CameraSettings.set_brightness(val)
        if self.PupilParam.video:
            self.camera.set(cv2.CAP_PROP_BRIGHTNESS, val)
        return

    def tk_gamma_change(self, val):
        """Slider 4: slider moved"""
        self.CameraSettings.set_gamma(val)
        if  self.PupilParam.video:
            self.camera.set(cv2.CAP_PROP_GAMMA, val)
            print(val)
        return

    def tk_exposure_change(self, val):
        """Slider 5: slider moved"""
        self.CameraSettings.set_exposure(val)
        if self.PupilParam.video:
            self.camera.set(cv2.CAP_PROP_EXPOSURE, val)
            print(val)
        return

    def tk_gain_change(self, val):
        """Slider 6: slider moved"""
        self.CameraSettings.set_gain(val)
        if self.PupilParam.video:
            self.camera.set(cv2.CAP_PROP_GAIN, val)
            print(val)
        return
    
    def set_plots(self):
        """sets the l,p,r for future algorithm work"""
        plot_attributes = ['l3', 'l4', 'l5', 'l6', 'l7', 'l8', 'p1', 'v1', 'v2', 'v3',
                           'v4', 'c1', 'c2', 'c3', 'c4', 'c5', 'r1', 'r2', 'r3', 'r4']
        for attr in plot_attributes:
            setattr(self.PupilParam, attr, self.ax.plot(1, 1)[0])


    def set_camera_values(self):
        """used when setting values mid video"""
        self.camera.set(cv2.CAP_PROP_BRIGHTNESS, self.CameraSettings.get_brightness())
        self.camera.set(cv2.CAP_PROP_GAMMA, self.CameraSettings.get_gamma())
        self.camera.set(cv2.CAP_PROP_EXPOSURE, self.CameraSettings.get_exposure())
        self.camera.set(cv2.CAP_PROP_GAIN, self.CameraSettings.get_gain())

        if self.CameraSettings.get_exposure_mode():
            self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        else:
            self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        # TODO: Fix this
       # self.camera.set(cv2.CAP_PROP_POS_FRAMES, self.CameraSettings.get_roi())

        frame_rate = self.camera.get(cv2.CAP_PROP_FPS)
        exposure = self.camera.get(cv2.CAP_PROP_EXPOSURE)
        gain = self.camera.get(cv2.CAP_PROP_GAIN)
        gamma = self.camera.get(cv2.CAP_PROP_GAMMA)
        exposure_auto = self.camera.get(cv2.CAP_PROP_AUTO_EXPOSURE)

        print("Frame Rate:\t", frame_rate)
        print("Exposure:\t", exposure)
        print("Gain:\t\t", gain)
        print("Gamma:\t\t", gamma)
        print("ExposureAuto:\t", exposure_auto)
        
        # Getter and Setter methods for PupilTracker
    def get_PupilTracker(self):
        return self.PupilTracker

    def set_PupilTracker(self, value):
        self.PupilTracker = value
        
    def main_loop(self):
        "main loop functioning for intitlization"
        self.tk_root.mainloop()

""" initializes and runs entirety of code"""
if __name__ == "__main__":
    tg = ProjectorGUI()
    tg.main_loop()
