import numpy as np
import cv2

# Clear all variables in the workspace
# There is no equivalent statement in Python

# Close all figures or windows
# There is no equivalent statement in Python

# Set the initial path for the file dialog box
start_path = 'C:/Programs/AOSLOBerkeleyNewCamera/'

# Display a dialog box for the user to select a file
filename = filedialog.askopenfilename(initialdir=start_path)

# Load the selected file into the workspace
data = np.load(filename)

# Get the number of frames per block
vformat = data.shape[1]

# Calculate the number of blocks in the video
I1 = data.shape[0] // vformat

# Iterate over each block in the video
for f in range(I1):
    # Get the frames for the current block
    V = data[f * vformat:(f + 1) * vformat, :, :] + 0

    # Convert the frames to grayscale
    V1 = cv2.cvtColor(V, cv2.COLOR_BGR2GRAY)

    # Crop the frames to remove the border pixels
    AvoidedBorder = 1
    Vt = V[AvoidedBorder:-AvoidedBorder, AvoidedBorder:-AvoidedBorder]

    # Display the frames as an image
    cv2.imshow('Video', Vt)

    # Wait for a key press or 0.5 seconds
    key = cv2.waitKey(500)
    if key == ord('q'):  # Exit the loop if the 'q' key is pressed
        break

# Close the video window
cv2.destroyAllWindows()