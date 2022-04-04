import unittest
from asanitize.data_structure.linked_list import LinkedList

class TestLinkedList(unittest.TestCase):

    def setUp(self) -> None:
        self.linked_list = LinkedList()

    def testIsEmptyIfEmpty(self) -> None:
        self.assertTrue(self.linked_list.is_empty())

    def testInsert(self) -> None:
        self.linked_list.append('test_item')
        self.linked_list.append('test_item2')
        self.linked_list.append('test_item3')

        self.assertEqual(self.linked_list.find(0).item, 'test_item')
        self.linked_list.insert(1, 'aaaa')
        self.assertEqual(self.linked_list.find(1).item, 'aaaa')
        self.assertEqual(self.linked_list.find(2).item, 'test_item2')
        self.assertEqual(self.linked_list.find(3).item, 'test_item3')

    def testAppend(self) -> None:
        self.linked_list.append('test_item')
        self.assertEqual(self.linked_list.head.item, 'test_item')

    def testIsEmptyIfNotEmpty(self) -> None:
        self.linked_list.append('test_item')
        self.assertFalse(self.linked_list.is_empty())

    def testFind(self) -> None:
        self.linked_list.append('test_item')
        node = self.linked_list.find(0)

        self.assertEqual(node.item, 'test_item')

    def testSet(self) -> None:
        self.linked_list.append('test_item')
        node = self.linked_list.find(0) 
        
        self.assertEqual(node.item, 'test_item')
        self.assertTrue(self.linked_list.set(0, 'test_item_2'))
        self.assertEqual(node.item, 'test_item_2')

    def testRemove(self):
        self.linked_list.append('test_item')
        self.linked_list.append('test_item2')
        self.linked_list.append('test_item3')

        self.linked_list.remove(1)
        self.assertEqual(self.linked_list.find(1).item, 'test_item3')