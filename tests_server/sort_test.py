import unittest
from sorting import our_sort

class MyTestCae(unittest.TestCase):
    def test_sort(self):
        mass = [[1, 4, 7, 9], [2, 3, 4, 5, 6], [8, 10, 16, 24]]
        res = list(our_sort(mass))
        refr = [1, 2, 3, 4, 4, 5, 6, 7, 8, 9, 10, 16, 24]
        self.assertEqual(res, refr)

if __name__ == '__main__':
    unittest.main()
