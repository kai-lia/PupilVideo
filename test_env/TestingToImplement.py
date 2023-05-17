import cv2
import numpy as np

def draw_line(frame, start, end, color=(0, 0, 255), thickness=10):
    cv2.line(frame, start, end, color, thickness)
    
def draw_box(frame, start, width, height, color=(0, 0, 255), thickness=10):
    end = (start[0] + width, start[1] + height)
    cv2.rectangle(frame, start, end, color, thickness)

"""Runs the video loop to show how the functions work"""
if __name__ == "__main__":
    # Open the video capture
    cap = cv2.VideoCapture(0)

    # Read the first frame to get the dimensions
    ret, frame = cap.read()
    height, width, _ = frame.shape
    
    # Initial positions of the linear graph
    line_x_pos = 10000
    line_y_pos = 1000
    line_prev_x_pos = 0
    line_prev_y_pos = 0

    # Initial positions of box graph
    box_x_pos = 100
    box_y_pos = 100
    box_width = 500
    box_heigh = 500

    while True:
        # Read the frame from the video capture
        ret, frame = cap.read()
        
        # Break the loop if the video capture is over
        if not ret:
            break
        
        # Overlay with line based on initialized points
        line_start = (line_prev_x_pos, line_prev_y_pos)
        line_end = (line_x_pos, line_y_pos)
        draw_line(frame, line_start, line_end)
        
        # Overlay with box based on intialized points
        box_start = (box_x_pos, box_y_pos)
        draw_box(frame, box_start, box_width, box_heigh)
        
        # Show the frame
        cv2.imshow("Video", frame)
        
        keypress = cv2.waitKey(1) & 0xFF
        
        # Exit if 'q' is pressed
        if keypress == ord('q'):
            break
        # Adjusts endpoint in the y axis
        elif keypress == ord('=') or keypress == ord('-'):
            change = keypress == ord('=')
            line_y_pos = line_y_pos + 50 - change * 100
        
    # Release the video capture and close the window
    cap.release()
    cv2.destroyAllWindows()
