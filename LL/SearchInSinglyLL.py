class Node:
    def __init__(self, data = None):
        self.data = data
        self.next = None

class singly__LL():
    def __init__(self):
        self.head  = None
        self.tail = None
        self.count = 0 

    def append_item(self, data):
        node = Node(data)
        if self.head:
            self.head.next = node
            self.head = node

        else:
            self.tail = node
            self.head = node
        self.count += 1

    