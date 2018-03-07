class headCoordinator:
	name =""
	x=0
	y=0
	w=0
	h=0
	def __init__(self, name, x, y, w ,h):
		self.name = name
		self.x = x
		self.y = y
		self.w = w
		self.h = h
head1 = headCoordinator("object1",30,10,10,10)
head2 = headCoordinator("object2",15,20,20,20)
listO = []
listO.append(head1)
listO.append(head2)
for x in listO:
	print(x.x)
for x in listO:
	if x.x==30:
		print("kk")
		listO.remove(x)
for x in listO:
	print(x.x)
