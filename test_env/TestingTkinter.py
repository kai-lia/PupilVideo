import cv2
import tkinter as tk
from PIL import Image, ImageTk

# Initialize the video capture
cap = cv2.VideoCapture(1)

# Create a tkinter window
window = tk.Tk()
window.title("Video Capture")
canvas = tk.Canvas(window, width=640, height=480)
canvas.pack()

def update_frame():
    ret, frame = cap.read()  # Read a frame from the video capture

    if ret:
        # Convert the frame to PIL Image format
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Resize the image to fit the canvas
        image = image.resize((640, 480), Image.ANTIALIAS)

        # Convert the PIL Image to Tkinter PhotoImage format
        photo = ImageTk.PhotoImage(image)

        # Update the canvas with the new frame
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo

    # Schedule the next frame update
    window.after(1, update_frame)

# Start updating the frame
update_frame()

# Start the tkinter event loop
window.mainloop()

# Release the video capture and destroy the window
cap.release()
cv2.destroyAllWindows()
