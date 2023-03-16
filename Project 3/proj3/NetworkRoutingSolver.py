#!/usr/bin/python3


from CS312Graph import *
from PriorityQueue import *
import time


class NetworkRoutingSolver:
    def __init__( self):
        self.network = None
        self.source  = None
        self.dest    = None
        self.dist    = None
        self.prev    = None

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex

        path = []
        curr = self.dest
        while curr != self.source:

            if curr is None:
                return {'cost':float('inf'), 'path':[]}

            path.append(curr)
            curr = self.prev[curr]
        path.append(self.source)
        path = path[::-1]

        path_edges = []
        for i in range(len(path)-1):
            for edge in self.network.nodes[path[i]].neighbors:
                if edge.dest.node_id == path[i+1]:
                    path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
                    break
        
        return {'cost':self.dist[self.dest], 'path':path_edges}


    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        self.dijkstra(use_heap)
        t2 = time.time()
        return (t2-t1)


    # dijkstra
# NOTE: time complexity: varies between array and heap implementations, space complexity: O(|V|)
    # time: Dijkstra itself has a time complexity of O(|V|) before anything is done since we must
    # first iterate over each node to set the dist and prev arrays. After that, the complexity
    # diverges depending on if we are using an array or heap implementation of a priority queue.
    # The array implementation has O(|V|) time complexity on its dominating function, deleteMin(),
    # since it has to iterate through the entire array to find the minimum node. We multiply this
    # with the base O(|V|) time complexity of dijkstra() to get O(|V|^2).
    # The heap implementation has O(log|V|) time complexity on each of its functions, since at each
    # step it cuts out half the tree as it sifts up/down. We multiply this with the base O(|V|)
    # time complexity of dijkstra() to get O(|V|log|V|).
    # space: O(|V|) since we are creating two dictionaries of size V, one for the distance
    # to each node, and one for the previous node of each node
    def dijkstra(self, use_heap=False):
        self.dist = {}
        self.prev = {}
        self.dist[self.source] = 0
        self.prev[self.source] = None

    # NOTE: time complexity: O(|V|), space complexity: O(|V|)
        # time: this is because we have to iterate through the entire graph to initialize the
        # distance and previous dictionaries, which is a linear time operation since |V|
        # is the number of nodes in the graph
        # space: this is because we are creating two dictionaries, one for the distance to
        # each node, and one for the previous node of each node, which is a linear space
        # operation since |V| is the number of nodes in the graph
        for node in self.network.nodes:
            if node.node_id != self.source:
                self.dist[node.node_id] = float('inf')
                self.prev[node.node_id] = None

        if not use_heap:
            nodesPQ = PriorityQueueArray()
        else:
            nodesPQ = PriorityQueueHeap()
        nodesPQ.insert(self.network.nodes[self.source], 0)
        currNode = None

    # NOTE: time complexity: varies between array and heap implementations, space complexity: O(|V|)
        # time: O(|V|^2) for the array implementaton and O(|V|log|V|) for the heap implementation
        # space: O(|V|) for both implementations
        while not nodesPQ.isEmpty():
            currNode = nodesPQ.deleteMin()
            for edge in currNode.neighbors:
                if self.dist[edge.dest.node_id] > self.dist[edge.src.node_id] + edge.length:
                    self.dist[edge.dest.node_id] = self.dist[edge.src.node_id] + edge.length
                    self.prev[edge.dest.node_id] = edge.src.node_id
                    nodesPQ.decreaseKey(edge.dest, self.dist[edge.dest.node_id])
