import cv2
import numpy as np
import os

file = open("newlocationwithout1over3.txt","w")

def isInt(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

with open("location.txt") as f:
	# loop through each line in your .txt file
	for line in f:
		list = []
		i=0
		# break line (after each space) ex: 1.JPG numObject x11 y11 x12 y12 x21 y21 x22 y22 into element ["1.JPG","numObject",...]
		for token in line.split():
			list.append(token)# add element in the end of list

		input_true = []
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
					file.write(str(list[0]))
			finally:
				i+=1
		tempInputTrue = 0
		count_object=0
		for i in xrange(1,int(numObject)+1):
			#print i
			x11=int(input_true[tempInputTrue])
			x12=int(input_true[tempInputTrue+1])
			x21=int(input_true[tempInputTrue])+int(input_true[tempInputTrue+2])
			x22=int(input_true[tempInputTrue+3])+int(input_true[tempInputTrue+1])
			if (x12>=180):
				count_object=count_object+1
				#file.write(" "+str(x11)+" "+str(x12)+" "+str(input_true[tempInputTrue+2])+" "+str(input_true[tempInputTrue+3]))
			tempInputTrue+=4
		file.write(" "+str(count_object))
		
		tempInputTrue = 0
		for i in xrange(1,int(numObject)+1):
			#print i
			x11=int(input_true[tempInputTrue])
			x12=int(input_true[tempInputTrue+1])
			x21=int(input_true[tempInputTrue])+int(input_true[tempInputTrue+2])
			x22=int(input_true[tempInputTrue+3])+int(input_true[tempInputTrue+1])
			if (x12>=180):
				count_object=count_object+1
				file.write(" "+str(x11)+" "+str(x12)+" "+str(input_true[tempInputTrue+2])+" "+str(input_true[tempInputTrue+3]))
			tempInputTrue+=4
		print("")
		file.write("\n")