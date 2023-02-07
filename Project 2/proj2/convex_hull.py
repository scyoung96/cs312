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

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = .25

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







	def rotatePointsList(self, points, startPoint):
		'''If the starting point is not the first point in the list, rotate the list until it is'''
		if points[0] != startPoint:
			while points[0] != startPoint:
				points.append(points.pop(0))

		return points


	def leftMostPoint(self, points):
		'''Returns the leftmost point in a list of points'''
		left_point = points[0]
		for point in points:
			if point.x() < left_point.x():
				left_point = point

		return left_point


	def rightMostPoint(self, points):
		'''Returns the rightmost point in a list of points'''
		right_point = points[0]
		for point in points:
			if point.x() > right_point.x():
				right_point = point

		return right_point


	def sortPointsCounterclockwise(self, points, startingPoint=None):
		"""Sorts a list of points counterclockwise from a given starting point. If no starting point is specified, the
		rightmost point is used."""
		if startingPoint is None:
			startingPoint = self.rightMostPoint(points)

		# Draw a line to every other point and sort by the slope of the line
		points.sort(key=lambda point: math.atan2(point.y() - startingPoint.y(), point.x() - startingPoint.x()))

		# If the starting point is not the first point, rotate the list until it is
		points = self.rotatePointsList(points, startingPoint)

		return points


	def sortPointsClockwise(self, points, startingPoint=None):
		"""Sorts a list of points clockwise from a given starting point. If no starting point is specified, the
		leftmost point is used."""
		if startingPoint is None:
			startingPoint = self.leftMostPoint(points)

		# Draw a line to every other point and sort by the slope of the line
		points.sort(key=lambda point: math.atan2(point.y() - startingPoint.y(), point.x() - startingPoint.x()), reverse=True)

		# If the starting point is not the first point, rotate the list until it is
		points = self.rotatePointsList(points, startingPoint)

		return points


	# self written hull solver
	def hull_solver(self, left, right):
		# when 3 or less points remain on each side
		if len(left) < 4 and len(right) < 4:
			left_hull = []
			right_hull = []

			if len(left) == 3:
				for i in range(len(left)):
					left_hull.append(QLineF(left[i], left[(i+1)%len(left)]))
			elif len(left) == 2:
				left_hull.append(QLineF(left[0], left[1]))
			else:
				pause = 1

			if len(right) == 3:	
				for i in range(len(right)):
					right_hull.append(QLineF(right[i], right[(i+1)%len(right)]))
			elif len(right) == 2:
				right_hull.append(QLineF(right[0], right[1]))
			else:
				pause = 1

			left_sorted = self.sortPointsCounterclockwise(left)
			right_sorted = self.sortPointsClockwise(right)

			# upper tangent
			left_upper_tangent = self.find_tangent(left_sorted, right_sorted, True, True)
			right_upper_tangent = self.find_tangent(left_sorted, [left_upper_tangent.p2()], True, False)
			upper_tangent = self.find_tangent([right_upper_tangent.p1()], right_sorted, True, True)
			self.blinkTangent([upper_tangent], RED)

			left_sorted = self.sortPointsClockwise(left)
			right_sorted = self.sortPointsCounterclockwise(right)

			# lower tangent
			left_lower_tangent = self.find_tangent(left_sorted, right_sorted, False, True)
			right_lower_tangent = self.find_tangent(left_sorted, [left_lower_tangent.p2()], False, False)
			lower_tangent = self.find_tangent([right_lower_tangent.p1()], right_sorted, False, True)
			self.blinkTangent([lower_tangent], GREEN)

			if (upper_tangent.p1() == lower_tangent.p1()):
				left_hull = [i for i in left_hull if i.p1() != upper_tangent.p1()]
			elif (upper_tangent.p2() == lower_tangent.p2()):
				right_hull = [i for i in right_hull if i.p2() != upper_tangent.p2()]

			return self.merge(left_hull, right_hull, upper_tangent, lower_tangent)

		# continue to recurse
		else:
			left_hull = self.hull_solver(left[:len(left) // 2], left[len(left) // 2:])
			self.showHull(left_hull, RED)
			right_hull = self.hull_solver(right[:len(right) // 2], right[len(right) // 2:])
			self.showHull(right_hull, GREEN)

			left_hull_points = []
			for i in range(len(left_hull)):
				if left_hull[i].p1() not in left_hull_points:
					left_hull_points.append(left_hull[i].p1())
			for i in range(len(left_hull)):
				if left_hull[i].p2() not in left_hull_points:
					left_hull_points.append(left_hull[i].p2())

			right_hull_points = []
			for i in range(len(right_hull)):
				if right_hull[i].p1() not in right_hull_points:
					right_hull_points.append(right_hull[i].p1())
			for i in range(len(right_hull)):
				if right_hull[i].p2() not in right_hull_points:
					right_hull_points.append(right_hull[i].p2())

			left_sorted = self.sortPointsCounterclockwise(left_hull_points)
			right_sorted = self.sortPointsClockwise(right_hull_points)

			# upper tangent
			left_upper_tangent = self.find_tangent(left_sorted, right_sorted, True, True)
			right_upper_tangent = self.find_tangent(left_sorted, [left_upper_tangent.p2()], True, False)
			upper_tangent = self.find_tangent([right_upper_tangent.p1()], right_sorted, True, True)
			self.blinkTangent([upper_tangent], RED)

			# lower tangent
			left_lower_tangent = self.find_tangent(left_sorted, right_sorted, False, True)
			right_lower_tangent = self.find_tangent(left_sorted, [left_lower_tangent.p2()], False, False)
			lower_tangent = self.find_tangent([right_lower_tangent.p1()], right_sorted, False, True)
			self.blinkTangent([lower_tangent], GREEN)

			return self.merge(left_hull, right_hull, upper_tangent, lower_tangent)

	# self written tangent finder
	def find_tangent(self, left_hull, right_hull, upper, left):
		if upper:
			if left:
				left_tangent = QLineF(left_hull[0], right_hull[0])
				for i in range(len(right_hull)):
					if left_tangent.dy() / left_tangent.dx() < QLineF(left_hull[0], right_hull[i]).dy() / QLineF(left_hull[0], right_hull[i]).dx():
						left_tangent = QLineF(left_hull[0], right_hull[i])
				return left_tangent
			else:
				right_tangent = QLineF(left_hull[0], right_hull[0])
				for i in range(len(left_hull)):
					if right_tangent.dy() / right_tangent.dx() > QLineF(left_hull[i], right_hull[0]).dy() / QLineF(left_hull[i], right_hull[0]).dx():
						right_tangent = QLineF(left_hull[i], right_hull[0])
				return right_tangent
		else:
			if left:
				left_tangent = QLineF(left_hull[0], right_hull[0])
				for i in range(len(right_hull)):
					if left_tangent.dy() / left_tangent.dx() > QLineF(left_hull[0], right_hull[i]).dy() / QLineF(left_hull[0], right_hull[i]).dx():
						left_tangent = QLineF(left_hull[0], right_hull[i])
				return left_tangent
			else:
				right_tangent = QLineF(left_hull[0], right_hull[0])
				for i in range(len(left_hull)):
					if right_tangent.dy() / right_tangent.dx() < QLineF(left_hull[i], right_hull[0]).dy() / QLineF(left_hull[i], right_hull[0]).dx():
						right_tangent = QLineF(left_hull[i], right_hull[0])
				return right_tangent


	# self written hull merger
	def merge(self, left_hull, right_hull, upper_tangent, lower_tangent):
		merged_hull = []
		upper_tangent_left = upper_tangent.p1()
		upper_tangent_right = upper_tangent.p2()
		lower_tangent_left = lower_tangent.p1()
		lower_tangent_right = lower_tangent.p2()
		slope = lambda p1, p2: math.atan2(p2.y() - p1.y(), p2.x() - p1.x())
		
		left_remove = []
		remove_tangent_link = False
		remove_others = False
		if len(left_hull) > 2:
			for i in range(len(left_hull)):
				p1 = left_hull[i].p1()
				p2 = left_hull[i].p2()

				if i == 0:
					# lower, non, upper
					if ((p1 == lower_tangent_left) and (p2 != upper_tangent_left)):
						if slope(upper_tangent_left, p1) > slope(p2, p1):
							left_remove.append(i)
							remove_others = True
						else:
							remove_tangent_link = True

					# lower, upper, non
					elif ((p1 == lower_tangent_left) and (p2 == upper_tangent_left)):
						remove_others = True

					# upper, lower, non
					elif ((p1 == upper_tangent_left) and (p2 == lower_tangent_left)):
						remove_others = True

					# upper, non, lower
					elif ((p1 == upper_tangent_left) and (p2 != lower_tangent_left)):
						if slope(lower_tangent_left, p1) < slope(p2, p1):
							left_remove.append(i)
							remove_others = True
						else:
							remove_tangent_link = True

					# non, lower, upper
					elif ((p1 != lower_tangent_left) and (p2 == lower_tangent_left)):
						remove_tangent_link = True

					# non, upper, lower
					elif ((p1 != upper_tangent_left) and (p2 == upper_tangent_left)):
						remove_tangent_link = True


				elif remove_tangent_link:
					if ((p1 == lower_tangent_left) and (p2 == upper_tangent_left)) or ((p1 == upper_tangent_left) and (p2 == lower_tangent_left)):
						left_remove.append(i)
				
				elif remove_others:
					if ((p1 == lower_tangent_left) and (p2 != upper_tangent_left)) or ((p1 == upper_tangent_left) and (p2 != lower_tangent_left)):
						pass
					else:
						left_remove.append(i)

			left_hull = [i for j, i in enumerate(left_hull) if j not in left_remove]
		
		merged_hull.extend(left_hull)

		right_remove = []
		remove_tangent_link = False
		remove_others = False
		if len(right_hull) > 2:
			for i in range(len(right_hull)):
				p1 = right_hull[i].p1()
				p2 = right_hull[i].p2()

				if i == 0:
					# lower, non, upper
					if ((p1 == lower_tangent_right) and (p2 != upper_tangent_right)):
						if slope(upper_tangent_right, p1) > slope(p2, p1):
							remove_tangent_link = True
						else:
							right_remove.append(i)
							remove_others = True

					# lower, upper, non
					elif ((p1 == lower_tangent_right) and (p2 == upper_tangent_right)):
						right_remove.append(i)

					# upper, lower, non
					elif ((p1 == upper_tangent_right) and (p2 == lower_tangent_right)):
						right_remove.append(i)

					# upper, non, lower
					elif ((p1 == upper_tangent_right) and (p2 != lower_tangent_right)):
						if slope(lower_tangent_right, p1) < slope(p2, p1):
							remove_tangent_link = True
						else:
							right_remove.append(i)
							remove_others = True

					# non, lower, upper
					elif ((p1 != lower_tangent_right) and (p2 == lower_tangent_right)):
						right_remove.append(i)
						remove_others = True

					# non, upper, lower
					elif ((p1 != upper_tangent_right) and (p2 == upper_tangent_right)):
						right_remove.append(i)
						remove_others = True


				elif remove_tangent_link:
					if ((p1 == lower_tangent_right) and (p2 == upper_tangent_right)) or ((p1 == upper_tangent_right) and (p2 == lower_tangent_right)):
						right_remove.append(i)
				
				elif remove_others:
					if ((p1 == lower_tangent_right) and (p2 == upper_tangent_right)) or ((p1 == upper_tangent_right) and (p2 == lower_tangent_right)):
						pass
					else:
						right_remove.append(i)

			right_hull = [i for j, i in enumerate(right_hull) if j not in right_remove]

		merged_hull.extend(right_hull)

		merged_hull.append(upper_tangent)
		merged_hull.append(lower_tangent)

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
		initial_left = points[:len(points) // 2]
		initial_right = points[len(points) // 2:]
		polygon = self.hull_solver(initial_left, initial_right)
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,BLUE)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
