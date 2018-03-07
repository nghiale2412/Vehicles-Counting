# Implemented by Nghia LE
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets  import RectangleSelector
from pylab import *
import cv2

# mouse event on crop image 
def line_select_callback(eclick, erelease):
	global x1,x2,y1,y2,w,h
	x1, y1 = eclick.xdata, eclick.ydata
	x2, y2 = erelease.xdata, erelease.ydata
	h = y2 - y1
	w = x2 - x1
	global coord
	coord = (int(x1//1),int(y1//1),int(w//1),int(h//1))

# mouse event on original image
def line_select_callback1(eclick1, erelease1):
	global x3,x4,y3,y4
	x3, y3 = eclick1.xdata, eclick1.ydata
	x4, y4 = erelease1.xdata, erelease1.ydata

# event for original image
def toggle_selector1(event):
	print '*** Key pressed in original plot'
	if event.key in ['X','x'] and toggle_selector1.RS.active:
		print '-> Zoomed selected area'
		# show cropped image in another figure
		plt.figure('crop')
		plt.axis([int(x3),int(x4),int(y4),int(y3)])
		axis = subplot(111)
		plt.imshow(image)
		toggle_selector.RS = RectangleSelector(axis, line_select_callback,
					   drawtype='box',useblit=False, button=[1], 
					   minspanx=5, minspany=5, spancoords='pixels', 
					   interactive=True, rectprops= dict(edgecolor= 'blue',alpha=2,fill=False))
		connect('key_press_event', toggle_selector)
		plt.show()

	if event.key in ['Q','q'] and toggle_selector1.RS.active:
		global numObject
		realNumObject = str(numObject-1)
		print 'Object of the image:',realNumObject
		f.write('\n------NumberofObject: ' + realNumObject +'\n')
		plt.close()
			
# event for crop image
def toggle_selector(event):
	print '*** Key pressed in cropped plot'
	if event.key in ['D','d'] and toggle_selector.RS.active:
		global numObject
		numObject = numObject + 1
		print coord
		mycoord = str(coord)
		mycoord = mycoord.replace("(",'')
		mycoord = mycoord.replace(")",'')
		mycoord = mycoord.replace("'",'')
		mycoord = mycoord.replace(",",'')
		f.write(mycoord + ' ')
		print '-> Coordinate has been recorded to file.'
		ax.add_patch(patches.Rectangle((int(x1),int(y1)),x2-x1,y2-y1,fill=False,edgecolor = 'blue'))

	if event.key in ['Z','z'] and toggle_selector1.RS.active:
		print '-> Close crop image'
		plt.close()



f=open('labeled.csv','w')
temp = 214
while temp<=280:
	numObject = 1
	f.write(str(temp) + '.jpg' + ' ')
	# load image 
	image = cv2.imread('new/'+str(temp)+'.jpg')
	# convert it to RGB into to show image with matplotlib
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	plt.figure(str(temp))
	ax = subplot(111)
	plt.imshow(image,aspect='auto')
	#height = np.size(image, 0)
	#width = np.size(image, 1)
	toggle_selector1.RS = RectangleSelector(ax, line_select_callback1,
					   drawtype='box',useblit=False, button=[1], 
					   minspanx=5, minspany=5, spancoords='pixels', 
					   interactive=True, rectprops= dict(edgecolor= 'red',alpha=2,fill=False))
	connect('key_press_event', toggle_selector1)
	plt.show()
	temp = temp + 3
