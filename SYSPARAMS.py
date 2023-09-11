class SYSPARAMS:

    def __init__(self):
        self.board = None  # Attribute
        self.netcommobj = None  # Attribute
        self.pupil_camera_fps = None  # Variable
        self.pupil_diff_x = []  # Variable
        self.pupil_diff_y = []  # Variable
        self.pupil_duration = None  # Variable
        self.pupil_TCA_x = None  # Variable
        self.pupil_TCA_y = None # Variable
        self.pupil_tracker = None  # Variable
        self.pixel_per_deg = None  # Variable
        self.real_system = None  # Variable

    # You can define methods to access or update specific parameters if needed
    def set_board(self, value):
        self.board = value

    def get_board(self):
        return self.board

    # Repeat similar methods for other parameters as needed
