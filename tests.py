import unittest
from retcalc import retCalc, simData

class TestSimData(unittest.TestCase):
    def setUp(self):
        print 'Setting up TestSimData'
    
    def test_single_simulation(self):
        s = simData(0,1,100)
        self.assertEqual(len(s.simulation()), 100, 'The simulation does not return the correct number of random data')
        self.assertTrue(0<=s.simulation()[0]<=1, 'The random data is not from [0,1]')
        
    def test_simulation_generator(self):
        s = simData(0,1,100)
        self.assertEqual(len(s.get_simulations()), 10000, 'The get_simulations() method does not return the correct number of simulations')
    
    def test_transform(self):
        self.assertFalse(1, 'This test is not yet implemented')

class TestRetCalc(unittest.TestCase):
    def setUp(self):
        print 'Setting up TestRetCalc'
    
    def failure_test(self):
        self.assertFalse(1, 'Test Failure by implementation')

if __name__=='__main__':
    unittest.main()