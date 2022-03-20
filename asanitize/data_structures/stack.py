from asanitize.data_structures.linked_list import Node

class Stack:
    top = None

    def push(self, item):
        new_node = Node(None, item, None)
        if self.top == None:
            self.top = new_node
            return
        
        self.top.next = new_node
        new_node.prev = self.top
        self.top = new_node

    def pop(self):
        if self.top == None:
            return self.top

        to_return = self.top
        if self.top.prev == None:
            self.top = None
            return to_return

        self.top = to_return.prev
        return to_return