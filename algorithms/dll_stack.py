class Node:
    def __init__(self, value: str) -> None:
        self.next: Node|None = None
        self.prev: Node|None = None
        self.value: str = value

class DLLStack:
    def __init__(self):
        self.head = None

    def push(self, value: str) -> None:
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            self.head.next = new_node
            new_node.prev = self.head
            self.head = new_node

    def pop(self) -> str | None:
        if not self.is_empty():
            head_node_value = self.head.value
            if self.head.prev is not None:
                self.head.prev.next = None
                self.head = self.head.prev
            else:
                self.head = None
            return head_node_value
        return None

    def is_empty(self) -> bool:
        return self.head is None

    #Removes the node with given value that is closest to head
    def remove(self, value: str) -> None:
        node = self.head
        while node is not None:
            if node.value == value:
                if node.prev is not None:
                    node.prev.next = node.next
                if node.next is None:
                    self.head = node.prev
                else:
                    node.next.prev = node.prev
                break
            else:
                node = node.prev


    def top(self) -> Node:
        return self.head

    def clear(self):
        self.head = None