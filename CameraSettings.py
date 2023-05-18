class CameraSettings:
    def __init__(self):
        self.brightness = 240
        self.iris = 1
        self.exposure = 0.0333
        self.exposure_mode = True
        self.gain = 0
        self.video_format = 'RGB24 (1216x1024) [Skipping 2x]'
        self.roi = [0, 0, 1216, 1024]

    # Getter and Setter methods for brightness
    def get_brightness(self):
        return self.brightness

    def set_brightness(self, brightness):
        self.brightness = brightness

    def reset_brightness(self):
        self.brightness = 240

    # Getter and Setter methods for gamma
    def get_gamma(self):
        return self.gamma

    def set_gamma(self, gamma):
        self.gamma = gamma

    def reset_gamma(self):
        self.gamma = 1

    # Getter and Setter methods for iris
    def get_iris(self):
        return self.iris

    def set_iris(self, iris):
        self.iris = iris

    def reset_iris(self):
        self.iris = 1

    # Getter and Setter methods for exposure
    def get_exposure(self):
        return self._exposure

    def set_exposure(self, exposure):
        self.exposure = exposure

    def reset_exposure(self):
        self.exposure = 0.0333

    # Getter and Setter methods for exposure_mode
    def get_exposure_mode(self):
        return self.exposure_mode

    def set_exposure_mode(self, exposure_mode):
        self.exposure_mode = exposure_mode

    def auto_exposure_mode(self):
        self.exposure_mode = True

    def manual_exposure_mode(self):
        self.exposure_mode = False

    # Getter and Setter methods for gain
    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def set_gain(self, gain):
        self.gain = 0

    # Getter and Setter methods for video format
    def get_video_format(self):
        return self.video_format

    def set_video_format(self, video_format):
        self.video_format = video_format

    # Getter and Setter methods for roi
    def get_roi(self):
        return self.roi


    def set_roi(self, roi):
        self.roi = roi

    # Setter functions

