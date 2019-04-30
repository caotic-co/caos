python_unit_test_file='''\
import unittest

class SimpleTest(unittest.TestCase):    

    def test_a(self) -> None:
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()

'''