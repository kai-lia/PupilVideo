import cv2
import numpy as np

# Function to draw a growing non-static linear graph
def draw_graph(frame, prev_x, prev_y, x, y, color):
    # Draw the line segment
    # cv2.line(frame, (prev_x, prev_y), (x, y), color, thickness=10)
    cv2.circle(frame, (x, y), radius=5, color=color, thickness=-10)

# Function to overlay the graph on the video frame
def overlay_graph(frame, x, y, prev_x, prev_y, color):
    # Draw the graph on the frame
    draw_graph(frame, prev_x, prev_y, x, y, color)

    # Update the previous position
    prev_x = x
    prev_y = y

    # Increase the position for the next frame
    x += 10
    y = int(x * 0.75)  # Adjust the slope of the graph as desired

    return x, y, prev_x, prev_y

# Open the video capture
cap = cv2.VideoCapture(1)  # Use 0 for default camera or provide the path to a video file

# Read the first frame to get the dimensions
ret, frame = cap.read()
height, width, _ = frame.shape

# Initial positions of the graph
x_pos = 0
y_pos = 0
prev_x_pos = 0
prev_y_pos = 0

# Color of the graph (in BGR format)
graph_color = (x_pos, y_pos, x_pos + y_pos) 


while True:
    # Read the frame from the video capture
    ret, frame = cap.read()

    # Break the loop if the video capture is over
    if not ret:
        break

    # Overlay the graph on the frame
    x_pos, y_pos, prev_x_pos, prev_y_pos = overlay_graph(frame, x_pos, y_pos, prev_x_pos, prev_y_pos, graph_color)

    # Mod to ensure dot stays in frame
    y_pos = y_pos % height
    x_pos = x_pos % width
    # Show the frame
    cv2.imshow("Video", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()
