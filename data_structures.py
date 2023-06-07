class CameraSettings:
    def __init__(self):
        # the 4 slider values
        self.brightness = 240
        self.gamma = 1
        self.exposure = 0.0333
        self.gain = 0

        self.exposure_mode = True
        self.iris = 1
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
        return self.exposure

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

    def reset_exposure_mode(self):
        self.exposure_mode = True

    def manual_exposure_mode(self):
        self.exposure_mode = False

    # Getter and Setter methods for gain
    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        
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
        
class CalibrationSettings:
    def __init__(self):
        self.pixel_calibration = 49.5517721152208 # 1
        self.TCAmmX = 3.500 # 2
        self.TCAmmY = 3.500 # 3 
        self.tolerated_pupil_dist= 0.150 # 4
        
        
    # Getter and Setter methods pixel_calibration
    def get_pixel_calibration(self):
        return self.pixel_calibration

    def set_pixel_calibration(self, pixel_calibration):
        self.pixel_calibration = pixel_calibration 
        
    # Getter and Setter methods TCAmmX
    def get_TCAmmX(self):
        return self.TCAmmX
  
    def set_TCAmmX(self, TCAmmX):
        self.TCAmmX = TCAmmX
        
    # Getter and Setter methods TCAmmY
    def get_TCAmmY(self):
        return self.TCAmmY

    def set_TCAmmY(self, TCAmmY):
        self.TCAmmY = TCAmmY
        
    # Getter and Setter methods tolerated_pupil_dist
    def get_tolerated_pupil_dist(self):
        return self.tolerated_pupil_dist
  
    def set_tolerated_pupil_dist(self, tolerated_pupil_dist):
        self.tolerated_pupil_dist = tolerated_pupil_dist
    
