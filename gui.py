import numpy as np

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import os
from PupilParam import *
from CameraSettings import *
from tkinter import simpledialog
import sys
import datetime
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np

global SYSPARAMS
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
        self.tk_root.geometry('900x600')
        self.tk_root.title('PupilVideoTrackingV2')
        self.type_pupil_file_name_prefix = ""
        self.PupilParam = PupilParam()
        self.PupilTracker = None

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
        make_middle_frame(middle_frame)

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
        self.tk_type_pupil_file_name_prefix_entry.pack(side="bottom",expand=True,fill='both')

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
        video_camera_frame_top.pack(side="top", fill='x')
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
        video_camera_frame_left = tk.Frame(video_camera_frame)
        video_camera_frame_left.pack(side="left", expand=True, fill='both')
        video_camera_frame_right = tk.Frame(video_camera_frame)
        video_camera_frame_right.pack(side="left", expand=True, fill='both')
        # sliders
        self.tk_brightness_label = tk.Label(video_camera_frame_left, text="Brightness:")
        self.tk_brightness_label.pack(expand=True, fill='both')
        self.tk_brightness_slider = tk.Scale(video_camera_frame_right, from_=0, to=4095, tickinterval=0.1, orient='horizontal')
        self.tk_brightness_slider.set(240)
        self.tk_brightness_slider.pack(expand=True, fill='both')

        self.tk_gamma_label = tk.Label(video_camera_frame_left, text="Gamma:")
        self.tk_gamma_label.pack(expand=True, fill='both')
        self.tk_gamma_slider = tk.Scale(video_camera_frame_right, from_=0, to=5, tickinterval=0.1, orient='horizontal')
        self.tk_gamma_slider.set(1)
        self.tk_gamma_slider.pack(expand=True, fill='both')

        self.tk_exposure_label = tk.Label(video_camera_frame_left, text="Exposure:")
        self.tk_exposure_label.pack(expand=True, fill='both')
        self.tk_exposure_slider = tk.Scale(video_camera_frame_right, from_=0, to=4, tickinterval=0.0005, orient='horizontal')
        self.tk_exposure_slider.set(0.0333)
        self.tk_exposure_slider.pack(expand=True, fill='both')

        self.tk_gain_label = tk.Label(video_camera_frame_left, text="Gain:")
        self.tk_gain_label.pack(expand=True, fill='both')
        self.tk_gain_slider = tk.Scale(video_camera_frame_right, from_=0, to=48, tickinterval=0.1, orient='horizontal')
        self.tk_gain_slider.set(0)
        self.tk_gain_slider.pack(expand=True, fill='both')

        # button
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


    def make_middle_frame(self, middle_frame):
        # open video source (by default this will try to open the computer webcam)
        # TODO: set up video frame and graph over lay
        """""""[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]"""
        axis = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

        x = y = np.array(axis)

        fig = Figure(figsize=(6, 6))
        pupil_fig = fig.add_subplot(111)

        pupil_fig.plot(x,y)

        canvas = FigureCanvasTkAgg(fig, master=middle_frame)
        canvas.get_tk_widget().pack()
        canvas.draw()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
        return

    ###top buttons###

    """ quits and exits program (button 1)
    if dataScn"""
    def tk_quit(self):
        self.set_PupilTracker(0);
        date_string = time.strftime('%Y-%m-%d_%H-%M-%S')

        if self.PupilParam.get_DataSync() is not None:
            pupil_data = self.PupilParam.get_DataSync()
            file = open(f'./VideoAndRef/Trial_DataPupil_{self.get_type_pupil_file_name_prefix()}_{date_string}')
            file.write(pupil_data)
            file.close()
        self.tk_root.destroy()

    """ starts video"""
    def tk_start_video(self):
        # TODO: alex help layer graph with video import in matlab library for this https://www.mathworks.com/matlabcentral/fileexchange/68852-code-examples-from-video-processing-in-matlab
        """ also layer with existing graph so we can plot on video """






        return
    """Stops video"""

    """sets refernce"""
    def tk_set_reference(self):

        """Get mouse coordinates then set reference to it"""
        def set_reference_helper(event):
            x, y = event.x, event.y
            reference_x1 = round(x)-30
            reference_x2 = round(x)+30
            reference_y1 = round(y)-30
            reference_y2 = round(y)-30
            
            self.PupilParam.set_x1(reference_x1)
            self.PupilParam.set_x2(reference_x2)
            self.PupilParam.set_y1(reference_y1)
            self.PupilParam.set_y2(reference_y2)
            # TODO: Save reference coordinates like matlab file

            self.tk_reference_button.configure(text="Unset Reference", command=self.tk_unset_reference())
        
        return


    def tk_load_reference(self):
        """loads then sets reference from a RefPupil_ file
            after, set reference button should now be unset reference
        """
        self.tk_root.withdraw()

        file_name = tk.filedialog.askopenfilename(title='Select RefPupil file', initialdir=os.getcwd())

        if file_name:

            path, file = os.path.split(file_name)
            if file.startswith('RefPupil_'):
                reference_data = sio.loadmat(file_name)
                reference_x1 = reference_data['Refx1'][0][0]
                reference_x2 = reference_data['Refx2'][0][0]
                reference_y1 = reference_data['Refy1'][0][0]
                reference_y2 = reference_data['Refy2'][0][0]

                self.PupilParam.set_x1(reference_x1)
                self.PupilParam.set_x2(reference_x2)
                self.PupilParam.set_y1(reference_y1)
                self.PupilParam.set_y2(reference_y2)

                self.tk_reference_button.configure(text="Unset Reference", command=self.tk_unset_reference())
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
        ##TODO: make sure box is de initilized
        self.tk_reference_button.configure(text="Set Reference", command=self.tk_set_reference)
        return

    def tk_disable_tracking(self):
        """disables tracking"""
        self.pupil_param.disable_tracking()
        self.tk_tracking_button.configure(text="Enable Tracking", command=self.tk_enable_tracking)
        return

    def tk_enable_tracking(self):
        """enables tracking"""
        self.pupil_param.enable_tracking()
        self.tk_tracking_button.configure(text="Disable Tracking", command=self.tk_disable_tracking)
        return

    """zooms in"""
    def tk_zoom_in(self):
        return

    """draws BE"""
    def tk_draw_be(self):
        if self.PupilParam.get_BEFlag() == 0:
            self.PupilParam.set_BEFlag(1)
            #TODO: set(hObject,'String','Hide BE')
            self.tk_draw_be_button.config(text = 'Hide BE')
            self.tk_draw_be_button.pack()
        else:
            self.PupilParam.set_BEFlag(0)
            # TODO: set(hObject,'String','Draw BE')
            self.tk_draw_be_button.config(text='Draw BE')
            self.tk_draw_be_button.pack()
        return

    def tk_sync_save(self):
        """sync save"""
        if (self.PupilParam.get_Video()):
            self.tk_sync_wait()
            return
        self.PupilParam.save_sync()
        self.tk_automatic_button.configure(text="Wait for Sync", command=self.tk_sync_wait)
        if len(self.PupilParam.get_DataSync()):
            date_string = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            #TODO: Prefix = get(handles.edit3, 'String')
            prefix = " "
            pupil_data = self.PupilParam.get_DataSync()
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
        """save video"""
        if self.PupilParam.get_Video() == 1 and self.PupilParam.set_SavingVideo() == 0:
            self.PupilParam.set_SavingVideo(1)
        return

    def tk_secs(self):
        """ with new value entry the savable frames/freq changes"""
        secs = self.tk_secs_entry.get()
        fps = self.tk_fps_entry.get()
        self.PupilParam.set_MAX_NUM_OF_SAVABLE_FRAMES(secs*fps)
        self.PupilParam.set_saving_frequency(1/fps)
        return

    def tk_FPS(self):
        """ with new value entry the savable frames/freq changes"""
        secs = self.tk_secs_entry.get()
        fps = self.tk_fps_entry.get()
        self.PupilParam.set_MAX_NUM_OF_SAVABLE_FRAMES(secs * fps)
        self.PupilParam.set_saving_frequency(1/fps)
        return

    def tk_save_pupil_tracking(self):
        """ values collected nothing functally needed """
        return

    def tk_type_pupil_file_name_prefix(self):
        """ """
        return

    """"""
    def get_type_pupil_file_name_prefix(self):
        return self.type_pupil_file_name_prefix

    def tk_auto(self):
        """ makes controls of video settings automatic """
        self.CameraSettings.auto_exposure_mode()
        self.tk_automatic_button.configure(text="Manual", command=self.tk_manual)
        #TODO: condition if video is running
        return

    def tk_manual(self):
        """ makes controls of video settings manual """
        self.CameraSettings.manual_exposure_mode()
        self.tk_automatic_button.configure(text="Auto", command=self.tk_auto)
        # TODO: condition if video is running
        return

    def tk_reset(self):
        """ resets camera values to starting values"""
        CameraSettings.reset_brightness()
        CameraSettings.reset_iris()
        CameraSettings.reset_exposure()
        CameraSettings.reset_exposure_mode() # sets to manual exposure
        CameraSettings.get_gain()

        #TODO: make it so it will work when video is running
        return

    """ """
    def tk_save_settings(self):
        return

    """ """
    def tk_load_settings(self):
        return


    def tk_enable_tca_correction(self):
        """ """
        original_color = [0.941176, 0.941176, 0.941176]
        self.PupilParam.enable_TCA_comp()
        self.PupilParam.totaloffx

        self.tk_focus_button.configure(text="Disable TCA Correction", command=self.tk_disable_tca_correction)
        return

    def tk_disable_tca_correction(self):
        """ """
        original_color = [0.941176, 0.941176, 0.941176]
        self.PupilParam.disable_TCA_comp()
        # PupilParam.totaloffx = []
        # PupilParam.totaloffy = []
        self.tk_focus_button.configure(text="Enable TCA Correction", command=self.tk_enable_tca_correction)


    def tk_tollernc_mm(self):
        """ """
        return

    def tk_TCA_XY_arcmin_mm(self):
        """ """
        return


    def tk_show_focus(self):
        """ shows focus """
        self.PupilParam.show_focus()
        self.tk_focus_button.configure(text="Hide Focus", command=self.tk_hide_focus)
        return


    def tk_hide_focus(self):
        """ hides focus """
        self.PupilParam.hide_focus()
        self.tk_focus_button.configure(text="Show Focus", command=self.tk_show_focus)
        return

    ######## sliders ###########

    def tk_brightness_change(self):
        """brightness slider moved"""
        self.CameraSettings.set_brightness(self.tk_brightness_slider)
        # TODO: if video in progress auto update value
        return

    def tk_gamma_change(self):
        """slider moved"""
        self.CameraSettings.set_gamma(self.tk_gamma_slider)
        # TODO: if video in progress auto update value
        return

    def tk_exposure_change(self):
        """slider moved"""
        self.CameraSettings.set_exposure(self.tk_exposure_slider)
        # TODO: if video in progress auto update value
        return

    def tk_gain_change(self):
        """slider moved"""
        self.CameraSettings.set_gain(self.tk_gain_slider)
        # TODO: if video in progress auto update value
        return






    "main loop functioning for intitlization"
    def main_loop(self):
        self.tk_root.mainloop()


# Getter and Setter methods for PupilTracker
    def get_PupilTracker(self):
        return self.PupilTracker

    def set_PupilTracker(self, value):
        self.PupilTracker = value

""" initializes and runs entirety of code"""
if __name__ == "__main__":
    tg = ProjectorGUI()
    tg.main_loop()
