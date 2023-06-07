import time
import matplotlib.pyplot as plt

class PupilParam:
    def __init__(self):
        self.x1 = -1
        self.x2 = -1
        self.y1 = -1
        self.y2 = -1

        self.TrackError = -1
        self.totaloffx = []
        self.totaloffy = []
        self.graylevel = 255
        self.Re = -1000
        self.Th = -1

        self.Flag = False
        self.BEFlag = False
        self.PTFlag = False
        self.PTTO = False
        self.PTData = None

        # video state
        self.video = False # if video is on
        self.savingvideo = False # if video is saving

        self.MAX_NUM_OF_SAVABLE_FRAMES = 5
        self.saving_frequency = 0.3
        self.FrameCount = self.MAX_NUM_OF_SAVABLE_FRAMES
        self.Sync = False

        self.show_reference = False
        self.tracking = True
        self.reftime = time.process_time() # Note: 'clock' function in Python returns the CPU time, not the wall time like in MATLAB
        self.idx_reftime = 11
        self.fps = [0] * 10
        self.vidRes = 1024
        self.focus = False # note means focus is shown
        self.TCA_comp = False
        self.Ltotaloffx = 1
        self.DataSync = None

        # l plots: doing (None,)*int to multi declare without dependencies
        self.l3, self.l4, self.l5, self.l6, self.l7, self.l8 = (None,)*6
        # p plot
        self.p1 = None
        # v plots
        self.v1, self.v2, self.v3, self.v4 = (None,)*4
        # c plots
        self.c1, self.c2, self.c3, self.c4, self.c5 = (None,)*5
        # r plots
        self.r1, self.r2, self.r3, self.r4 = (None,)*4

# x1, x2, y1, y2 Features for tracking
    # Getter and Setter methods for x1
    def get_x1(self):
        return self.x1

    def set_x1(self, value):
        self.x1 = value

    def reset_x1(self):
        self.x1 = -1

    # Getter and Setter methods for x2
    def get_x2(self):
        return self.x2

    def set_x2(self, x2):
        self.x2 = x2

    def reset_x2(self):
        self.x2 = -1

    # Getter and Setter methods for y1
    def get_y1(self):
        return self.y1

    def set_y1(self, y1):
        self.y1 = y1

    def reset_y1(self):
        self.y1 = -1

    # Getter and Setter methods for y2
    def get_y2(self):
        return self.y2

    def set_y2(self, y2):
        self.y2 = y2

    def reset_y2(self):
        self.y2 = -1

    # Getter and Setter for Track Error
    def get_TrackError(self):
        return self.TrackError

    def set_TrackError(self, TrackError):
        self.TrackError = TrackError

    def reset_TrackError(self):
        self.TrackError = -10

    # Getter and Setter methods for graylevel
    def get_gray_level(self):
        return self._graylevel

    def set_gray_level(self, gray_leve):
        self._graylevel = gray_leve

    # Getter and Setter methods for Re
    def get_Re(self):
        return self.Re

    def set_Re(self, Re):
        self.Re = Re

    # Getter and Setter methods for Th
    def get_Th(self):
        return self.Th

    def set_Th(self, Th):
        self.Th = Th

    # Getter and Setter methods for Flag
    def get_Flag(self):
        return self.Flag

    def set_Flag(self, Flag):
        self.Flag = Flag

    # Getter and Setter methods for BEFlag
    def get_BEFlag(self):
        return self.BEFlag

    def set_BEFlag(self, BEFlag):
        self.BEFlag = BEFlag

    # Getter and Setter methods for PTFlag
    def get_PTFlag(self):
        return self.PTFlag

    def set_PTFlag(self, PTFlag):
        self.PTFlag = PTFlag

