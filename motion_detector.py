# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# Fixes division to be from 3.x.x python
from __future__ import division

import sys
import os
sys.path.append('/usr/local/lib/python2.7/site-packages')
# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
from datetime import datetime

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=100, help="minimum area size")
ap.add_argument("-b", "--max-area", type=int, default=5000, help="maximum area size")
ap.add_argument("-c", "--camera", type=int, help="camera number")
ap.add_argument("-f", "--frame", type=int, default=100, help="frame to sample from")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)

# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])


# if the camera argument is not set, break the program and tell the person that a "-c" is required
if args.get("camera", None) is None:
	print "Next time please add the '-c' flag and number of the camera to your argument."
	args["camera"] = int(input("Which camera is this a video recording of?"))



# Create folder to store all the analysis information (output video, capture photo, log file)
path = str( os.path.splitext(args.get("video"))[0])
if not os.path.exists(path):
	os.mkdir(path)

newpath= str(path + "/")

###Beginning of log header
# Creates "logs" which should be a list of 3 tuples (timestamp, x-coordinate, and y-coordinate
# Variable is called locationlog
# The name of the file is called the video file's name and adds ".log"
locationlog = open(newpath + args["video"]+ ".log", mode="w")
# writes the header for the file
# First line includes file name.
locationlog.write("Filename: " + args["video"]+ "\n")
# Line includes the length of the video
	# As of yet, you cannot get the camera length
####locationlog.write("Video length: " + camera.get())
# Line includes the date of analysis. Could be useful to determine the version of the software used
locationlog.write("Date analyzed: " + str(datetime.today()) + "\n")
# Line includes the number of the camera
locationlog.write("Camera Number: " + str(args["camera"]) + "\n")
# Line includes the frame sampled
locationlog.write("Frame sampled: " + str(args["frame"]) + "\n")
# Line includes the minimum and maximum area of the spider
locationlog.write("Minimum area: " + str(args["min_area"]) + ", Maximum area: " + str(args["max_area"]) + "\n")
#line includes table header (top xy-coordinate of line, bottom xy-coordinate of line, x-slope, x-intercept )
locationlog.write("Sector lines created for this video: top xy-coordinate, bottom xy-coordinate, x-slope, x-intercept \n")

#End log file header additions

fps = 15
#capSize = (int(camera.get(3)),int(camera.get(4))) # this is the size of my source video
capSize = (int(camera.get(3)),int(camera.get(4)))
### Save for when video writing is fast enough or using a windows computer
#fourcc = cv2.cv.FOURCC('F','F','V','1')
#fourcc = cv2.cv.FOURCC('S', 'V', 'Q', '3')
#voutput = cv2.VideoWriter(newpath + str(args["video"]) +'_output.mp4',fourcc,fps,capSize,True)

# Sets the size of the font to use
RelScale = {}
RelScale["FontSize"] = 0.001 * camera.get(3) # Used for the general scaling relative to the picture width
RelScale["Thickness"] = int(0.002 * camera.get(3))


#open up window to setup sectors
camera.set(1,args["frame"])
(grabbed, frame) = camera.read()
cv2.putText(frame, "frame: {}".format(args["frame"]), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, RelScale["FontSize"], (0, 0, 255), RelScale["Thickness"])
cv2.imshow("Create Sections", frame)

# Master list that holds the pairs of points as an ordered pair (x,y), and line equation as m, b (form x = my + b)
# lines [[top left, bottom left ] [top right, bottom right]]
# Should get ordered from smallest to largest with respect to b (the fourth entry in all first-level elements)
lines = [
			[[0, 0],[0, camera.get(4)], 0, 0],
			[[camera.get(3), 0],[camera.get(3), camera.get(4)], 0, camera.get(3)]
		]
# Holds the first point
point_holder = []
# Allows make_point to add the two points to lines list or hold on to the first points
	# False -> Hold on to the first points
	# True -> Add the two points to lines list
firstpoint = False

