class Node:
    item = None
    prev = None
    next = None

    def __init__(self, prev, item, next):
        self.prev = prev
        self.item = item
        self.next = next
    
class LinkedList:
    count = 0
    head = None

    def is_empty(self):
        return (self.count == 0)

    def find(self, position):
        if position > self.count or self.is_empty():
            return None

        current_node = self.head
        for i in range(0, self.count):
            if i == position:
                break

            current_node = current_node.next

        return current_node
    
    def set(self, position, item):
        if position > self.count:
            return False

        node = self.find(position)
        node.item = item
        return True

    def insert(self, position, item):
        if position > self.count:
            return False

        # If it is adding at the start of list.
        if position == 0:
            self.head = Node(None, item, self.head)
        elif position == self.count: # If it is adding at the end of list.
            prev_node = self.find(position - 1)
            new_node = Node(prev_node, item, None)
            prev_node.next = new_node
        else: # If it is adding at anywhere between 2 nodes.
            node_to_replace = self.find(position)
            new_node = Node(node_to_replace.prev, item, node_to_replace)
            node_to_replace.prev.next = new_node
            node_to_replace.prev = new_node

        self.count += 1
        return True

    def append(self, item):
        return self.insert(self.count, item)
        
    def remove(self, position):
        if position > self.count:
            return False
        
        node = self.find(position)

        node.prev.next = node.next
        node.next.prev = node.prev

        return True