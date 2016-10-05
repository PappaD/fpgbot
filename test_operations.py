import operations
import unittest

class find_pokemon_tests(unittest.TestCase):
    def testEmpty(self):
        self.assertEqual(operations.find_pokemon('xxasd'), [])

    def testSingle(self):
        self.assertEqual(operations.find_pokemon('pidgey'), ['PIDGEY'])        

    def testMultiple(self):
        self.assertEqual(operations.find_pokemon('pid'), ['PIDGEY', 'PIDGEOT', 'PIDGEOTTO', 'RAPIDASH'])



if __name__ == '__main__':
    unittest.main()        