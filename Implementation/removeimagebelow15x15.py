# Coded by Le Trung Nghia 
# Make sure you backup your files before performing delete.
import cv2
import numpy as np
import os

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

with open("pos1515.txt") as f:
	# loop through each line in your .txt file
	for line in f:
		list = []
		i=0
		# break line (after each space) ex: 1.JPG numObject x11 y11 x12 y12 x21 y21 x22 y22 into element ["1.JPG","numObject",...]
		for token in line.split():
			list.append(token)# add element in the end of list

		while i<len(list): # loop through whole line
			try:
			# check if the input is a number or not
			# if it isnt a number -> path name
				if isInt(list[i]):
					if i==1:
						numObject = list[i] # numObject = number of objects in image
					else:
						input_true.append(list[i])# add coor in end of list
				else:
					path=list[i] # path = path name
			finally:
				i+=1
		img = cv2.imread(str(list[0]))
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# get height 
		height = np.size(img,0)
		# get width
		width = np.size(img,1)
		if height <15 or width <15:
			print "Height:",height 
			print "Width:",width
			os.remove(str(list[0]))
			print 'Image has been removed.'
		cv2.waitKey(2)