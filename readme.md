
<a name="readme-top"></a>
  <h3 align="center">Pupil Video Tracking</h3>

  <p align="center">
    Read Me for Future Usage
    <br />
    <a href="https://github.com/kai-lia/PupilVideo"><strong>Explore the doc
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About</a>
      <ul>
        <li><a href="#original-code">Original Code</a>
        <ul>
        <li><a href="#translation-guide">Translation Guide</a></li>
      </ul>
      </li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

### Original Code

Past Github: https://github.com/Roorda-Tuten-Labs/AOMcontrol

Why Change in code:
* Running too many Matlab Dependencies at the same time 
* Better Documentation
* Optics Code is hard to read/change

If checking out the orginal code here is a translation guide major changes from original code are in PupilVideoAlg also nameing conventions and coding style. 

### Translation Guide

#### Buttons
| Original Matlab | Current Code |
| ----------- | ----------- |
| Button 1 | Quit |
| Button 2 | Start Video |
| Button 3 | Set Reference |
| Button 4 | Load Reference |
| Button 5 | Save Video |
| Button 7 | Draw BE |
| Button 8 | Save Pupil Tracking |
| Button 9 | Save Sync |
| Button 10 | Manual |
| Button 11 | Save Settings |
| Button 13 | Reset |
| Button 14 | Enable TCA Correction |
| Button 15 | Disable Tracking |
| Button 16 | Zoom In |
| Button 21 | Show Focus |

#### Slider Translations

| Original Matlab | Current Code |
| ----------- | ----------- |
| Slider 3 | Brightness |
| Slider 4 | Gamma |
| Slider 5 | Exposure |
| Slider 6 | Gain |

#### Edit Translations

| Original Matlab | Current Code |
| ----------- | ----------- |
| Edit 1 | Save Video Seconds |
| Edit 2 | FPS |
| Edit 3 | Type Pupil File name Prefix |
| Edit 6 | calibrations/tollernc(.mm) |
| Edit 7 | TCA |


## Getting Started

Instructions on setting up project locally To get a local copy up and running follow these simple example steps.

### Dependancies

- Python (3.x recommended)
- Tkinter
- OpenCV
- Matplotlib
- Numpy


_Installing and setting up your app locally_

1. Check python version
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install packages
   ```sh
   pip install requirments.txt
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


# gui.py
used tkinter to make interface
## User Interface Components

### Top Frame (Horizontal Button Layout):

 Buttons for basic video control, including start, stop, and reference management.

- Quit: Exits the application.
- Start Video: Initiates video streaming.
- Set Reference: Sets a reference point/frame for tracking or comparison.
- Load Reference: Loads a previously set reference point/frame.
- Disable Tracking: Turns off any ongoing tracking features.
- Draw BE: Activates the Draw BE feature (purpose-specific).

### Left Frame (Vertical Layout):

Focuses on saving functionalities and settings, along with pupil tracking options.

- Sync Save: Saves current settings in sync.
- Save Video: Saves the current video stream.
- Save Video Settings: Includes fields for seconds (secs) and frames per second (fps).
- Save Pupil Tracking: save pupil tracking data.
- Type Pupil File Name: Input for naming tracking files.

### Right Frame (Vertical Layout with Settings Box):

Contains advanced settings for the video camera and calibration tools.

Video Camera Settings:
- Buttons for Auto, Reset, Save Settings, and Load Settings.
- Sliders for adjusting Brightness, Gamma, Exposure, and Gain.
- Enable TCA Correction: Button to enable TCA correction.
- Calibration Settings:
Input fields for tollernc.(mm) and TCA(X/Y)arcmin/mm.
Show Focus button to display focus settings.

### Middle Frame

Displays the video feed and provides options to annotate or draw on the video. 

Video Display and Control:
- The middle frame opens a video
- The video stream is integrated with a matplotlib figure, allowing for graphical overlaying on the video.
- A separate video frame is created within the middle frame for displaying the video content.


## Buttons

### Quit


### 


Button 1 | Quit |
| Button 2 | Start Video |
| Button 3 | Set Reference |
| Button 4 | Load Reference |
| Button 5 | Save Video |
| Button 7 | Draw BE |
| Button 8 | Save Pupil Tracking |
| Button 9 | Save Sync |
| Button 10 | Manual |
| Button 11 | Save Settings |
| Button 13 | Reset |
| Button 14 | Enable TCA Correction |
| Button 15 | Disable Tracking |
| Button 16 | Zoom In |
| Button 21 | Show Focus |


## Sliders

## Text Box




<p align="right">(<a href="#readme-top">back to top</a>)</p>

# PupilTrackingAlg.py



<!-- CONTACT -->
## Contact

Kaiona Martinson - [@kai-lia](https://github.com/kai-lia) - martinson.kaiona(@berkeley.edu)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

f

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
Brian P. Schmit's Prior documentation 
___ help with deciphering some of the MatLab code
no more optics code please 