# Saves clean frame
cleanframe = frame

# Defines callback function that literally does everything......
### We should fix the organization of this code
def make_point(event,x,y,flags,param):
	global lines
	global point_holder
	global firstpoint
	global frame
	if firstpoint == True and event == cv2.EVENT_LBUTTONDOWN:

		# calculuates the x-intercept formula
		m = (point_holder[0] - x)/(point_holder[1] - y)
		b = int(point_holder[0] - (m * point_holder[1]))

		# Enter in code to add locations to list
	### the below line should look like: lines.append([point_holder, [x, y], m, b])
		lines.append([[int(b), 0], [int(m * camera.get(4) + b), int(camera.get(4))], m, b]) #Appends to master list

		# Orders the lines in lines[] based off of b from smallest to largest
		lines.sort(key=lambda line: line[3])

		# Assigns value g to the index of where the last line was added.
		# This is allow us to quickly remove that line because the line turned out to overlap
		g = next(((i, line.index(m)) for i, line in enumerate(lines) if m in line), None)

		# Checks that lines do not overlap
		i = 1
		while i < len(lines):   # Python indexes start at zero
			# Former's bottom point's x-coord calculation
			v = int(lines[i-1][1][0])
			# Later's bottom point's x-coord calculation
			w = int(lines[i][1][0])
			# Checks if the bottom point's x-coord is greater than the next line's bottom point x-coord
			i = i + 1
			if v > w:
				del lines[g[0]]

		for line in lines:
			cv2.line(frame, (int(line[0][0]), int(line[0][1])), (int(line[1][0]), int(line[1][1])), (255,255,255),1)
		cv2.imshow("Create Sections", frame)

		firstpoint = False #Resets firstpoint so next click holds on to the coordinate
	elif firstpoint == False and event == cv2.EVENT_LBUTTONDOWN: #event == cv2.EVENT_LBUTTONDOWN and firstpoint == False:
		point_holder = [x,y]
		firstpoint = True #First point is held so allows next point click to add pair of coordinates to lines

# Activates callback function for window
cv2.setMouseCallback("Create Sections", make_point)

# Allows user to enter in sectors
while True:
	if not grabbed:
		break
	# Create a loop to create a two point system that defines a line
	# Data structure { l1, l2 , l3..., ln} where l is a {p1,p2} where p is a point defined by {x,y}

	# User selects point -> User selects new point -> points created in list - > Draw sector


	# Creates to reset to clear all sector divisons created
	# Redraws sector divisions

	###
	# Allows user to exit if can't finish or some weird reason
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break
	### END of code to allow user to finish

# Writes out the data for the sector divisions to log file
for listitem in lines:
	locationlog.write(str(listitem) + '\n')

# Saves out what the frame looks like with the divisions to a .jpg for later use and review
cv2.imwrite(newpath + args["video"] + "_capture" + ".jpg", frame)

# initialize the first frame in the video stream
firstFrame = None

# Defines last_location so that if we lose the location of the spider by default we say where it last was
last_location = [-1,-1]
if args["camera"] % 2 == 0:
	last_location = [camera.get(3), -1]
### Second Table Header
#line includes table header (time, x, y, sector number, detected spider )
locationlog.write("Frame Number, Time of frame since beginning of video (ms), x-coordinate, y-coordinate, sector number, detected \n")
### End of Second Table Header

# Because the first part of the program took the 10th frame of the video, we have to reset the feed to the beginning of the video
# Should this be set to the user's discretion?
camera.set(1,1)

