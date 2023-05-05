class CameraSettings:
    def __init__(self):
        self._brightness = 240
        self._iris = 1
        self._exposure = 0.0333
        self._exposure_mode = 2
        self._gain = 0
        self._video_format = 'RGB24 (1216x1024) [Skipping 2x]'
        self._roi = [0, 0, 1216, 1024]

    # Getter and Setter methods for brightness
    def get_brightness(self):
        return self._brightness

    def set_brightness(self, brightness):
        self._brightness = brightness

    # Getter and Setter methods for iris
    def get_iris(self):
        return self._iris

    def set_iris(self, iris):
        self._iris = iris

    # Getter and Setter methods for exposure
    def get_exposure(self):
        return self._exposure

    def set_exposure(self, exposure):
        self._exposure = exposure

    # Getter and Setter methods for exposure_mode
    def get_exposure_mode(self):
        return self._exposure_mode

    def set_exposure_mode(self, exposure_mode):
        self._exposure_mode = exposure_mode

    # Getter and Setter methods for gain
    def get_gain(self):
        return self._gain

    def set_gain(self, gain):
        self._gain = gain

    # Getter and Setter methods for video format
    def get_video_format(self):
        return self._video_format

    def set_video_format(self, video_format):
        self._video_format = video_format

    # Getter and Setter methods for roi
    def get_roi(self):
        return self._roi


    def set_roi(self, roi):
        self._roi = roi

    # Setter functions

