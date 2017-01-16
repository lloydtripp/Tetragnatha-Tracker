CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Requirements
 * Recommended modules
 * Installation
 * Configuration
 * Instructions
 * Troubleshooting
 * FAQ
 * Maintainers


---------------------
 * Introduction

The goal of this program is to track the Tetragnatha as it approaches the ends of the Y-olfactometer. The program guesses the location of the spider based on the difference in pixels based off of the sample frame taken around the beginning of the program. Users define the sections that the spider shall be considered to be located rather than the pixel location of the spider.

---------------------
 * Requirements

CPU: Quad core CPU 3.0GHz
RAM: 4GB DDR3
GPU: GeForce GTX 760-class (2 GB) or Intel HD Graphics 3000 (or later)
OS: Recommended either Windows 7 (or higher) or OSX.
Storage: At least 1GB free

---------------------
 * Required Modules

 - Python 2.7
 - Numpy 1.5 or later
 - OpenCV 2.4
 - Imutils 0.3.6

---------------------
 * Installation

---------------------
 * Configuration

Please install all required modules and software. There is no configuration required other than editing the software's defaults that may lead to cumbersome redundant command runs. Some defaults include minimum and maximum area size of the spider as it might have to be changed depending on the size of the video (pixel dimensions). The other default is the frame sampled to compare the later frames as the software depends on comparing the current frame to a static frame.

---------------------
 * Instructions

Please see the included instructions.pdf file that is included with the distribution of this software. If not found, please contact the maintainer for instructions.

---------------------
 * Troubleshooting and Best Practices

Issue: The program detects a spider when there is none throughout the whole frame.
Solution: Change the sampled frame. The frame grabbed may include an artifact that is not present in the following frames thus the comparisons made think there is an object (the size of a spider) present in the feed.

Issue: The program detected a spider when there was none for a couple frames.
Solution: If there is a dramatic change in lighting then the program will interpret the feed as having a spider. Please manually edit the artifact in the saved log file.

Best Practices:
 1. Manually observe the video feed and record any artifacts that present themselves for the duration of the video.
 2. Make sure that there is no lighting changes for the duration of the video when recording.
 3. Make sure the camera during recording does not jostle or change direction.
 4. Sample a frame that is similar to all the other frames in the video feed (i.e. doesn't include an artifact).

---------------------
 * FAQ

Under progress. Please contact maintainer with questions to populate this resource.

---------------------
 * Maintainers

 Please contact Lloyd Tripp at lloydmtripp@gmail.com or lloydt@berkeley.edu
