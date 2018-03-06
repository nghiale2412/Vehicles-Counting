import sys
from collections import namedtuple
import numpy as np
import cv2
sys.stdout.flush()
count_line=0
file = open("pos1515.txt","w")
with open("location1515.txt") as f:
	#loop through each line in location.txt
	for line in f:
		list = []
		for token in line.split():
			list.append(token)#add element in the end of list
		temp=line
		img = cv2.imread("pos1515/"+str(list[0]))
		height, width, channel = img.shape
		print str(list[0])
		print width, height
		file.write(str(list[0])+" 1 0 0 "+str(width)+" "+str(height)+"\n")
file.close()