import sys
from collections import namedtuple
import numpy as np
import cv2
sys.stdout.flush()
Detection = namedtuple("Detection", ["image_path", "gt", "pred"])
face_cascade = cv2.CascadeClassifier('test.xml')
#3 : 0.01
#6 : 0.05
#9 : 0.14
#12 : 0.36
#15 : 0.15
# define the `Detection` object
#Detection = namedtuple("Detection", ["image_path", "gt", "pred"]) 
def bb_intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
	# compute the area of intersection rectangle
	interArea = (xB - xA ) * (yB - yA )#+1 de lam gi
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])#+1 de lam gi
	boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])#+1 de lam gi
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)
 	
	# return the intersection over union value
	return iou

def doOverlap(x0,y0,x1,y1,a0,b0,a1,b1):
	overLap = True
	
	# determine if the rectangle is on the side or over each other or not
	if (x0 > a1) or (a0 > x1) or (y1 < b0) or (b1 < y0):
		overLap = False
	return overLap

#return true if number and false if not
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

count_line=0
#open file
with open("test.txt") as f:
	#loop through each line in location.txt
	for line in f:
		list = []
		count_line+=1
		i=0
		#break line (after each space) ex: 1.JPG numObject x11 y11 x12 y12 x21 y21 x22 y22 into element ["1.JPG","numObject",...]
		for token in line.split():
			list.append(token)#add element in the end of list

		input_true = []
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
		img = cv2.imread("new/"+str(list[0]))
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.005, 15, minSize=(8,8),maxSize=(30,30))
		tempInputTrue = 0

		count_match=0
		for i in xrange(1,int(numObject)+1):
			print i
			x11=int(input_true[tempInputTrue])
			x12=int(input_true[tempInputTrue+1])
			x21=int(input_true[tempInputTrue])+int(input_true[tempInputTrue+2])
			x22=int(input_true[tempInputTrue+3])+int(input_true[tempInputTrue+1])
			#----------
			#cv2.rectangle(img,(x11,x12),(x21,x22),(0,255,0),2)
			#loop through each predicted faces
			for (x,y,w,h) in faces:
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
				Detection.gt = [x11,x12,x21,x22]
				Detection.pred = [x,y,x+w,y+h]
				#cv2.rectangle(img,(x11,x12),(x21,x22),(0,255,0),2)
			#	check overlap if do -> calculate iou
				if doOverlap(x11,x12,x21,x22,x,y,x+w,y+h):
					iou = bb_intersection_over_union(Detection.gt,Detection.pred)
					#match if iou>0.5
					if iou>0.5:
						count_match+=1
						print("iou : "+str(iou))
			#index +4 
			tempInputTrue+=4
		for (x,y,w,h) in faces:
			Detection.pred=[x,y,x+w,y+h]
			for i in xrange(1,int(numObject)+1):
				x11=int(input_true[tempInputTrue])
				x12=int(input_true[tempInputTrue+1])
				x21=int(input_true[tempInputTrue])+int(input_true[tempInputTrue+2])
				x22=int(input_true[tempInputTrue+3])+int(input_true[tempInputTrue+1])
				Detection.gt= [x11,x12,x21,x22]
				if doOverlap(x11,x12,x21,x22,x,y,x+w,y+h):
					iou = bb_intersection_over_union(Detection.gt,Detection.pred)
					#match if iou>0.5
					if iou<=0.5:
						print"cropping object"
						crop_img = gray[x:(x+w),y:(y+h)]
				else:
					print "cropping object"
					crop_img = gray[x:(x+w),y:(y+h)]
					

		cv2.imshow("frame",img)
		cv2.waitKey(83)
		#cv2.destroyAllWindows()
		#--------------
