import cv2
import numpy as np 
import time

# Instantiate OCV kalman filter
start_time = time.time()
#dim = (800,800)
dim = (960,540)
cap = cv2.VideoCapture("IMG_6391.MOV")
face_cascade = cv2.CascadeClassifier('hopeCascade/cascade.xml')
try:
	while (cap.isOpened()):
		ret, frame = cap.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		count_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
		int_count = int(count_frame)
		
		#cv2.imwrite("new/{}.jpg".format(int_count),gray)
		#chi lay truc y tu 180->het ~ 1/3
		cropGray = gray[300:np.size(gray,0),0:np.size(gray,1)]
		faces = face_cascade.detectMultiScale(cropGray, 1.05, 5,minSize=(20,20),maxSize=(66,60))
		i=0
		for (x,y,w,h) in faces:
			cv2.rectangle(frame,(x,y+300),(x+w,y+h+300),(255,0,0),2)
			#    roi_gray = gray[y:y+h, x:x+w]
			#    roi_color = img[y:y+h, x:x+w]
			cv2.putText(frame, "{}".format(i), (x, y - 10 +300),#+180 la dua vao cropGray 180:np.size
				cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
			i+=1
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		cv2.waitKey(1)
		#cap.set(cv2.CAP_PROP_POS_FRAMES, count_frame+2) 
		resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
		cv2.imshow("frame", resized)
finally:
	cap.release()
	cv2.destroyAllWindows()
	print("--- %s seconds ---" % (time.time() - start_time))