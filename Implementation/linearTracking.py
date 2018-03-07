import cv2
from collections import namedtuple
import numpy as np 
import time
#define class head coordinator
Detection = namedtuple("Detection", ["image_path", "gt", "pred"])
class HeadCoordinator:
	name =""
	x=0
	y=0
	w=0
	h=0
	count=0
	existFrame=0
	def __init__(self, name, x, y, w ,h ,count, existFrame):
		self.name = name
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.count = count
		self.existFrame = existFrame

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



# Instantiate OCV kalman filter
start_time = time.time()
#dim = (800,800)
dim = (960,540)
cap = cv2.VideoCapture("IMG_6391.MOV")
#get frame width and height
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
#write video object
out = cv2.VideoWriter('videoLinearTracking.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 12, (960,540))


face_cascade = cv2.CascadeClassifier('hopeCascade/cascade.xml')
listObject = []
countObject=0
try:
	while (cap.isOpened()):
		ret, frame = cap.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		count_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
		int_count = int(count_frame)
		
		#cv2.imwrite("new/{}.jpg".format(int_count),gray)
		#chi lay truc y tu 180->het ~ 1/3
		cropGray = gray[300:np.size(gray,0),0:np.size(gray,1)]
		cropGray = cv2.GaussianBlur(cropGray,(5,5),0)
		faces = face_cascade.detectMultiScale(cropGray, 1.1, 5,minSize=(20,20),maxSize=(66,60))
		
		i=0
		#loop through the whole resultSet
		for (x,y,w,h) in faces:
			ultimateTemp = 0

			#loop through all object in array if overlap then count +1( count is the number of time detected object
			#overlap the older)
			for eachObject in listObject:
				if doOverlap(eachObject.x,eachObject.y,eachObject.x+eachObject.w,eachObject.y+eachObject.h,x,y+h,w+x,h+y+h) or doOverlap(eachObject.x,eachObject.y,eachObject.x+eachObject.w,eachObject.y+eachObject.h,x,y,w+x,h+y):
					eachObject.x=x
					eachObject.y=y
					eachObject.w=w
					eachObject.h=h
					eachObject.count+=1
					ultimateTemp=1
					break;
			
			#add new object in the array if there is no matched object
			#ultimatTemp = 0 that is when there are no old detected object(tracking) -> add new object(tracking) in class
			if ultimateTemp == 0:
				tempHead = HeadCoordinator("Object{}".format(i),x,y,w,h,0,0)
				listObject.append(tempHead)

			#remove object(tracking) that go pass the detecting zone
			for eachObject in listObject:
				if eachObject.y >= 0 and eachObject.y < 50:
					if eachObject.count > 0:
						countObject+=1
					listObject.remove(eachObject)
					print("delete")
			
			#draw retangle for detected objects
			cv2.rectangle(frame,(x,y+300),(x+w,y+h+300),(255,0,0),0)
			#    roi_gray = gray[y:y+h, x:x+w]
			#    roi_color = img[y:y+h, x:x+w]
			#cv2.putText(frame, "{}".format(i), (x, y - 10 +300),#+180 la dua vao cropGray 180:np.size
			#	cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
			i+=1

			#reset 
			x=0
			y=0
			w=0
			h=0
		
		#delete objects(tracking) that are not tracked anymore
		for eachObject in listObject:
			eachObject.existFrame+=1
			if eachObject.existFrame >5 and eachObject.count < eachObject.existFrame -2:
				listObject.remove(eachObject)

		#draw retangle for objects(tracking)
		for eachObject in listObject:
			cv2.rectangle(frame,(eachObject.x,eachObject.y+300),(eachObject.x+eachObject.w,eachObject.y+eachObject.h+300),(0,0,255),0)
			cv2.putText(frame , "{}".format(eachObject.name), (eachObject.x,eachObject.y -10 + 300),
				cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)


		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
		cv2.waitKey(1)
		cv2.putText(frame, "{}".format(countObject), (10,50),#+180 la dua vao cropGray 180:np.size
				cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
			#cap.set(cv2.CAP_PROP_POS_FRAMES, count_frame+2) 
		cv2.rectangle(frame,(0,300),(1920,350),(0,255,0),2)		
		print countObject
		#resize the frame to smaller
		resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
		cv2.imshow("frame", resized)
		
		#write video
		#out.write(resized)
finally:
	#212
	print "final count : " + countObject
	cap.release()
	cv2.destroyAllWindows()
	print("--- %s seconds ---" % (time.time() - start_time))