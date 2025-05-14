import unittest
from algorithms.dll_stack import DLLStack
from algorithms.dll_stack import Node

class TestDLLStack(unittest.TestCase):
    def setUp(self):
        self.node_init_value = "value"
        self.init_node = Node(self.node_init_value)
        self.init_dll_stack = DLLStack()

    def test_node_initialization_next_is_none(self):
        self.assertIsNone(self.init_node.next)

    def test_node_initialization_prev_is_none(self):
        self.assertIsNone(self.init_node.prev)

    def test_node_initialization_value_check(self):
        self.assertEqual(self.init_node.value, self.node_init_value)

    def test_dll_stack_initialization_head_is_none(self):
        self.assertIsNone(self.init_dll_stack.head)

    def test_dll_stack_is_empty(self):
        self.assertTrue(self.init_dll_stack.is_empty())

    def test_dll_stack_is_not_empty(self):
        self.init_dll_stack.push(self.node_init_value)
        self.assertFalse(self.init_dll_stack.is_empty())

    def test_dll_stack_is_empty_after_pop(self):
        self.init_dll_stack.pop()
        self.assertTrue(self.init_dll_stack.is_empty())

    def test_push(self):
        dll_stack = DLLStack()

        value1 = "left"
        value2 = "right"
        value3 = "top"

        dll_stack.push(value1)
        self.assertEqual(value1, dll_stack.top().value)

        dll_stack.push(value2)
        self.assertEqual(value2, dll_stack.top().value)

        dll_stack.push(value3)
        self.assertEqual(value3, dll_stack.top().value)

    def test_pop_if_no_head(self):
        dll_stack = DLLStack()
        pop_value = dll_stack.pop()
        self.assertIsNone(pop_value)

    def test_pop(self):
        dll_stack = DLLStack()

        value = "left"
        value2 = "right"
        value3 = "top"

        dll_stack.push(value)
        dll_stack.push(value2)
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
