import time
import matplotlib.pyplot as plt

class PupilParam:
    def __init__(self):
        self.x1 = -1
        self.x2 = -1
        self.y1 = -1
        self.y2 = -1
        self.graylevel = 255
        self.Re = -1000
        self.Th = -1
        self.Flag = 0
        self.BEFlag = 0
        self.PTFlag = 0
        self.Video = 0
        self.SavingVideo = 0
        self.MAX_NUM_OF_SAVABLE_FRAMES = 5
        self.saving_frequency = 0.3
        self.FrameCount = self.MAX_NUM_OF_SAVABLE_FRAMES
        self.Sync = False
        self.ShowReference = 0
        self.tracking = True
        self.reftime = time.process_time() # Note: 'clock' function in Python returns the CPU time, not the wall time like in MATLAB
        self.idx_reftime = 11
        self.fps = [0] * 10
        self.vidRes = 1024
        self.focus = False # note means focus is shown
        self.EnableTCAComp = 0
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

    def set_x2(self, value):
        self.x2 = value

    def reset_x2(self):
        self.x2 = -1

    # Getter and Setter methods for y1
    def get_y1(self):
        return self.y1

    def set_y1(self, value):
        self.y1 = value

    def reset_y1(self):
        self.y1 = -1

    # Getter and Setter methods for y2
    def get_y2(self):
        return self.y2

    def set_y2(self, value):
        self.y2 = value

    def reset_y2(self):
        self.y2 = -1

    # Getter and Setter methods for graylevel
    def get_graylevel(self):
        return self._graylevel

    def set_graylevel(self, value):
        self._graylevel = value

    # Getter and Setter methods for Re
    def get_Re(self):
        return self._Re

    def set_Re(self, value):
        self._Re = value

    # Getter and Setter methods for Th
    def get_Th(self):
        return self._Th

    def set_Th(self, value):
        self._Th = value

    # Getter and Setter methods for Flag
    def get_Flag(self):
        return self.Flag

    def set_Flag(self, value):
        self.Flag = value

    # Getter and Setter methods for BEFlag
    def get_BEFlag(self):
        return self.BEFlag

    def set_BEFlag(self, value):
        self.BEFlag = value

    # Getter and Setter methods for PTFlag
    def get_PTFlag(self):
        return self.PTFlag

    def set_PTFlag(self, value):
        self.PTFlag = value


    # Getter and Setter methods for Video
    def get_Video(self):
        return self.Video

    def set_Video(self, value):
        self._Video = value

    # Getter and Setter methods for SavingVideo
    def get_SavingVideo(self):
        return self._SavingVideo

    def set_SavingVideo(self, value):
        self._SavingVideo = value

    # Getter and Setter methods for MAX_NUM_OF_SAVABLE_FRAMES
    def get_MAX_NUM_OF_SAVABLE_FRAMES(self):
        return self._MAX_NUM_OF_SAVABLE_FRAMES

    def set_MAX_NUM_OF_SAVABLE_FRAMES(self, value):
        self._MAX_NUM_OF_SAVABLE_FRAMES = value

    # Getter and Setter methods for DataSync
    def get_DataSync(self):
        return self.DataSync

    def set_DataSync(self, value):
        self.DataSync = value

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

    # enable and disable for tracking
    def show_focus(self):
        self.focus = True

    def hide_focus(self):
        self.focus = False



    # getter setter saving frequency
    def get_saving_frequency(self):
        return self.saving_frequency

    def set_saving_frequency(self, value):
        self.saving_frequency = value






















####Getter and setters for vectors##########

    # l3 property
    def get_l3(self):
        return self.l3

    def set_l3(self, plot_obj):
        self.l3 = plot_obj

    # l4 property
    def get_l4(self):
        return self.l3

    def set_l4(self, plot_obj):
        self.l3 = plot_obj

    # l5 property
    def get_l5(self):
        return self.l3

    def set_l5(self, plot_obj):
        self.l3 = plot_obj


    # l6 property
    def get_l6(self):
        return self.l6

    def set_l6(self, plot_obj):
        self.l6 = plot_obj

    # l7 property
    def get_l7(self):
        return self.l7

    def set_l7(self, plot_obj):
        self.l7 = plot_obj

    # l8 property
    def get_l8(self):
        return self.l8

    def set_l8(self, plot_obj):
        self.l8 = plot_obj

    # p1 property
    def get_p1(self):
        return self.p1

    def set_p1(self, plot_obj):
        self.p1 = plot_obj

    # v1 property
    def get_v1(self):
        return self.v1

    def set_v1(self, plot_obj):
        self.v1 = plot_obj

    # v2 property
    def get_v2(self):
        return self.v2

    def set_v2(self, plot_obj):
        self.v2 = plot_obj

    # v3 property
    def get_v3(self):
        return self.v3

    def set_v3(self, plot_obj):
        self.v3 = plot_obj

    # c vectors

    # c1 property
    def get_c1(self):
        return self.c1

    def set_c1(self, plot_obj):
        self.c1 = plot_obj

    # c2 property
    def get_c2(self):
        return self.c2

    def set_c2(self, plot_obj):
        self.c2 = plot_obj

    # c3 property
    def get_c3(self):
        return self.c3

    def set_c3(self, plot_obj):
        self.c3 = plot_obj

    # c4 property
    def get_c4(self):
        return self.c4

    def set_c4(self, plot_obj):
        self.c4 = plot_obj

    # c5 property
    def get_c5(self):
        return self.c5

    def set_c5(self, plot_obj):
        self.c5 = plot_obj


    # r1 property
    def get_r1(self):
        return self.r1

    def set_r1(self, plot_obj):
        self.r1 = plot_obj

    # r2 property
    def get_r2(self):
        return self.r2

    def set_r2(self, plot_obj):
        self.r2 = plot_obj

    # r3 property
    def get_r3(self):
        return self.r3

    def set_r3(self, plot_obj):
        self.r3 = plot_obj

    # r4 property
    def get_r4(self):
        return self.r4

    def set_r4(self, plot_obj):
        self.r4 = plot_obj

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

