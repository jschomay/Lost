import unittest
from utils import *


class TestUtils(unittest.TestCase):

    def test_progress(self):
        self.assertEqual(progress(100, 200, 150), 0.5)
        self.assertEqual(progress(100, 200, 250), 1)
        self.assertEqual(progress(100, 200, 50), 0)
        self.assertEqual(progress(100, 200, 199), 0.99)
        self.assertEqual(progress(0, 300, 200), 2/3)
        self.assertEqual(progress(100, 200, 101), 0.01)
        self.assertEqual(progress(100, 200, 100), 0)


if __name__ == "__main__":
    unittest.main(exit=False)
