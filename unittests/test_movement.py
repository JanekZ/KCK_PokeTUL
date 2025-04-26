import unittest
from algorithms.dll_stack import DLLStack
from algorithms.dll_stack import Node

class TestMovement(unittest.TestCase):
    def test_node_initialization(self):
        value = "left"
        node = Node(value)
        self.assertIsNone(node.next)
        self.assertIsNone(node.prev)
        self.assertEqual(node.value, value)

    def test_dll_stack_initialization(self):
        dll_stack = DLLStack()
        self.assertIsNone(dll_stack.head)

    def test_empty(self):
        dll_stack = DLLStack()
        self.assertTrue(dll_stack.is_empty())

        value = "right"
        dll_stack.push(value)
        self.assertFalse(dll_stack.is_empty())

        dll_stack.pop()
        self.assertTrue(dll_stack.is_empty())

    def test_push(self):
        dll_stack = DLLStack()

        value = "left"
        dll_stack.push(value)
        self.assertEqual(value, dll_stack.top().value)

        value2 = "right"
        dll_stack.push(value2)
        self.assertEqual(value2, dll_stack.top().value)

        value3 = "top"
        dll_stack.push(value3)
        self.assertEqual(value3, dll_stack.top().value)

    def test_pop(self):
        dll_stack = DLLStack()

        value = "left"
        dll_stack.push(value)
        value2 = "right"
        dll_stack.push(value2)
        value3 = "top"
        dll_stack.push(value3)

        self.assertEqual(value3, dll_stack.pop())
        self.assertEqual(value2, dll_stack.pop())
        self.assertEqual(value, dll_stack.pop())
        self.assertIsNone(dll_stack.pop())

    def test_remove(self):
        dll_stack = DLLStack()

        values = ["left", "right", "top", "down"]
        dll_stack.push(values[0])
        dll_stack.push(values[1])
        dll_stack.push(values[2])
        dll_stack.push(values[3])

        key = "down"
        dll_stack.remove(key)
        node = dll_stack.head
        while node is not None:
            self.assertNotEqual(node.value, key)
            node = node.prev

        key = "left"
        dll_stack.remove(key)
        node = dll_stack.head
        while node is not None:
            self.assertNotEqual(node.value, key)
            node = node.prev

        key = "top"
        dll_stack.remove(key)
        node = dll_stack.head
        while node is not None:
            self.assertNotEqual(node.value, key)
            node = node.prev

        key = "right"
        dll_stack.remove(key)
        node = dll_stack.head
        while node is not None:
            self.assertNotEqual(node.value, key)
            node = node.prev


if __name__ == "__main__":
    unittest.main()