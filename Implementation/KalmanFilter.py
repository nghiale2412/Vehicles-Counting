#--------------------------------------------------------------------
# Implements Ball motion prediction using Kalman Filter
#
# Author: Sriram Emarose [sriram.emarose@gmail.com]
#
#
#
#--------------------------------------------------------------------

import cv2 as cv
import numpy as np
face_cascade = cv.CascadeClassifier('hopeCascade/cascade.xml')
# Instantiate OCV kalman filter
dim = (960,540)
class KalmanFilter:

	kf = cv.KalmanFilter(4, 2)
	kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
	kf.transitionMatrix = np.array([[1, 0, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1]], np.float32)

	def Estimate(self, coordX, coordY):
		''' This function estimates the position of the object'''
		measured = np.array([[np.float32(coordX)], [np.float32(coordY)]])
		self.kf.correct(measured)
		predicted = self.kf.predict()
		return predicted



#Performs required image processing to get ball coordinated in the video
class ProcessImage:

	def DetectObject(self):

		vid = cv.VideoCapture('IMG_6391.MOV')

		if(vid.isOpened() == False):
			print('Cannot open input video')
			return

		width = int(vid.get(3))
		height = int(vid.get(4))

		# Create Kalman Filter Object
		kfObj = KalmanFilter()
		predictedCoords = np.zeros((2, 1), np.float32)

		while(vid.isOpened()):
			rc, frame = vid.read()

			gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
			gray = cv.GaussianBlur(gray,(5,5),0)
			faces = face_cascade.detectMultiScale(gray, 1.1, 5)
			for (x,y,w,h) in faces:
				ballX = x+w/2
				ballY = y+h/2
				predictedCoords = kfObj.Estimate(ballX, ballY)
				cv.circle(frame, (ballX, ballY), 20, [0,0,255], 2, 8)
				cv.line(frame,(ballX, ballY + 20), (ballX + 50, ballY + 20), [100,100,255], 2,8)
				cv.putText(frame, "Actual", (ballX + 50, ballY + 20), cv.FONT_HERSHEY_SIMPLEX,0.5, [50,200,250])

					# Draw Kalman Filter Predicted output
				cv.circle(frame, (predictedCoords[0], predictedCoords[1]), 20, [0,255,255], 2, 8)
				cv.line(frame, (predictedCoords[0] + 16, predictedCoords[1] - 15), (predictedCoords[0] + 50, predictedCoords[1] - 30), [100, 10, 255], 2, 8)
				cv.putText(frame, "Predicted", (predictedCoords[0] + 50, predictedCoords[1] - 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, [50, 200, 250])
			if cv.waitKey(1) & 0xFF == ord("q"):
				break
			resized = cv.resize(frame,dim,interpolation = cv.INTER_AREA)
			cv.imshow('Input', resized)
			cv.waitKey(1)
				
			
		vid.release()
		cv.destroyAllWindows()

def main():
	processImg = ProcessImage()
	processImg.DetectObject()


if __name__ == "__main__":
	main()
print('Program Completed!')