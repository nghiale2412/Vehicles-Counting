import sys
from collections import namedtuple
import numpy as np
import cv2
import time
start_time = time.time()
sys.stdout.flush()
count_object=0
Detection = namedtuple("Detection", ["image_path", "gt", "pred"])
face_cascade = cv2.CascadeClassifier('cascade.xml')
#151512neg.xml : 
#Precision : 30.7871367966%
#Recall : 51.1606245932%
#F-measure : 0.384412977545

#1515LBP12neg.xml : 
#Precision : 33.4039847892%
#Recall : 52.229436018%
#F-measure : 0.407474387885

#1515fullneg.xml :
#Precision : 28.4640250043%
#Recall : 50.8505779029%
#F-measure : 0.364979982968

#1515newHaar12neg.xml : 


# define the `Detection` object
#Detection = namedtuple("Detection", ["image_path", "gt", "pred"]) 
def bb_intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])#----------------------------------------------
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

todo=0
dim = (800,800)
sumPrecision = 0
sumRecall = 0
count_line=0
#open file
with open("test2.txt") as f:
	#loop through each line in location.txt
	for line in f:
		list = []
		count_line+=1
		i=0
		#break line (after each space) ex: 1.JPG numObject x11 y11 x12 y12 x21 y21 x22 y22 into element ["1.JPG","numObject",...]
		for token in line.split():
			list.append(token)#add element in the end of list

		input_true = []
		predPositive=0
		truePositive=0
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
		img = cv2.imread("hope6Crop/"+str(list[0]))
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		cropGray = gray[300:np.size(gray,0),0:np.size(gray,1)]
		faces = face_cascade.detectMultiScale(cropGray, 1.05, 5,minSize=(20,20),maxSize=(66,60))
		tempInputTrue = 0
		#cv2.rectangle(frame,(0,300),(1920,300),(0,255,0),2) 
		#cropGray = gray[245:np.size(gray,0),0:np.size(gray,1)]
		count_match=0
		for i in xrange(1,int(numObject)+1):
			#print i
			count_object+=1
			x11=int(input_true[tempInputTrue])
			x12=int(input_true[tempInputTrue+1])
			x21=int(input_true[tempInputTrue])+int(input_true[tempInputTrue+2])
			x22=int(input_true[tempInputTrue+3])+int(input_true[tempInputTrue+1])
			#----------
			#cv2.rectangle(img,(x11,x12),(x21,x22),(0,255,0),2)
			#loop through each predicted faces
			predPositive=0
			for (x,y,w,h) in faces:
				predPositive+=1
				cv2.rectangle(cropGray,(x,y),(x+w,y+h),(255,0,0),2)
				Detection.gt = [x11,x12,x21,x22]
				Detection.pred = [x,y+300,x+w,y+h+300]
				#cv2.rectangle(img,(x11,x12),(x21,x22),(0,255,0),2)
			#	check overlap if do -> calculate iou
				if doOverlap(x11,x12,x21,x22,x,y+300,x+w,y+h+300):
					iou = bb_intersection_over_union(Detection.gt,Detection.pred)
					#match if iou>0.5
					if iou>0.5:
						count_match+=1
						#print("iou : "+str(iou))
			#index +4 
			tempInputTrue+=4
		#calculate Precision and Recall
		truePositive=count_match
		if predPositive==0:
			Precision=0
		else : 
			Precision = truePositive / float(predPositive)
		Recall = truePositive / float(numObject)
		sumRecall+=Recall
		sumPrecision+=Precision
		print("Precision : {}/{} = {}%".format(truePositive,predPositive,Precision*100))
		print("Recall : {}/{} = {}%".format(truePositive,numObject,Recall*100))
		print ""
		#--------------
		#cv2.putText(img, "{} objects".format(i), (10, 30),
		#	cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 2)
		resized = cv2.resize(cropGray, dim, interpolation = cv2.INTER_AREA)
		#cv2.imshow("frame",resized)
		cv2.waitKey(1)
		#cv2.destroyAllWindows()
		#--------------
sumPrecision=sumPrecision/count_line
sumRecall=sumRecall/count_line
if (sumPrecision+sumRecall)==0:
	F_measure=0
else:
	F_measure = (2*(sumPrecision*sumRecall))/(sumPrecision+sumRecall)
print("Precision : "+str(sumPrecision*100)+"%")
print("Recall : "+str(sumRecall*100)+"%")
print("F-measure : "+str(F_measure))
print(count_line)
print(count_object)
print("--- %s seconds ---" % (time.time() - start_time))