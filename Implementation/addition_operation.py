import numpy as np
import cv2
#save a frame to image, calculate fps and total frames
cap = cv2.VideoCapture("IMG_6391.MOV")
while (cap.isOpened()):
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	count_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
	int_count = int(count_frame)
	cv2.rectangle(frame,(0,300),(1920,300),(0,255,0),2)
	cv2.imwrite("hope6Crop/{}.jpg".format(int_count),frame)
	
	#cv2.imshow("frame", frame)
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break
	#cv2.destroyAllWindows()
	
	cv2.waitKey(1)
 	cap.set(cv2.CAP_PROP_POS_FRAMES, count_frame+2) 
width=cap.get(3)
height=cap.get(4)
#total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
#fps_count = cap.get(cv2.CAP_PROP_FPS)
cap.release()
#print total_frame
#print fps_count
print width
print height