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
from StateGraph import *

import time
import numpy as np
from TSPClasses import *
from queue import PriorityQueue
from random import randint
from copy import deepcopy


DEBUG = False


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
	# def greedy(self,time_allowance=60.0):
	# 	results = {}
	# 	cities = self._scenario.getCities()
	# 	route = []
	# 	# NOTE: assuming start city is first city in list
	# 	start_city = 0
	# 	bssf = None
		
	# 	start_time = time.time()
		
	# 	while route == []:
	# 		# Start at the first city
	# 		route.append(cities[start_city])
	# 		currCityIndex = 0

	# 		# Create a list of the remaining cities
	# 		remaining_cities = cities.copy()
	# 		remaining_cities.remove(cities[start_city])

	# 		# Loop through the remaining cities
	# 		while len(remaining_cities) > 0:
	# 			# Find the closest city
	# 			closest_city = None
	# 			closest_distance = math.inf
	# 			for city in remaining_cities:
	# 				distance = route[currCityIndex].costTo(city)
	# 				if distance < closest_distance:
	# 					closest_city = city
	# 					closest_distance = distance

	# 			if closest_distance == math.inf:
	# 				break

	# 			# Add the closest city to the route
	# 			route.append(closest_city)
	# 			remaining_cities.remove(closest_city)
	# 			currCityIndex += 1

	# 		# Check if valid tour found
	# 		if route[-1].costTo(route[0]) == math.inf or len(route) != len(cities):
	# 			printc(f"No valid route found (start city: {cities[start_city]._name}, index: {start_city}), trying next city", "red")
	# 			start_city += 1
	# 			if start_city >= len(cities):
	# 				raise Exception("No valid route found starting from any city")
	# 			route = []
	# 			continue

	# 	# Create the BSSF from the route we found
	# 	bssf = TSPSolution(route)

	# 	# Return the results
	# 	end_time = time.time()
	# 	results['cost'] = bssf.cost
	# 	results['time'] = end_time - start_time
	# 	results['count'] = 0
	# 	results['soln'] = bssf
	# 	results['max'] = None
	# 	results['total'] = None
	# 	results['pruned'] = None
	# 	return results


	# GROUP CODE ###########################################################################

	def greedy(self, time_allowance=60.0):
		cities = self._scenario.getCities()

		# make np array of distances
		distances = np.zeros((len(cities), len(cities)))
		for i in range(len(cities)):
			for j in range(len(cities)):
				distances[i][j] = cities[i].costTo(cities[j])
		n = distances.shape[0]


		best_cost = np.inf
		best_path = None


		start_time = time.time()
		for start_city in range(n):
			path = [start_city]
			total_cost = 0


			while len(path) < n:
				if time.time() - start_time > time_allowance:
					break
				current_city = path[-1]
				next_city = None
				min_cost = np.inf


				for city in range(n):
					if city not in path:
						cost = distances[current_city, city]
						if cost < min_cost:
							min_cost = cost
							next_city = city


				if next_city is None:
					# if there is no path to any unvisited city from the current city,
					# start again from a random unvisited city
					unvisited_cities = set(range(n)) - set(path)
					start_city = random.choice(list(unvisited_cities))
					path.append(start_city)
					continue


				path.append(next_city)
				total_cost += min_cost


			if len(path) == n:
				# a complete path was found
				total_cost += distances[path[-1], start_city]


				if total_cost < best_cost:
					best_cost = total_cost
					best_path = path


		end_time = time.time()


		if best_path is not None:
			# convert path to city list
			city_path = [cities[i] for i in best_path]
			bssf = TSPSolution(city_path)
			results = {'cost': int(best_cost), 'time': end_time - start_time, 'count': 1,
						'soln': bssf, 'max': None, 'total': None, 'pruned': None}
		else:
			results = {'cost': np.inf, 'time': end_time - start_time, 'count': 1,
						'soln': None, 'max': None, 'total': None, 'pruned': None}


		return results

	# GROUP CODE ###########################################################################


	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''
	def branchAndBound(self,time_allowance=60.0):
		# Start the timer immediately
		start_time = time.time()

		cities = self._scenario.getCities()
		results = {}
		# Our initial BSSF is found using the greedy algorithm
		bssf = self.greedy(time_allowance)['soln']
		cost = bssf.cost
		count = 0
		max_queue_size = 0
		total_states = 1
		pruned_states = 0

		# Create a priority queue
		pq = PriorityQueue()

		# Create the initial StateGraph (i.e. the initial adjacency matrix)
		state_graph = StateGraph(cities, bssf)

		# Add the initial state to the priority queue (this PQ is sorted by lower bound)
		pq.put((state_graph.lower_bound, state_graph))

		# Continuously loop until the queue is empty or until the time allowance is up
		while not pq.empty() and time.time() - start_time <= time_allowance:
			# Get the next state (the adjacency matrix with the lowest lower bound and deepest depth)
			state_graph = pq.get()[1]

			# If the state has a lower bound greater than the current best solution, prune it
			if state_graph.lower_bound >= cost:
				pruned_states += 1
				continue

			# Check if the state is a solution
			if state_graph.is_solution():
				# Check if the state is better than the current best solution
				if state_graph.bssf.cost < cost:
					# Update the best solution
					bssf = state_graph.bssf
					cost = bssf.cost
					count += 1
			else:
				# Expand the state  (i.e. create children adjacency matrices from the current state)
				children, pruned_states_count = state_graph.get_partial_paths()

				# Add the children to the priority queue, incrementing the total number of states for each child
				for child in children:
					if DEBUG:
						child.print_adj_matrix()
					pq.put((child.lower_bound, child))
					total_states += 1

			# Update the stats
			if pq.qsize() > max_queue_size:
				max_queue_size = pq.qsize()
			pruned_states += pruned_states_count

		# Stop the timer
		end_time = time.time()

		# Add any remaining states with lowerbound >= cost to pruned states
		while pq.qsize() > 0:
			state_graph = pq.get()[1]
			if state_graph.lower_bound >= cost:
				pruned_states += 1

		# Return the results
		results['cost'] = cost
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = max_queue_size
		results['total'] = total_states
		results['pruned'] = pruned_states
		return results


	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found during search, the
		best solution found.  You may use the other three field however you like.
		algorithm</returns>
	'''

	def fancy(self, time_allowance=60.0):
		# These preliminary pieces of code were copied and pasted from the default algorithm
		results = {}
		count = 0
		bssf = None
		start_time = time.time()


		# This default algorithm is used to find the initial BSSF
		while time.time() - start_time < time_allowance:
			bssf = self.greedy(time_allowance)['soln']

			if bssf.cost == np.inf:
				break

			bssf = self.two_opt(bssf.route, bssf.cost, count)
			break


		# Also taken from the default algorithm, returns the results of the algorithm to the GUI
		end_time = time.time()
		results['cost'] = bssf.cost
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		return results


	def two_opt(self, path, cost, count):
		n = len(path)
		improved = True
		while improved:
			improved = False
			for i in range(1, n - 1):
				for j in range(i + 1, n):
					#Copies the path and swaps the edges by swapping the cities i and j
					new_path = deepcopy(path)
					new_path[i:j] = path[j - 1:i - 1:-1]
					new_dist = 0

					for k in range(n):
						new_dist += new_path[k].costTo(new_path[(k + 1) % n])
					if new_dist < cost:
						path = new_path
						cost = new_dist
						count += 1
						improved = True

		path = TSPSolution(path)
		return path


	#Creates the initial matrix using the information from the cities array
	def matrixCreator(self, cities):
		nCities = len(cities)
		toReturn = [[0 for i in range(nCities)] for j in range(nCities)]
		for i in range(nCities):
			for j in range(nCities):
				if (i != j):
					toReturn[i][j] = cities[i].costTo(cities[j])
				else:
					toReturn[i][j] = math.inf
		return toReturn
