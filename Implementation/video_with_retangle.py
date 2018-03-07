import cv2
import numpy as np 
import time
start_time = time.time()
maxw=0
maxh=0
minw=100
minh=100
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
face_cascade = cv2.CascadeClassifier('test.xml')
count_line=0
out = cv2.VideoWriter('video_with_retangle.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 4, (800,450))
count_object=0
with open("location.txt") as f:
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
						count_object+=int(numObject)
					else:
						input_true.append(list[i])#add coor in end of list
				else:
					path=list[i]#path = path name
					print "image path : "+path
			finally:
				i+=1
		img = cv2.imread("new_withcolour/"+str(list[0]))
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.1, 5)
		tempInputTrue = 0
		for i in xrange(1,int(numObject)+1):
			#print i
			x11=int(input_true[tempInputTrue])
			x12=int(input_true[tempInputTrue+1])
			x21=int(input_true[tempInputTrue])+int(input_true[tempInputTrue+2])
			x22=int(input_true[tempInputTrue+3])+int(input_true[tempInputTrue+1])
			#----------
			#print i
			#print"w = {}".format(input_true[tempInputTrue+2])
			#print "h = {}".format(input_true[tempInputTrue+3])
			#cau lenh if o day de tim ra object co w va h max, cung voi w va h min
			if maxw<int(input_true[tempInputTrue+2]):
				print"max w from {} to {}".format(maxw,input_true[tempInputTrue+2])
				maxw=int(input_true[tempInputTrue+2])

			if maxh<int(input_true[tempInputTrue+3]):
				print"max h from {} to {}".format(maxh,input_true[tempInputTrue+3])
				maxh=int(input_true[tempInputTrue+3])

			if minw>int(input_true[tempInputTrue+2])&int(input_true[tempInputTrue+2])>0:
				print"min w from {} to {}".format(minw,input_true[tempInputTrue+2])
				minw=int(input_true[tempInputTrue+2])

			if minh>int(input_true[tempInputTrue+3])&int(input_true[tempInputTrue+3])>0:
				print"min h from {} to {}".format(minh,input_true[tempInputTrue+3])
				minh=int(input_true[tempInputTrue+3])

			cv2.rectangle(img,(x11,x12),(x21,x22),(0,255,0),2)
			tempInputTrue+=4
			#loop through each predicted faces
			#--------------
		#out.write(img)
		cv2.rectangle(img,(0,300),(799,300),(0,255,0),1)
		cv2.imshow("frame",img)
		cv2.waitKey(2)
		print "maxw = {}".format(maxw)
		print "maxh = {}".format(maxh)
		print "minw = {}".format(minw)
		print "minh = {}".format(minh)
		#cv2.destroyAllWindows()
		#--------------
print list
print count_object
print("--- %s seconds ---" % (time.time() - start_time))