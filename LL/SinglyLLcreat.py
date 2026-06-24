class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class singly__LL:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def iterate_item(self): # iterate the list
        current_item = self.head
        while current_item:
            val = current_item.data
            current_item = current_item.next
            yield val
    
    def append_item(self, data):
        node = Node(data)
        if self.tail:
            self.tail.next = node
            self.tail = node

        else:
            self.head = node
            self.tail = node
        self.count += 1

items = singly__LL()
items.append_item(1)
items.append_item(1)
items.append_item(1)
items.append_item(1)

for v in items.iterate_item():
    print(v)
print("\nHead : ",items.head.data)
print("\nTail : ",items.tail.data)
print("\nSize of LL : ",items.count)
