import unittest
from asanitize.data_structures.stack import Stack

class TestStack(unittest.TestCase):

    def setUp(self) -> None:
        self.stack = Stack()

    def test_push(self):
        self.stack.push('A')
        self.assertEqual(self.stack.top.item, 'A')

        self.stack.push('B')
        self.assertEqual(self.stack.top.item, 'B')
        
        self.stack.push('C')
        self.assertEqual(self.stack.top.item, 'C')
        
        self.stack.push('D')
        self.assertEqual(self.stack.top.item, 'D')

    def test_pop(self):
        self.stack.push('A')
        self.stack.push('B')
        self.stack.push('C')
        self.stack.push('D')
        self.stack.push('E')

        self.assertEqual(self.stack.pop().item, 'E')
        self.assertEqual(self.stack.top.item, 'D')
        self.assertEqual(self.stack.pop().item, 'D')
        self.assertEqual(self.stack.top.item, 'C')
        self.assertEqual(self.stack.pop().item, 'C')
        self.assertEqual(self.stack.top.item, 'B')
        self.assertEqual(self.stack.pop().item, 'B')
        self.assertEqual(self.stack.top.item, 'A')
        self.assertEqual(self.stack.pop().item, 'A')