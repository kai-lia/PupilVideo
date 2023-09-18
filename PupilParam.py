import time
import matplotlib.pyplot as plt

class PupilParam:
    def __init__(self):
        self.x1 = -1
        self.x2 = -1
        self.y1 = -1
        self.y2 = -1

        self.track_error = -1
        self.totaloffx = []
        self.totaloffy = []
        self.graylevel = 255
        self.Re = -1000
        self.Th = -1

        self.Flag = False
        self.BEFlag = False
        self.PTFlag = False
        self.PTData = None

        # video state
        self.video = False # if video is on
        self.saving_video = False # if video is saving

        self.MAX_NUM_OF_SAVABLE_FRAMES = 5
        self.saving_frequency = 0.3
        self.FrameCount = self.MAX_NUM_OF_SAVABLE_FRAMES
        self.Sync = False

        self.show_reference = False
        self.tracking = True
        self.reftime = None # Note: 'clock' function in Python returns the CPU time, not the wall time like in MATLAB
        self.idx_reftime = 11
        self.camera_fps = 0
        self.fps = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.vidRes = []
        self.focus = False # note means focus is shown
        self.TCA_comp = False
        self.Ltotaloffx = 1
        self.DataSync = None
        self.lap = None
        
        #coreslates for Calibration Settings
        self.pixel_calibration = 49.5517721152208 
        self.TCAmmX = None
        self.TCAmmY = None
        self.tolerated_pupil_dist = None

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
    def reset_x1(self):
        self.x1 = -1

    def reset_x2(self):
        self.x2 = -1
        
    def reset_y1(self):
        self.y1 = -1
        
    def reset_y2(self):
        self.y2 = -1

# trackerror
    def reset_track_error(self):
        self.track_error = -1

    # DataSync
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
        
    def get_tracking(self):
        return self.tracking

    # showing and hiding focus
    def show_focus(self):
        self.focus = True

    def hide_focus(self):
        self.focus = False
       
    # enable and disable for TCA computation
    def disable_TCA_comp(self):
        self.TCA_comp = False

    def enable_TCA_comp(self):
        self.TCA_comp = True

# ### PTT stuff ### #
    # PTData
    def reset_PTData(self):
        self.PTData = []
        
    """Reset_vectors:
        used when opening new video instance or zooming in
        resets vector so tracking accuracy preserved """
    def reset_vectors(self):
        plot_obj = plt.plot([1], [1])[0]
        # l value
        self.l3 = plot_obj
        self.l4 = plot_obj
        self.l5 = plot_obj
        self.l6 = plot_obj
        self.l7 = plot_obj
        self.l8 = plot_obj
        # p value
        self.p1 = plot_obj
        # v values
        self.v1 = plot_obj
        self.v2 = plot_obj
        self.v3 = plot_obj
        # c values
        self.c1 = plot_obj
        self.c2 = plot_obj
        self.c3 = plot_obj
        self.c4 = plot_obj
        # r values
        self.r1 = plot_obj
        self.r2 = plot_obj
        self.r3 = plot_obj
        self.r4 = plot_obj

