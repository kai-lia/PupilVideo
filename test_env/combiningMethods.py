import numpy as np
import matplotlib.pyplot as plt
import cv2

def main():
    # Adjust the figure size and axes limits
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    ax.set_xlim(1, 10)
    ax.set_ylim(1, 10)

    # Generate linear data points
    x = np.linspace(1, 10, 100)
    y = 2 * x + 3

    # Plot the linear graph
    line, = ax.plot(x, y, color='blue')

    # Load the video file
    video_path = 1
    cap = cv2.VideoCapture(video_path)

    # Get the original video's dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a video overlay using OpenCV
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the video frame to match the graph's dimensions
        frame = cv2.resize(frame, (width, height))

        # Convert BGR to RGB color space
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Show the video frame as an overlay on the graph
        line.set_zorder(1)  # Make sure the graph is behind the video overlay
        ax.imshow(frame, extent=[1, 10, 1, 10], aspect='auto', alpha=0.7)

        # Update the plot
        plt.pause(0.001)

        # Clear the current frame for the next iteration
        ax.images[-1].remove()

    # Release the video capture and close the plot
    cap.release()
    plt.close()

if __name__ == '__main__':
    main()
