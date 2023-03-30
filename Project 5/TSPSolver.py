from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

from colorize import *
import StateGraph

import time
import numpy as np
from TSPClasses import *
import heapq
import itertools


class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution,
		time spent to find solution, number of permutations tried during search, the
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def defaultRandomTour(self, time_allowance=60.0):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def greedy(self,time_allowance=60.0):
		results = {}
		cities = self._scenario.getCities()
		route = []
		
		start_time = time.time()
		
		# Start at the first city
# FIXME: assuming start city is first city in list
		route.append(cities[0])
		currCityIndex = 0

		# Create a list of the remaining cities
		remaining_cities = cities.copy()
# FIXME: if previous fixme is changed (ie start city is not first in list), update this ref as well
		remaining_cities.remove(cities[0])

		# Loop through the remaining cities
		while len(remaining_cities) > 0:
			# Find the closest city
			closest_city = None
			closest_distance = math.inf
			for city in remaining_cities:
				distance = route[currCityIndex].costTo(city)
				if distance < closest_distance:
					closest_city = city
					closest_distance = distance

			# Add the closest city to the route
			route.append(closest_city)
			remaining_cities.remove(closest_city)
			currCityIndex += 1

		bssf = TSPSolution(route)

		end_time = time.time()
		results['cost'] = bssf.cost
		results['time'] = end_time - start_time
		results['count'] = 0
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results



	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''

	def branchAndBound(self,time_allowance=60.0):
		cities = self._scenario.getCities()
		ncities = len(cities)

		results = {}

		bssf = self.greedy(self, time_allowance)['soln']
		cost = bssf['cost']
		count = 0
		max_queue_size = 0
		total_states = 0
		pruned_states = 0

		# Create a priority queue
		from queue import PriorityQueue
		pq = PriorityQueue()

		# Create the initial StateGraph
		state_graph = StateGraph(cities, bssf)

		# Add the initial state to the priority queue
		pq.put((state_graph.lower_bound, state_graph))

		start_time = time.time()

		while not pq.empty() and time.time() - start_time <= time_allowance:
			# Get the next state
			next_state_graph = pq.get()
			state_graph_lower_bound = next_state_graph[0]
			state_graph = next_state_graph[1]

			# Check if the state is a solution
			if state_graph.is_solution():
				# Check if the state is better than the current best solution
				if state_graph.bssf.cost < cost:
					# Update the best solution
					bssf = state_graph.bssf
					cost = bssf.cost()
					count += 1
			else:
				# Expand the state
				children = state_graph.get_partial_paths()

				# Add the children to the priority queue
				for child in children:
					pq.put((child.lower_bound, child))

			# Update the stats
			if pq.qsize() > max_queue_size:
				max_queue_size = pq.qsize()
			total_states += 1
			pruned_states += state_graph.pruned_states_count



		




	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found during search, the
		best solution found.  You may use the other three field however you like.
		algorithm</returns>
	'''

	def fancy(self,time_allowance=60.0):
		pass
