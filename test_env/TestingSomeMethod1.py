import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Function to update the graph based on variables 'x' and 'slope' and frame dimensions
def update_graph(x, slope, width, height):
    graph = np.zeros((height, width, 3), np.uint8)
    y = slope * x / width
    y = height - int(y * height)
    cv2.line(graph, (0, height), (x, y), (0, 255, 0), 3)
    return graph

# Create a video capture object
cap = cv2.VideoCapture(1)

# Set the desired size for the resized video feed
resized_width = 640
resized_height = 480

# Create a tkinter window
window = tk.Tk()
window.title("Video Overlay")

# Create a frame for GUI elements on the left side
left_frame = tk.Frame(window)
left_frame.pack(side=tk.LEFT)

# Create a frame for GUI elements on the right side
right_frame = tk.Frame(window)
right_frame.pack(side=tk.RIGHT)

# Create scaler labels in the left frame
scaler_x = tk.Label(left_frame, text="X")
scaler_x.pack(side=tk.BOTTOM, anchor=tk.E)
for i in range(11):
    label = tk.Label(left_frame, text=str(i))
    label.pack(side=tk.BOTTOM, anchor=tk.E)

# Create slope scale in the right frame
slope_scale = tk.Scale(right_frame, label="Slope", from_=-10, to=10, resolution=0.1, orient=tk.VERTICAL)
slope_scale.pack(side=tk.TOP)

# Create scaler labels in the right frame
scaler_y = tk.Label(right_frame, text="Y")
scaler_y.pack(side=tk.TOP)
for i in range(11):
    label = tk.Label(right_frame, text=str(i))
    label.pack(side=tk.TOP)

flip = False

# Create a flip button in the left frame
def flip_video():
    global flip
    flip = not flip

flip_button = tk.Button(left_frame, text="Flip", command=flip_video)
flip_button.pack(side=tk.BOTTOM)

# Create a label to display the video feed in the center
video_label = tk.Label(window)
video_label.pack()

# Main loop
def update_frame():
    global flip

    # Read a frame from the video feed
    ret, frame = cap.read()

    # Flip the frame horizontally if 'flip' flag is True
    if flip:
        frame = cv2.flip(frame, 1)

    # Resize the frame to the desired dimensions
    resized_frame = cv2.resize(frame, (resized_width, resized_height))

    # Get the width and height of the resized frame
    height, width, _ = resized_frame.shape

    # Get the current slope value from the scale
    slope = slope_scale.get()

    # Generate a linear graph based on the width, height, and slope
    graph = update_graph(width, slope, width, height)

    # Overlay the graph on the resized frame
    overlay = cv2.addWeighted(resized_frame, 0.7, graph, 0.3, 0)

    # Convert the overlayed frame to RGB format
    overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)

    # Convert the RGB frame to PIL Image format
    img = Image.fromarray(overlay_rgb)

    # Convert the PIL Image to Tkinter-compatible Image
    img_tk = ImageTk.PhotoImage(image=img)

    # Update the video label with the new frame
    video_label.img_tk = img_tk
    video_label.configure(image=img_tk)

    # Schedule the next frame update
    video_label.after(20, update_frame)

# Start updating the frames
update_frame()

# Run the Tkinter event loop
window.mainloop()

# Release the video capture object
cap.release()
