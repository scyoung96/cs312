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
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE

        path = []
        curr = self.dest
        while curr != self.source:
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
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        self.dijkstra(use_heap)
        t2 = time.time()
        return (t2-t1)

    def dijkstra(self, use_heap=False):
        self.dist = {}
        self.prev = {}
        self.dist[self.source] = 0
        self.prev[self.source] = None

        for node in self.network.nodes:
            if node.node_id != self.source:
                self.dist[node.node_id] = float('inf')
                self.prev[node.node_id] = None

        if not use_heap:
            nodesPQ = PriorityQueueArray()
        else:
            nodesPQ = PriorityQueueHeap()
        nodesPQ.insert(self.network.nodes[self.source], 0)
        currItem = None

        while not nodesPQ.isEmpty():
            currItem = nodesPQ.deleteMin()
            for edge in currItem.node.neighbors:
                if self.dist[edge.dest.node_id] > self.dist[edge.src.node_id] + edge.length:
                    self.dist[edge.dest.node_id] = self.dist[edge.src.node_id] + edge.length
                    self.prev[edge.dest.node_id] = edge.src.node_id
                    nodesPQ.decreaseKey(edge.dest, self.dist[edge.dest.node_id])