# Video Related Features
    # Getter and Setter methods for Video
    def get_video(self):
        return self.video

    def set_video(self, video):
        self.video = video

    # Getter and Setter methods for saving video
    def get_saving_video(self):
        return self.saving_video

    def set_saving_video(self, saving_video):
        self.saving_video = saving_video

    # Getter and Setter methods for MAX_NUM_OF_SAVABLE_FRAMES
    def get_MAX_NUM_OF_SAVABLE_FRAMES(self):
        return self.MAX_NUM_OF_SAVABLE_FRAMES

    def set_MAX_NUM_OF_SAVABLE_FRAMES(self, MAX_NUM_OF_SAVABLE_FRAMES):
        self.MAX_NUM_OF_SAVABLE_FRAMES = MAX_NUM_OF_SAVABLE_FRAMES

    # Getter and Setter methods for DataSync
    def get_DataSync(self):
        return self.DataSync

    def set_DataSync(self, DataSync):
        self.DataSync = DataSync

    def reset_DataSync(self):
        self.DataSync = None

    #sync ops for "Save Sync button"
    def save_sync(self):
        self.tracking = False

    def wait_sync(self):
        self.tracking = True

    # enable and disable for tracking
    def disable_tracking(self):
        self.tracking = False

    def enable_tracking(self):
        self.tracking = True

    # showing and hiding focus
    def show_focus(self):
        self.focus = True

    def hide_focus(self):
        self.focus = False

    # enable and disable for TCA computation
    def get_TCA_comp(self):
        return self.TCA_comp

    def disable_TCA_comp(self):
        self.TCA_comp = False

    def enable_TCA_comp(self):
        self.TCA_comp = True

    # getter and setter for Frame Count
    def get_FrameCount(self):
        return self.FrameCount

    def set_FrameCount(self, FrameCount):
        self.FrameCount = FrameCount

    # getter setter saving frequency
    def get_saving_frequency(self):
        return self.saving_frequency

    def set_saving_frequency(self, saving_frequency):
        self.saving_frequency = saving_frequency

# ### PTT stuff ### #
    # getter setter PTTO
    def get_PTTO(self):
        return self.PTTO

    def set_PTTO(self, PTTO):
        self.PTTO = PTTO

    # getter setter PTD
    def get_PTData(self):
        return self.PTData

    def set_PTData(self, PTData):
        self.PTData = PTData

# ### Getter and Setters for Vectors ### #
    # l3 property
    def get_l3(self):
        return self.l3

    def set_l3(self, l3):
        self.l3 = l3

    # l4 property
    def get_l4(self):
        return self.l4

    def set_l4(self, l4):
        self.l4 = l4

    # l5 property
    def get_l5(self):
        return self.l5

    def set_l5(self, l5):
        self.l5 = l5

    # l6 property
    def get_l6(self):
        return self.l6

    def set_l6(self, l6):
        self.l6 = l6

    # l7 property
    def get_l7(self):
        return self.l7

    def set_l7(self, l7):
        self.l7 = l7

    # l8 property
    def get_l8(self):
        return self.l8

    def set_l8(self, l8):
        self.l8 = l8

    # p1 property
    def get_p1(self):
        return self.p1

    def set_p1(self, p1):
        self.p1 = p1

    # v1 property
    def get_v1(self):
        return self.v1

    def set_v1(self, v1):
        self.v1 = v1

    # v2 property
    def get_v2(self):
        return self.v2

    def set_v2(self, v2):
        self.v2 = v2

    # v3 property
    def get_v3(self):
        return self.v3

    def set_v3(self, v3):
        self.v3 = v3

    # c vectors
    # c1 property
    def get_c1(self):
        return self.c1

    def set_c1(self, c1):
        self.c1 = c1

    # c2 property
    def get_c2(self):
        return self.c2

    def set_c2(self, c2):
        self.c2 = c2

    # c3 property
    def get_c3(self):
        return self.c3

    def set_c3(self, c3):
        self.c3 = c3

    # c4 property
    def get_c4(self):
        return self.c4

    def set_c4(self, c4):
        self.c4 = c4

    # c5 property
    def get_c5(self):
        return self.c5

    def set_c5(self, c5):
        self.c5 = c5

# r values
    # r1 property
    def get_r1(self):
        return self.r1

    def set_r1(self, r1):
        self.r1 = r1

    # r2 property
    def get_r2(self):
        return self.r2

    def set_r2(self, r2):
        self.r2 = r2

    # r3 property
    def get_r3(self):
        return self.r3

    def set_r3(self, r3):
        self.r3 = r3

    # r4 property
    def get_r4(self):
        return self.r4

    def set_r4(self, r4):
        self.r4 = r4

    """Reset_vectors:
        used when opening new video instance or zooming in
        resets vector so tracking accuracy preserved """
    def reset_vectors(self):
        plot_obj = plt.plot([1], [1])[0]
        # l value
        self.set_l3(plot_obj)
        self.set_l4(plot_obj)
        self.set_l5(plot_obj)
        self.set_l6(plot_obj)
        self.set_l7(plot_obj)
        self.set_l8(plot_obj)
        # p value
        self.set_p1(plot_obj)
        # v values
        self.set_v1(plot_obj)
        self.set_v2(plot_obj)
        self.set_v3(plot_obj)
        # c values
        self.set_c1(plot_obj)
        self.set_c2(plot_obj)
        self.set_c3(plot_obj)
        self.set_c4(plot_obj)
        # r values
        self.set_r1(plot_obj)
        self.set_r2(plot_obj)
        self.set_r3(plot_obj)
        self.set_r4(plot_obj)