# loop over the frames of the video for coordinate analysis
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	text = 0

	# Remember to not count the spider as being on screen if the location is (-1,-1)
	location = [ -1 , -1 ]
	if args["camera"] % 2 == 0:
		location = [camera.get(3), -1]
	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	# (resize the frame not doing this) convert it to grayscale, and blur it
	#frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	if firstFrame is None:
		camera.set(1,args["frame"])
		(grabbed, frame) = camera.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)
		firstFrame = gray
		camera.set(1,1)
		(grabbed, frame) = camera.read()
		continue

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	# (x,y,w,h). x and y are initially set to -1,-1 so because the location is updated later on in the for loops
	## doesn't matter all to much that we take into account the even camera numbers
	largest_square = [-1,-1,0,0]
	if args["camera"] % 2 == 0:
		largest_square = [camera.get(3), -1, 0, 0]

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue
		if cv2.contourArea(c) > args["max_area"]:
			continue
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		if w * h > largest_square[2] * largest_square[3]:
			largest_square = [x, y, w, h]
		# cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) where x,y,w,h come from largest_square list
		cv2.rectangle(frame, (largest_square[0], largest_square[1]), (largest_square[0] + largest_square[2], largest_square[1] + largest_square[3]), (0, 255, 0), 2)

		# Because c is looping through cnts, thus there must be a spider detected
		text = 1

	# Updates location to give position of spider on screen
	# location = [(x + w)/2, (y+h)/2] where x,w,y,h come from largest_square list
	location = [(2*largest_square[0] + largest_square[2])/2, (2*largest_square[1]+largest_square[3])/2]
	cv2.circle(frame, (int(location[0]),int(location[1])), 5, (250, 250, 250), 1)

	# Calculate the sector that the spider is in
	### What do we do if we don't know where the spider is? --> Use the past location. What if there is no past location?
	## does this code make sense?
	if location == [-1,-1]:
		# Because we lost the spider, we should use the previous location
		location = last_location
	elif location == [camera.get(3),-1]:
		# Because we lost the spider using an even numbered camera
		location = last_location
	else:
		last_location = location
		# Because we found the spider, we should update its last known location

	# Find the x-value associated to the y value of the spider's current location
	xvalues = []
	for li in lines:
		xvalues.append(int(li[2]*last_location[1] + li[3])) # Appends x value from x=my+b where y is the y-coordinate of the spider
	if (args['camera'] % 2) == 1:
		xvalues.reverse()

	i = 1
	# When the spider isn't detected initially, the sector should thus be in the farthest sector aka not on screen
	sector = len(lines) -1

	#We change the ordering of xvalues dependent on the camera being odd or even
	if (args['camera'] % 2 == 1):
		while (i < len(lines)):
			if location[0] > xvalues[i]:
				sector = i
				break
			else:
				i = i + 1
	else:
		while (i < len(lines)):
			if location[0] < xvalues[i]:
				sector = i
				break
			else:
				i = i + 1

	# Adds lines to the frame for review and live viewing
	for line in lines:
		cv2.line(frame, (int(line[0][0]), int(line[0][1])), (int(line[1][0]), int(line[1][1])), (255,255,255),1)

	# Create data point to save to locationlog file
	# Append to list called "logs"
	# Adds a line in the format: frame number, frame time (ms), x-coordinate, y-coordinate, sector number, and if occupied ( 1 is yes; 0 is no)
	locationlog.write(str(camera.get(1)) + ", "+str(camera.get(0)) + ", " + str(location[0]) + ", " + str(location[1]) + ", " + str(sector)+ ", " + str(text)+ "\n")

	# draw the text and timestamp on the frame
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, RelScale["FontSize"], (0, 0, 255), RelScale["Thickness"])
	cv2.putText(frame, "[x,y]: [" + str(last_location[0]) + "," + str(last_location[1]) + "], Sector: " + str(sector) + ". Frame #: " + str(camera.get(1)),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, RelScale["FontSize"], (255, 255, 255), RelScale["Thickness"])


	# show the frame and record if the user presses a key
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	cv2.imshow("Security Feed", frame)

	#Writes out the final print out to the output file. SAVE for video writing
	#voutput.write(frame)


	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the loop
	if key == ord("q"):
		break

print "Done!"

# cleanup the camera and close any open windows
camera.release()
#voutput.release()
cv2.destroyAllWindows()
