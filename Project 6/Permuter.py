from copy import deepcopy
from random import randint

from colorize import *
from TSPClasses import *

class Permuter:
    def __init__(self, cities, bssf=None):
        self.cities = cities
        self.num_cities = len(cities)
        self.bssf = bssf
    
    def get_permutations(self):
        '''Returns list of partial StateGraphs that can be created from the row (city) we are currently at.'''
        permutations = []

        # create a random permutation (swap random edges)
        for i in range(self.num_cities):
            copy = deepcopy(self)

            rand1 = randint(0, self.num_cities - 1)
            rand2 = randint(0, self.num_cities - 1)

            # swap the cities
            self.cities[rand1], self.cities[rand2] = self.cities[rand2], self.cities[rand1]

            permutations.append(copy)

        return permutations
    
    def is_solution(self):
        '''Returns true if the current StateGraph is a solution.'''
        return len(self.path) == self.num_cities
