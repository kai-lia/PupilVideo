import time

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
        self.SAVING_FREQUENCY = 0.3
        self.FrameCount = self.MAX_NUM_OF_SAVABLE_FRAMES
        self.Sync = 0
        self.ShowReference = 0
        self.DisableTracking = 0
        self.reftime = time.process_time() # Note: 'clock' function in Python returns the CPU time, not the wall time like in MATLAB
        self.idx_reftime = 11
        self.fps = [0] * 10
        self.vidRes = 1024
        self.ShowFocus = 0
        self.EnableTCAComp = 0
        self.Ltotaloffx = 1
        self.DataSync = None

# Getter and Setter methods for x1
    def get_x1(self):
        return self._x1

    def set_x1(self, value):
        self._x1 = value

    # Getter and Setter methods for x2
    def get_x2(self):
        return self._x2

    def set_x2(self, value):
        self._x2 = value

    # Getter and Setter methods for y1
    def get_y1(self):
        return self._y1

    def set_y1(self, value):
        self._y1 = value

    # Getter and Setter methods for y2
    def get_y2(self):
        return self._y2

    def set_y2(self, value):
        self._y2 = value

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
        return self._Video

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