import numpy as np
from copy import deepcopy

from colorize import *
from TSPClasses import *

class StateGraph:
    def __init__(self, cities, bssf=None):
        self.cities = cities
        self.num_cities = len(cities)
        self.adj_list = []
        self.adj_matrix = np.zeros((self.num_cities, self.num_cities))
        self.create_adj_list()
        self.create_adj_matrix()
        self.bssf = bssf
        self.lower_bound = 0
        self.row_reduce()
        self.col_reduce()
        self.path = []
        self.depth = 0

    def __lt__(self, other):
        return self.depth < other.depth
    
    def create_adj_list(self):
        for i in range(self.num_cities):
            self.adj_list.append([])
            for j in range(self.num_cities):
                if i != j:
                    self.adj_list[i].append(j)
                else:
                    self.adj_list[i].append(np.inf)
    
    def create_adj_matrix(self):
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                if i != j:
                    self.adj_matrix[i][j] = self.cities[i].costTo(self.cities[j])
                else:
                    self.adj_matrix[i][j] = np.inf

    def row_reduce(self):
        '''Reduces rows of the adjacency matrix by the minimum value in the row. Ensures that the minimum value in each row is 0.'''
        for i in range(self.num_cities):
            min_val = np.inf
            for j in range(self.num_cities):
                if self.adj_matrix[i][j] < min_val:
                    min_val = self.adj_matrix[i][j]
                    if min_val == 0:
                        break
            if min_val != np.inf:
                self.lower_bound += min_val
                for j in range(self.num_cities):
                    self.adj_matrix[i][j] -= min_val
    
    def col_reduce(self):
        '''Reduces columns of the adjacency matrix by the minimum value in the column. Ensures that the minimum value in each column is 0.'''
        for i in range(self.num_cities):
            min_val = np.inf
            for j in range(self.num_cities):
                if self.adj_matrix[j][i] < min_val:
                    min_val = self.adj_matrix[j][i]
                    if min_val == 0:
                        break
            if min_val != np.inf:
                self.lower_bound += min_val
                for j in range(self.num_cities):
                    self.adj_matrix[j][i] -= min_val
    
    def get_partial_paths(self):
        '''Returns list of partial StateGraphs that can be created from the row (city) we are currently at.'''
# REVIEW: keep track of how many states we prune on this iteration, rather than the total number of pruned states?
        pruned_states_count = 0

# FIXME: assuming start city is first city in list
        if len(self.path) == 0:
            self.path.append(0)
            curr_city = 0
        else:
            curr_city = self.path[-1]

        # Indices of cities that we can visit from the current city
        possible_paths = []
        for i in range(self.num_cities):
            if self.adj_matrix[curr_city][i] != np.inf:
                possible_paths.append(i)

        # Create a list of partial StateGraphs to consider
        partial_StateGraphs = []

        for neighborCity in possible_paths:
            # copy the current state graph before making changes
            partial_StateGraph = deepcopy(self)
            # add the cost of the edge to the lower bound
            partial_StateGraph.lower_bound += self.adj_matrix[curr_city][neighborCity]
            # update the depth of the partial StateGraph
            partial_StateGraph.depth += 1

            # remove the edge from the adjacency matrix
            for i in range(self.num_cities):
                partial_StateGraph.adj_matrix[curr_city][i] = np.inf
                partial_StateGraph.adj_matrix[i][neighborCity] = np.inf
            partial_StateGraph.adj_matrix[neighborCity][curr_city] = np.inf

            # reduce the matrix
            partial_StateGraph.row_reduce()
            partial_StateGraph.col_reduce()

            # if the lower bound is less than the current best solution, add the neighbor city to the path and
            # add the partial StateGraph to the list of partial StateGraphs to consider; otherwise, prune
            if partial_StateGraph.lower_bound < self.bssf.cost:
                partial_StateGraph.path.append(neighborCity)
                partial_StateGraphs.append(partial_StateGraph)
            else:
                pruned_states_count += 1
                continue

            if partial_StateGraph.is_solution():
                route = [self.cities[i] for i in partial_StateGraph.path]
                partial_StateGraph.bssf = TSPSolution(route)

        return partial_StateGraphs, pruned_states_count
    
    def is_solution(self):
        '''Returns true if the current StateGraph is a solution.'''
        return len(self.path) == self.num_cities


    
    def print_adj_matrix(self):
        printc(f"Lower Bound: {self.lower_bound}", 'magenta')
        printc(f"bssf cost: {self.bssf.cost}", 'magenta')
        for i in self.adj_matrix:
            for j in i:
                if j == np.inf:
                    print(colorize(j, 'red'), end='\t')
                elif j == 0:
                    print(colorize(j, 'green'), end='\t')
                else:
                    print(colorize(j, 'indigo'), end='\t')
            print()
