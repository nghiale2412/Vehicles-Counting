import cv2
from collections import namedtuple
import numpy as np

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


imageName=1
with open("testthu.txt") as f:
	#loop through each line in location.txt
	for line in f:
		list = []
		i=0
		#break line (after each space) ex: 1.JPG numObject x11 y11 x12 y12 x21 y21 x22 y22 into element ["1.JPG","numObject",...]
		for token in line.split():
			list.append(token)#add element in the end of list

		while i<len(list): #loop through whole line
			try:
			#check if the input is a number or not
			#if it isnt a number -> path name
				if isInt(list[i]):
					if i==1:
						numObject = list[i] #numObject = number of objects in image
						print "no of object : "+numObject
					else:
						input_true.append(list[i])#add coor in end of list
				else:
					path=list[i]#path = path name
					print "image path : "+path
			finally:
				i+=1
		img = cv2.imread("pos/"+str(list[0]))
		height = np.size(img,0)
		width = np.size(img,1)
		print height
		print width
		cv2.imshow("frame",img)
		cv2.waitKey(0)