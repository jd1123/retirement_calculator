import unittest
from retcalc import retCalc, simData

class TestSimData(unittest.TestCase):
    def setUp(self):
        print 'Setting up TestSimData'
    
    def test_single_simulation(self):
        s = simData(0,1,100)
        self.assertEqual(len(s.simulation()), 100, 'The simulation does not return the correct number of random data')
        for i in s.simulation():
            self.assertTrue(0<=i<=1, 'The random data is not from [0,1]')
        
    def test_simulation_generator(self):
        s = simData(0,1,100)
        l = len(s.get_simulations()[0])
        st = "The get_simulations() method returned " + str(l) + ' and expected ' + str(s.n)
        self.assertEqual(l, 1000, st)
    
    def test_transform(self):
        self.assertFalse(1, 'This test is not yet implemented')

class TestRetCalc(unittest.TestCase):
    def setUp(self):
        print 'Setting up TestRetCalc'
    
    def failure_test(self):
        self.assertFalse(1, 'Test Failure by implementation')

if __name__=='__main__':
    unittest.main()