import os
import csv
from tkinter import simpledialog

import cv2
import sys
import datetime
import numpy as np 
import tkinter as tk
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import tkinter.filedialog
import tkinter.messagebox
import traceback
import scipy.io as sio

# Implement the default Matplotlib key bindings.
from PIL import ImageTk, Image

from tkinter import *

from matplotlib.figure import Figure
import matplotlib.patches as patches
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler

from data_structures import CameraSettings, CalibrationSettings

from datetime import datetime
from PupilParam import *
from SYSPARAMS import *
from PupilTrackingAlg import PupilTrackingAlg

from cv2 import VideoCapture
from cv2 import waitKey

# Implement the default Matplotlib key bindings.

# Reset 
plt.rcdefaults()

"""  displaying error messages in GUI"""
def exception_troubleshoot(func):
    print("exception_troubleshoot")
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
        self.tk_root.geometry('1750x600')
        self.tk_root.title('PupilVideoTrackingV2')
        self.type_pupil_file_name_prefix = ""
        self.PupilParam = PupilParam()
        self.SYSPARAMS = SYSPARAMS()
        self.CalibrationSettings = CalibrationSettings()
        self.CameraSettings = CameraSettings()
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
        buttons : Quit, Start Video, Set Refernce, Load Refernce, Disable Tracking, Draw BE
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
        self.tk_TCA_X_arcmin_mm_entry = tk.Entry(calibration_frame_bottom, textvariable=self.tk_TCA_XY_arcmin_mm)
        self.tk_TCA_Y_arcmin_mm_entry = tk.Entry(calibration_frame_bottom, textvariable=self.tk_TCA_XY_arcmin_mm)
        self.tk_TCA_X_arcmin_mm_entry.insert(0, "3.5")
        self.tk_TCA_Y_arcmin_mm_entry.insert(0, "3.5")
        
        self.tk_TCA_Y_arcmin_mm_entry.pack(side="left", expand=True, fill='both')
        self.tk_TCA_XY_arcmin_mm_divide = tk.Label(calibration_frame_bottom, text="/")
        self.tk_TCA_XY_arcmin_mm_divide.pack(side="left", expand=True, fill='both')
        self.tk_TCA_X_arcmin_mm_entry.pack(side="left", expand=True, fill='both')

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
        if self.PupilParam.saving_video:
            self.tk_recording_video()
        if self.PupilParam.pupil_tracking_flag:
            self.tk_recording_pupil()
        self.tk_root.destroy()

    def tk_start_video(self):
        """Button 2: starts video
        also layer with existing graph so we can plot on video """
        self.PupilParam.video = True
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
        #start video loop
    
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
        self.PupilParam.sync = False
        self.camera.release()
        cv2.destroyAllWindows()
        
        if self.PupilParam.saving_video:
            self.tk_recording_video()
        if self.PupilParam.pupil_tracking_flag:
            self.tk_recording_pupil()
                
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
        #calls and exicutes our tracking alg
        PupilTrackingAlg(frame, self.PupilParam, self.SYSPARAMS, self.video_frame.pack(), self.ax) # Process the frame for pupil tracking
        
        print(self.PupilParam.x1, self.PupilParam.x2, self.PupilParam.y1, self.PupilParam.y2)
        # Save the frame to video if recording
        #once less than just call tk_record
        if self.PupilParam.pupil_tracking_flag:
            block_fps = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.PupilParam.pupil_tracking_Data.append([self.PupilParam.x1, self.PupilParam.x2, 
                                                   self.PupilParam.y1, self.PupilParam.y2, block_fps])
            
        if self.PupilParam.saving_video and self.PupilParam.frame_count < self.PupilParam.MAX_NUM_OF_SAVABLE_FRAMES:
            current_time = datetime.now()
            time_difference = current_time - self.PupilParam.start_save_time
            
            if time_difference.total_seconds() > self.PupilParam.saving_frequency:
                self.video_writer.write(frame)
                self.PupilParam.frame_count += 1
                self.PupilParam.start_save_time = current_time
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
            # light tracking box
            width = abs(self.PupilParam.x2 - self.PupilParam.x1)
            height = abs(self.PupilParam.y2 - self.PupilParam.y1)
            size = max(width, height) # might want to replace with size
            track_rect = patches.Rectangle((self.PupilParam.x1, self.PupilParam.y1), width, height, linewidth=1, edgecolor='r', fill=False)
           
            if self.PupilParam.show_reference:
                self.ax.plot([self.PupilParam.x1 + width/2, self.PupilParam.ref_center_x], [self.PupilParam.y1 +height/2, self.PupilParam.ref_center_y])
            else:
                self.ax.plot([self.PupilParam.x1 + width/2, self.PupilParam.frame_width/2], [self.PupilParam.y1 +height/2, self.PupilParam.frame_height/2])
            self.ax.plot([self.PupilParam.x1, self.PupilParam.x2], [self.PupilParam.y1, self.PupilParam.y2])
            
            self.ax.add_patch(track_rect)
        
            
        if self.PupilParam.show_reference:
            width = self.PupilParam.ref_x2 - self.PupilParam.ref_x1  # Width of the rectangle
            height = self.PupilParam.ref_y2 - self.PupilParam.ref_y1  # Height of the rectangle
            # Create a Rectangle patch
            ref_rect = patches.Rectangle((self.PupilParam.ref_x1, self.PupilParam.ref_y1), width, height, linewidth=1,edgecolor='b', fill=False)
            self.ax.add_patch(ref_rect)
            
        if self.PupilParam.BEflag:
            H1 = int(round(self.PupilParam.frame_height / 2))
            V1 = int(round(self.PupilParam.frame_width / 2))
            Dmm = int(1 * self.PupilParam.pixel_calibration)
            
            # Update or create plot r1
            self.PupilParam.r1, =  self.ax.plot(range(self.PupilParam.frame_height), [V1] * self.PupilParam.frame_height, linewidth=1, color='red')

            # Update or create plot r2
            x_values_r2 = [x for x in range(H1 - Dmm, -1, -Dmm)] + [x for x in range(H1 + Dmm, self.PupilParam.frame_height, Dmm)]
            self.PupilParam.r2, =  self.ax.plot(x_values_r2, [V1] * len(x_values_r2), '+', linewidth=1, color='red')

            # Update or create plot r3
            self.PupilParam.r3, =  self.ax.plot([H1] * self.PupilParam.frame_width, range(self.PupilParam.frame_width), linewidth=1, color='red')

            # Update or create plot r4
            y_values_r4 = [y for y in range(V1 - Dmm, -1, -Dmm)] + [y for y in range(V1 + Dmm, self.PupilParam.frame_width, Dmm)]
            self.PupilParam.r4, =  self.ax.plot([H1] * len(y_values_r4), y_values_r4, '+', linewidth=2, color='red')
            
            
        
        self.ax.imshow(frame_rgb, aspect='auto')
        #TODO plot other aspects:
        self.video_canvas.draw()
        self.video_canvas.get_tk_widget().pack()
        self.video_frame.pack()
    
    def tk_set_reference(self): #DONE
        """Button 3: sets reference
        Get mouse coordinates then set reference to it"""
        self.video_canvas.get_tk_widget().config(cursor='cross')
        self.cid = self.video_canvas.mpl_connect('button_press_event', self.tk_set_reference_click)
        
    def tk_set_reference_click(self, event):
        print(f'You clicked at coordinates: ({event.xdata}, {event.ydata})')
        x = event.xdata
        y = event.ydata
        
        self.PupilParam.ref_center_x = x
        self.PupilParam.ref_center_y = y
        
        self.PupilParam.ref_x1 = round(x)-30
        self.PupilParam.ref_x2 = round(x)+30
        self.PupilParam.ref_y1 = round(y)-30
        self.PupilParam.ref_y2 = round(y)+30
        
        # TODO: Save reference coordinates like matlab file
        # np.savez('./VideoAndRef/RefPupil_' + date_string, Refx1=ref_x1, Refx2=ref_x2, Refy1=ref_y1, Refy2=ref_y2)
    
        self.video_canvas.get_tk_widget().config(cursor='')
        self.video_canvas.mpl_disconnect(self.cid)
        self.tk_reference_button.configure(text="Unset Reference", command=self.tk_unset_reference)
        self.PupilParam.show_reference = True
        

    def tk_load_reference(self):
        """ Button 4: loads then sets reference from a RefPupil_ file
            after, set reference button should now be unset reference
        """
        self.tk_root.withdraw()
        file_name = tk.filedialog.askopenfilename(title='Select RefPupil file', initialdir=os.getcwd())
        self.tk_root.deiconify()
        if file_name:
            path, file = os.path.split(file_name)
            if file.startswith('RefPupil_'):
                reference_data = sio.loadmat(file_name)
                self.PupilParam.ref_x1 = reference_data['Refx1'][0][0]
                self.PupilParam.ref_x2 = reference_data['Refx2'][0][0]
                self.PupilParam.ref_y1 = reference_data['Refy1'][0][0]
                self.PupilParam.ref_y2 = reference_data['Refy2'][0][0]
                self.tk_reference_button.configure(text="Unset Reference", command=self.tk_unset_reference)
                self.PupilParam.show_reference = True
            else:
                print("Invalid file name. File must start with 'RefPupil_'")

    def tk_unset_reference(self):
        """unsets reference
            should only appear as a button option after setting or loading reference"""
        self.PupilParam.reset_ref_x1()
        self.PupilParam.reset_ref_x2()
        self.PupilParam.reset_ref_y1()
        self.PupilParam.reset_ref_y2()
        ##TODO: make sure box is de-initilized
        self.tk_reference_button.configure(text="Set Reference", command=self.tk_set_reference)
        self.PupilParam.show_reference = False
        return
    
