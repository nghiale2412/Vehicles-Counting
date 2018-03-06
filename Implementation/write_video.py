import cv2
import numpy as np
 
# Create a VideoCapture object
cap = cv2.VideoCapture("IMG_6391.MOV")
 

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
 
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('video_with_retangle2.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 12, (frame_width,frame_height))
face_cascade = cv2.CascadeClassifier('test.xml')
dim = (960,540)
while(cap.isOpened()):
  ret, frame = cap.read()
 
  if ret == True: 

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    #faces = face_cascade.detectMultiScale(gray, 1.005, 15)
    # Write the frame into the file 'output.avi'
#    for (x,y,w,h) in faces:
#        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    # Display the resulting frame    
    #out.write(frame)
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow('frame',resized) 
    # Press Q on keyboard to stop recording
    if cv2.waitKey(83) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else:
    break 
 
# When everything done, release the video capture and video write objects
cap.release()
out.release()
 
# Closes all the frames
cv2.destroyAllWindows() 