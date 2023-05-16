from tkinter import *
import cv2
from PIL import Image, ImageTk
import time
from tkinter import filedialog


class App:
# Check what video_source does, 1 makes it so it records from laptop. Not sure how it translates to lab cam?
    def __init__(self, video_source=1):
        # Initialize frame
        self.overlay_img = None
        self.appName = "Testing"
        self.window = Tk()
        self.window.title(self.appName) 
        self.window.resizable(0, 0)
        # self.window.wm_iconbitmap("cam.ico")
        self.window['bg'] = 'black'
        self.video_source = video_source
 
        # Set up for video capture
        self.vid = MyVideoCapture(self.video_source)
        # self.label = Label(self.window, text=self.appName, font=15, bg='blue', fg='white').pack(side=TOP, fill=BOTH)
        self.canvas = Canvas(self.window, width=self.vid.width, height=self.vid.height, bg='red')
        self.canvas.pack()
        
        # Features for buttons
        self.btn_snapshot = Button(self.window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(side=LEFT, padx=10)
        self.btn_flip = Button(self.window, text="Flip Image", width=50, command=self.flip_img)
        self.btn_flip.pack(side=LEFT, padx=10)
        self.btn_overlay = Button(self.window, text="Overlay", width=50, command=self.overlay)
        self.btn_overlay.pack(side=LEFT, padx=10)
 
        self.update()
        self.window.mainloop()
 
    def flip_img(self):
        """Flips image
        """
        self.vid.flipped = not self.vid.flipped
 
    def overlay(self):
        """Overlays image on frame
        """
        file = filedialog.askopenfile(
            mode='rb', defaultextension='.png',title="Choose Overlay Image", filetypes=[("PNG Files", '*.png')])
        if file:
            self.overlay_img = ImageTk.PhotoImage(file=file)
            self.canvas.tag_raise(self.overlay_img)
            self.canvas.create_image(0, 0, image=self.overlay_img, anchor=NW)
 
    def snapshot(self):
        """Overlaps snapshot of image on frame
        """
        file = filedialog.askopenfile(
        mode='rb', defaultextension='.png',title="Choose Overlay Image", filetypes=[("PNG Files", '*.png')])
        if file:
            self.overlay_img = ImageTk.PhotoImage(file=file)
 
    def update(self):
        """Updates frame
        """
        isTrue, frame = self.vid.getFrame()
  
        if isTrue:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.tag_lower(self.photo)
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
    
        if self.overlay_img:
            self.canvas.tag_raise(self.overlay_img)
            self.canvas.create_image(0, 0, image=self.overlay_img, anchor=NW)
    
        self.window.after(100, self.update)


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


if __name__ == "__main__":
    App()