# BE triggering button
    def tk_draw_be(self):
        """Button 7: draws BE"""
        self.PupilParam.BEflag = True
        self.tk_draw_be_button.configure(text='Hide BE', command=self.tk_hide_be)

    def tk_hide_be(self):
        """hides BE"""
        self.PupilParam.BEflag = False
        self.tk_draw_be_button.configure(text='Draw BE',  command=self.tk_draw_be)

    def tk_sync_save(self):
        """Button 9: sync save
        initializes the next trigger """
        if self.PupilParam.video:
            self.PupilParam.sync = True
            self.PupilParam.DataSync = []
            self.tk_automatic_button.configure(text="Wait for Sync", command=self.tk_sync_wait)

    def tk_sync_wait(self):
        """sync wait"""
        self.PupilParam.sync = False
        if self.PupilParam.DataSync.size:
            file_name = "Trial_DataPupil_"
            self.save_pupil_data(file_name, self.PupilParam.DataSync)
            self.PupilParam.DataSync = []
            
        self.tk_automatic_button.configure(text="Sync Save", command=self.tk_sync_save)

    def tk_save_video(self):
        """Button 5: save video"""
        if not self.PupilParam.video:
            return 
        self.PupilParam.saving_video = True
        
        prefix = self.tk_type_pupil_file_name_prefix_entry.get()
        self.PupilParam.frame_count = 1
        self.PupilParam.start_save_time = datetime.now()
        self.video_writer = cv2.VideoWriter('temp_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, tuple(self.PupilParam.vidRes))
        self.tk_save_video_button.configure(text="Recording Video ...",command = self.tk_recording_video)
            
        if not self.PupilParam.pupil_tracking_flag:
            self.tk_save_pupil_tracking()
            
    def tk_recording_video(self):
        """Button 5: save video"""
        if self.PupilParam.video:
            self.PupilParam.saving_video = False
            # Prefix = input('Enter Prefix: ')  # Get prefix from user
            self.video_writer.release()
            # final_name = Prefix + "_video.avi"
            # os.rename('temp_video.avi', final_name)
            if self.PupilParam.pupil_tracking_flag:
                self.tk_recording_pupil()
            self.tk_save_video_button.configure(text='Save Video', command = self.tk_save_video)
    
    def tk_save_pupil_tracking(self):
        """ Button 8: values collected nothing functally needed """
        if not self.PupilParam.video:
            return 
     
        self.PupilParam.pupil_tracking_flag = True
        self.PupilParam.pupil_tracking_TO = datetime.now()
        block_fps = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.PupilParam.pupil_tracking_Data = [[0, 0, 0, 0, block_fps]]
        self.PupilParam.pupil_tracking_Data = [[0, 0, 0, 0, block_fps]]
            
        self.tk_save_pupil_tracking_button.configure(text='Recording Pupil ...', command=self.tk_recording_pupil)
        
       
    def tk_recording_pupil(self):
        """Pairwise on button 8"""
        if self.PupilParam.video:
            self.PupilParam.pupil_tracking_flag = False
            self.save_pupil_data("DataPupil_", self.PupilParam.pupil_tracking_Data)
            # self.pupilData.pixel_calibration = self.PupilParam.pixel_calibration # confusion but was in matlab code
            self.PupilParam.pupil_tracking_Data = []
            self.tk_save_pupil_tracking_button.configure(text='Save Pupil Tracking',  command=self.tk_save_pupil_tracking)
            
    def tk_secs(self):
        """ with new value entry the savable frames/freq changes"""
        secs = int(self.tk_secs_entry.get())
        fps = int(self.tk_fps_entry.get())
        self.PupilParam.MAX_NUM_OF_SAVABLE_FRAMES = secs*fps
        self.PupilParam.saving_frequency = 1/fps

    def tk_FPS(self):
        """ with new value entry the savable frames/freq changes"""
        secs = int(self.tk_secs_entry.get())
        fps = int(self.tk_fps_entry.get())
        self.PupilParam.MAX_NUM_OF_SAVABLE_FRAMES = secs*fps
        self.PupilParam.saving_frequency = 1/fps

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
        """Button 11: used for saving settings"""
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
        self.PupilParam.enable_TCA_comp()
        self.PupilParam.totaloffx = []
        self.PupilParam.totaloffy = []
        
        # Update button properties to indicate TCA correction is enabled
        self.tk_focus_button.configure(text="Disable TCA Correction",
                                       command=self.tk_disable_tca_correction)
        

    def tk_disable_tca_correction(self):
        """Button 14: """
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
                #MATLABAomControl32(aligncommand) 
            else:
                """ TODO: Call to netcomm goes here; the exact Python equivalent is unknown"""
                #netcomm_write(SYSPARAMS['netcommobj'], aligncommand.encode())  # Replace with actual Python function
            
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

    def tk_gain_change(self, val):
        """Slider 6: slider moved"""
        self.CameraSettings.set_gain(val)
        if self.PupilParam.video:
            self.camera.set(cv2.CAP_PROP_GAIN, val)
            print(val)

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
        
    def set_PupilTracker(self, value):
        self.PupilTracker = value
        

    def save_pupil_data(self, file_name, pupil_data):
        """
        Save pupil data to a file.
        """
        prefix = self.tk_type_pupil_file_name_prefix_entry.get()
        
        date_string = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        date_string = date_string.replace(' ', '_').replace(':', '_')
        save_file_name = f'.\\VideoAndRef\\{prefix}]{file_name}{date_string}.csv'

        with open(save_file_name, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(pupil_data)

    def save_pupil_video(prefix, video_to_save):
        """
        Save pupil video to a file.
        """
        date_string = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        date_string = date_string.replace(' ', '_').replace(':', '_')
        save_file_name = f'.\\VideoAndRef\\{prefix}VideoPupil_{date_string}.avi'

        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(save_file_name, fourcc, 30.0, (640, 480))

        for frame in video_to_save:
            out.write(frame)

        out.release()

        
    def main_loop(self):
        "main loop functioning for intitlization"
        self.tk_root.mainloop()

""" initializes and runs entirety of code"""
if __name__ == "__main__":
    tg = ProjectorGUI()
    tg.main_loop()
