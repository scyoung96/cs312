import numpy as np
from copy import deepcopy

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
        self.pruned_states_count = 0
    
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

# FIXME: assuming start city is first city in list
        if len(self.path) == 0:
            self.path.append(0)
            curr_city = 0
        else:
            curr_city = self.path[-1]

        # Indices of cities that we can visit from the current city
        possible_paths = []
        for i in range(len(curr_city)):
            if curr_city[i] != np.inf:
                possible_paths.append(i)

        # Create a list of partial StateGraphs to consider
        partial_StateGraphs = []

        for neighborCity in possible_paths:
# REVIEW: Does this need to be a deep copy? Is this just a reference?
            # partial_StateGraph = StateGraph(self.cities, self.bssf)
            partial_StateGraph = deepcopy(self)

            for i in range(self.num_cities):
                partial_StateGraph.adj_matrix[curr_city][i] = np.inf
                partial_StateGraph.adj_matrix[i][neighborCity] = np.inf
            
            partial_StateGraph.adj_matrix[neighborCity][curr_city] = np.inf

            partial_StateGraph.row_reduce()
            partial_StateGraph.col_reduce()

            if partial_StateGraph.lower_bound < self.bssf.cost:
                partial_StateGraph.path.append(neighborCity)
                partial_StateGraphs.append(partial_StateGraph)
            else:
                self.pruned_states_count += 1

        return partial_StateGraphs
    
    def is_solution(self):
        '''Returns true if the current StateGraph is a solution.'''
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                if self.adj_matrix[i][j] != np.inf:
                    return False
        return True


    

