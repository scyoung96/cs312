# array
class PriorityQueueArray:
    def __init__(self):
        self.array = []
        self.dist = {}
        self.visited = set()
        self.currKey = 0

# NOTE: time complexity: O(1), space complexity: O(1)
    # this is because all we are doing is appending the item to the end of the array,
    # which is a constant time and space operation
    def insert(self, node, key):
        '''inserts a node into the priority queue with a given key'''
        if node not in self.visited:
            self.array.append(node)
            self.visited.add(node)
            self.dist[node] = key

# NOTE: time complexity: O(|V|), space complexity: O(1)
    # time: this is because we have to iterate through the entire array to find the minimum,
    # which is a linear time operation since |V| is the number of nodes in the graph
    # and we will have to iterate through the entire array to ensure we find the minimum
    # space: this is because we are not creating any new data structures, we are just
    # iterating through the array and removing the minimum node from the array
    def deleteMin(self):
        '''returns the node with the minimum key and removes it from the priority queue'''
        if len(self.array) == 0:
            return None
        else:
            minNode = self.array[0]
            minDist = self.dist[self.array[0]]
            for i in range(1, len(self.array)):
                if self.dist[self.array[i]] < minDist:
                    minNode = self.array[i]
                    minDist = self.dist[self.array[i]]
            self.array.remove(minNode)
            del self.dist[minNode]
            return minNode

# NOTE: complexity: O(1), space complexity: O(1)
    # time: this is because we are just updating the key in the dictionary, which is a constant
    # time operation. For code compression, if a call to decreaseKey() is made and the
    # node is not in the priority queue, then we add the node to the priority queue
    # space: this is because we are just updating the key in the dictionary, which is a constant
    # space operation
    def decreaseKey(self, node, newKey):
        '''returns True if node's key was decreased, False if key was not found and new key was added'''
        if node in self.visited:
            self.dist[node] = newKey
            return True
        else:
            self.insert(node, newKey)
            return False

    def isEmpty(self):
        '''returns True if the priority queue is empty, False otherwise'''
        return len(self.array) == 0

    def size(self):
        '''returns the number of elements in the priority queue'''
        return len(self.array)


# heap
class PriorityQueueHeap:
    def __init__(self):
        self.heap = []
        self.refDict = {}
        self.visited = set()
        self.currKey = 0

# NOTE: time complexity: O(log|V|), space complexity: O(1)
    # time: this is because we are sifting up the element to its correct position in the heap after
    # appending it to the end of the heap, which means that siftUp() will call itself recursively
    # at most log|V| times
    # space: this is because we are not creating any new data structures, we are just appending
    # the item to the end of the heap and then sifting it up to its correct position in the heap
    def insert(self, node, key):
        '''inserts a node into the priority queue with a given key'''
        if node not in self.visited:
            self.heap.append(Item(node, key))
            self.visited.add(node)
            self.refDict[node] = len(self.heap) - 1
            self.siftUp(len(self.heap) - 1)

# NOTE: time complexity: O(log|V|), space complexity: O(1)
    # time: this is because we are swapping the end of the array with the root, popping the min item
    # that was put at the end, and then sifting down the new root to its correct position in the
    # heap, which means that siftDown() will call itself recursively at most log|V| times
    # space: this is because we are not creating any new data structures, we are just swapping
    # the end of the array with the root, popping the min item that was put at the end, and then
    # sifting down the new root to its correct position in the heap
    def deleteMin(self):
        '''returns the node with the minimum key and removes it from the priority queue'''
        if len(self.heap) == 0:
            return None
        else:
            del self.refDict[self.heap[0].node]
            self.refDict[self.heap[len(self.heap) - 1].node] = 0
            self.heap[0], self.heap[len(self.heap) - 1] = self.heap[len(self.heap) - 1], self.heap[0]
            min = self.heap.pop()
            self.siftDown(0)
            return min.node

# NOTE: time complexity: O(log|V|), space complexity: O(1)
    # time: this is because we are sifting up the element to its correct position in the heap after
    # updating its key, which means that siftUp() will call itself recursively at most log|V|
    # times. For code compression, if a call to decreaseKey() is made and the node is not in
    # the priority queue, then we add the node to the priority queue
    # space: this is because we are not creating any new data structures, we are just updating
    # the key of the node and then sifting it up to its correct position in the heap
    def decreaseKey(self, node, newKey):
        '''returns True if node's key was decreased, False if key was not found and new key was added'''
        try:
            index = self.refDict[node]
            self.heap[index].key = newKey
            self.siftUp(index)
            return True
        except:
            index = len(self.heap)
            self.insert(node, index)

    def siftUp(self, index):
        '''sifts up the element at index to its correct position in the heap'''
        if index == 0:
            return
        parent = (index - 1) // 2
        if self.heap[index].key < self.heap[parent].key:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self.refDict[self.heap[parent].node] = parent
            self.refDict[self.heap[index].node] = index
            self.siftUp(parent)

    def siftDown(self, index):
        '''sifts down the element at index to its correct position in the heap'''
        left = 2 * index + 1
        right = 2 * index + 2
        if left >= len(self.heap):
            return
        if right >= len(self.heap):
            if self.heap[index].key > self.heap[left].key:
                self.heap[index], self.heap[left] = self.heap[left], self.heap[index]
                self.refDict[self.heap[left].node] = left
                self.refDict[self.heap[index].node] = index
            return
        if self.heap[left].key < self.heap[right].key:
            if self.heap[index].key > self.heap[left].key:
                self.heap[index], self.heap[left] = self.heap[left], self.heap[index]
                self.refDict[self.heap[left].node] = left
                self.refDict[self.heap[index].node] = index
                self.siftDown(left)
        else:
            if self.heap[index].key > self.heap[right].key:
                self.heap[index], self.heap[right] = self.heap[right], self.heap[index]
                self.refDict[self.heap[right].node] = right
                self.refDict[self.heap[index].node] = index
                self.siftDown(right)

    def isEmpty(self):
        '''returns True if the priority queue is empty, False otherwise'''
        return len(self.heap) == 0

    def size(self):
        '''returns the number of elements in the priority queue'''
        return len(self.heap)


class Item:
    '''Item class to improve readability of the heap implementation of the priority queue'''
    def __init__(self, node=None, key=None):
        self.key = key
        self.node = node
