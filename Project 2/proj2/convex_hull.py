from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False

# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseHull(self,polygon):
		self.view.clearLines(polygon)

	def showText(self,text):
		self.view.displayStatusText(text)


	# self written hull solver
	def hull_solver(left, right):
		if len(left) == 2 and len(right) == 2:
			return [QLineF(left[0], right[0]), QLineF(left[1], right[1]), QLineF(left[0], left[1])]
		else:
			left_hull = ConvexHullSolver.hull_solver(left[:len(left) // 2], left[len(left) // 2:])
			right_hull = ConvexHullSolver.hull_solver(right[:len(right) // 2], right[len(right) // 2:])
			left_tangent = ConvexHullSolver.find_tangent(left_hull, right_hull, True)
			right_tangent = ConvexHullSolver.find_tangent(left_hull, right_hull, False)
			ConvexHullSolver.blinkTangent(left_tangent, RED)
			return ConvexHullSolver.merge(left_hull, right_hull)

	# self written tangent finder
	def find_tangent(left_hull, right_hull, left):
		if left:
			left_tangent = QLineF(left_hull[0].p1(), right_hull[0].p1())
			for i in range(len(left_hull)):
				for j in range(len(right_hull)):
					if left_tangent.length() < QLineF(left_hull[i].p1(), right_hull[j].p1()).length():
						left_tangent = QLineF(left_hull[i].p1(), right_hull[j].p1())
			return left_tangent
		else:
			right_tangent = QLineF(left_hull[0].p2(), right_hull[0].p2())
			for i in range(len(left_hull)):
				for j in range(len(right_hull)):
					if right_tangent.length() < QLineF(left_hull[i].p2(), right_hull[j].p2()).length():
						right_tangent = QLineF(left_hull[i].p2(), right_hull[j].p2())
			return right_tangent

	# self written hull merger
	def merge(left_hull, right_hull, left_tangent, right_tangent):
		left_index = 0
		right_index = 0
		for i in range(len(left_hull)):
			if left_hull[i] == left_tangent:
				left_index = i
		for i in range(len(right_hull)):
			if right_hull[i] == right_tangent:
				right_index = i
		merged_hull = []
		for i in range(left_index, left_index + len(left_hull)):
			merged_hull.append(left_hull[i % len(left_hull)])
		for i in range(right_index, right_index + len(right_hull)):
			merged_hull.append(right_hull[i % len(right_hull)])
		return merged_hull


# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull(self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		# TODO: SORT THE POINTS BY INCREASING X-VALUE
		points = sorted(points, key=lambda point: point.x())
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		# polygon = [QLineF(points[i],points[(i+1)%3]) for i in range(3)]
		polygon = ConvexHullSolver.hull_solver(points[:len(points) // 2], points[len(points) // 2:])
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
