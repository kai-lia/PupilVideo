import tkinter as tk
import cv2
import PIL

class MyVideoCapture:
    def __init__(self, video_source=1):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open this camera \n select another video source", video_source)
 
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
        self.flipped = True

    def getFrame(self):
        if self.vid.isOpened():
            isTrue, frame = self.vid.read()
            if isTrue and self.flipped:
                frame = cv2.flip(frame, 1)
            if isTrue:
                return (isTrue, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (isTrue, None)
        else:
            return (isTrue, None)
 
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            
def snapshot():
    file = tk.filedialog(
        mode='rb', defaultextension='.png',title="Choose Overlay Image", filetypes=[("PNG Files", '*.png')]
    )
    if file:
        overlay_img = PIL.ImageTk.PhotoImage(file=file)

window = tk()
window.resizable(0, 0)

video = MyVideoCapture(1)
canvas = tk.Canvas(window, width=video.width, height=video.height, bg='red')

Snapshot = tk.Button(window, text='snapshot', width=10, command=snapshot)

