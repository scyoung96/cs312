# array
class PriorityQueueArray:
    def __init__(self):
        self.array = []
        self.visited = []
        self.currKey = 0

# basic functionality
    def insert(self, node, key):
        self.array.append(Item(node, key))

    def remove(self):
        # returns the Item with the maximum key that was removed
        if len(self.array) == 0:
            return None
        else:
            max = self.array[0]
            for i in range(1, len(self.array)):
                if self.array[i].key > max.key:
                    max = self.array[i]
            self.array.remove(max)
            return max

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
            min = self.array[0]
            for i in range(1, len(self.array)):
                if self.array[i].key < min.key:
                    min = self.array[i]
            self.array.remove(min)
            self.visited.append(min.node)
            return min

    def decreaseKey(self, node, newKey):
        # returns True if key was decreased, False if key was not found and new key was added
        for i in range(len(self.array)):
            if self.array[i].node == node:
                self.array[i] = Item(node, newKey)
                return True
        self.array.append(Item(node, newKey))
        return False


# heap
class PriorityQueueHeap:
    def __init__(self):
        self.heap = []
        self.refDict = {}
        self.currKey = 0

# basic functionality
    def insert(self, node, key):
        self.heap.append(Item(node, key))
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
            return min

    def decreaseKey(self, node, newKey):
        # returns True if key was decreased, False if key was not found and new key was added
        try:
            index = self.refDict[node]
            self.heap[index] = Item(node, newKey)
            self.siftUp(index)
            return True
        except:
            index = len(self.heap)
            self.heap.append(Item(node, newKey))
            self.refDict[node] = index
            self.siftUp(index)
            return False


class Item:
    def __init__(self, node=None, key=None):
        self.key = key
        self.node = node
