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
import math
import os

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


	# cyclically permute the points in the list until the leftmost point is first
	def rotatePointsList(self, points, startPoint):
		'''If the starting point is not the first point in the list, rotate the list until it is'''
		if points[0] != startPoint:
			while points[0] != startPoint:
				points.append(points.pop(0))

		return points


	# finds the point with the smallest x value
	def leftMostPoint(self, points):
		'''Returns the leftmost point in a list of points'''
		left_point = points[0]
		for point in points:
			if point.x() < left_point.x():
				left_point = point

		return left_point


	# finds the point with the largest x value
	def rightMostPoint(self, points):
		'''Returns the rightmost point in a list of points'''
		right_point = points[0]
		for point in points:
			if point.x() > right_point.x():
				right_point = point

		return right_point

	# divide-and-conquer algorithm for finding the convex hull; recursively descends until there is only one point left, then merges the hulls;
	# performed in O(nlogn) time, with a branching factor of 2 and a depth of logn, as well as a recombination step of O(n), where n is the number of points
	def hull_solver(self, points):
		if len(points) == 1:
			return points

		left = self.hull_solver(points[:len(points) // 2])
		right = self.hull_solver(points[len(points) // 2:])

		# upper tangent
		upper_tangent = self.find_tangent(left, right, True)

		# lower tangent
		lower_tangent = self.find_tangent(left, right, False)

		return self.merge(left, right, upper_tangent, lower_tangent)


	# finds upper/lower tangents by comparing slopes of lines between points, starting with the rightmost/leftmost points of the hulls;
	# performed in O(n) time, where n is the number of points in the hulls being compared
	def find_tangent(self, left_hull, right_hull, upper):
		start_left_hull = self.rightMostPoint(left_hull)
		start_right_hull = self.leftMostPoint(right_hull)
		start_line = QLineF(start_left_hull, start_right_hull)
		slope = start_line.dy() / start_line.dx()
		done = False

		# if we find a point with a steeper slope, we update the start point and continue
		while not done:
			done = True

			# if we are finding the upper tangent, we want to find the point with the steepest slope
			if upper:
				for point in right_hull:
					temp = QLineF(start_left_hull, point)
					if temp.dy() / temp.dx() > slope:
						slope = temp.dy() / temp.dx()
						start_right_hull = point
						done = False
				
				for point in left_hull:
					temp = QLineF(start_right_hull, point)
					if temp.dy() / temp.dx() < slope:
						slope = temp.dy() / temp.dx()
						start_left_hull = point
						done = False
			
			# if we are finding the lower tangent, we want to find the point with the shallowest slope
			else:
				for point in right_hull:
					temp = QLineF(start_left_hull, point)
					if temp.dy() / temp.dx() < slope:
						slope = temp.dy() / temp.dx()
						start_right_hull = point
						done = False
				
				for point in left_hull:
					temp = QLineF(start_right_hull, point)
					if temp.dy() / temp.dx() > slope:
						slope = temp.dy() / temp.dx()
						start_left_hull = point
						done = False
		
		return [start_left_hull, start_right_hull]


	# merges the hulls by removing the inner points;
	# performed in O(n) time, where n is the number of points in the hulls being merged
	def merge(self, left_hull, right_hull, upper_tangent, lower_tangent, final=False):
		merged_hull = []
		upper_tangent_left = upper_tangent[0]
		upper_tangent_right = upper_tangent[1]
		lower_tangent_left = lower_tangent[0]
		lower_tangent_right = lower_tangent[1]
		
		# remove inner points from left hull
		left_hull = self.rotatePointsList(left_hull, upper_tangent_left)
		lower_left_point = None
		for i in range(len(left_hull)):
			if left_hull[i] != lower_tangent_left:
				pass
			else:
				lower_left_point = i
				break
		left_hull = left_hull[:lower_left_point + 1]
		
		merged_hull.extend(left_hull)

		# remove inner points from right hull
		right_hull = self.rotatePointsList(right_hull, lower_tangent_right)
		upper_right_point = None
		for i in range(len(right_hull)):
			if right_hull[i] != upper_tangent_right:
				pass
			else:
				upper_right_point = i
				break
		right_hull = right_hull[:upper_right_point + 1]

		merged_hull.extend(right_hull)

		return merged_hull


# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull(self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		# Write points out to a txt file
		# pointsFilePath = os.path.join(os.path.dirname(__file__), 'points.txt')
		# with open(pointsFilePath, 'w') as f:
		# 	for point in points:
		# 		f.write(f"{point.x()} {point.y()}\n")

		t1 = time.time()
		# TODO: SORT THE POINTS BY INCREASING X-VALUE
		# sorts the array of points by x value, with lower x values first;
		# performed in O(nlogn) time (https://stackoverflow.com/questions/14434490/what-is-the-complexity-of-the-sorted-function)
		points = sorted(points, key=lambda point: point.x())
		t2 = time.time()

		t3 = time.time()
		polygon_points = self.hull_solver(points)
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		polygon = [QLineF(polygon_points[i], polygon_points[(i + 1) % len(polygon_points)]) for i in range(len(polygon_points))]
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,BLUE)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
