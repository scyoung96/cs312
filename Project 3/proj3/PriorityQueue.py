# array
class PriorityQueueArray:
    def __init__(self):
        self.array = []
        self.dist = {}
        self.visited = set()
        self.currKey = 0

# basic functionality
    def insert(self, node, key):
        if node not in self.visited:
            self.array.append(node)
            self.dist[node] = key
            self.visited.add(node)

    def remove(self):
        # returns the Item with the maximum key that was removed
        if len(self.array) == 0:
            return None
        else:
            maxNode = self.array[0]
            maxDist = self.dist[self.array[0]]
            for i in range(1, len(self.array)):
                if self.dist[self.array[i]] > maxDist:
                    maxNode = self.array[i]
                    maxDist = self.dist[self.array[i]]
            self.array.remove(maxNode)
            del self.dist[maxNode]
            return maxNode

    def isEmpty(self):
        return len(self.array) == 0

    def size(self):
        return len(self.array)

# additonal functionality
    def deleteMin(self):
        # returns the Item with the minimum key that was removed
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

    def decreaseKey(self, node, newKey):
        # returns True if key was decreased, False if key was not found and new key was added
        if node in self.visited:
            self.dist[node] = newKey
            return True
        else:
            self.array.append(node)
            self.visited.add(node)
            self.dist[node] = newKey
            return False


# heap
class PriorityQueueHeap:
    def __init__(self):
        self.heap = []
        self.refDict = {}
        self.visited = set()
        self.currKey = 0

# basic functionality
    def insert(self, node, key):
        if node not in self.visited:
            self.heap.append(Item(node, key))
            self.visited.add(node)
            self.refDict[node] = len(self.heap) - 1
            self.siftUp(len(self.heap) - 1)

    def siftUp(self, index):
        if index == 0:
            return
        parent = (index - 1) // 2
        if self.heap[index].key < self.heap[parent].key:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self.refDict[self.heap[parent].node] = parent
            self.refDict[self.heap[index].node] = index
            self.siftUp(parent)

    def siftDown(self, index):
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
        if self.heap[left].key > self.heap[right].key:
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
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)

# additonal functionality
    def deleteMin(self):
        # returns the Item with the minimum key that was removed
        if len(self.heap) == 0:
            return None
        else:
            del self.refDict[self.heap[0].node]
            self.refDict[self.heap[len(self.heap) - 1].node] = 0
            self.heap[0], self.heap[len(self.heap) - 1] = self.heap[len(self.heap) - 1], self.heap[0]
            min = self.heap.pop()
            self.siftDown(0)
            return min.node

    def decreaseKey(self, node, newKey):
        # returns True if key was decreased, False if key was not found and new key was added
        try:
            index = self.refDict[node]
            self.heap[index] = Item(node, newKey)
            self.siftUp(index)
            return True
        except:
            if node not in self.visited:
                index = len(self.heap)
                self.heap.append(Item(node, newKey))
                self.visited.add(node)
                self.refDict[node] = index
                self.siftUp(index)
                return False


class Item:
    def __init__(self, node=None, key=None):
        self.key = key
        self.node = node
