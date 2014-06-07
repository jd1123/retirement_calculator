import random
from scipy.stats import norm

## This generatres the random data to run the statistical analysis on your portfolio
class simData():
    def __init__(self, mean, stdev, vec_size, n=2500):
        self.mean = mean
        self.stdev = stdev
        self.vec_size = vec_size
        self.n = n
        (x,y) = self.get_simulations()
        self.raw_sims = x
        self.return_sims = y
    
    # Im pretty sure these can be class methods but i dont know how to do them
    # One simulation of size vec_size
    def simulation(self):
        rets = []
        for i in range(self.vec_size):
            rets.append(random.random())
        return rets
    
    # n simulations
    def get_simulations(self):
        sims = []
        full_sims = []
        for i in range(self.n):
            s = self.simulation()
            sims.append(s)
            full_sims.append(norm.ppf(s,loc=self.mean, scale=self.stdev))
        return (sims, full_sims)
    
    #this function runs REALLY slowly - i dont know why.
    def transform_sim_data(self, mean, stdev):
        self.mean = mean
        self.stdev = stdev
        transformed_sims = []
        for s in self.raw_sims:
                transformed_sims.append([norm.ppf(i, loc=mean, scale=stdev) for i in s])
        self.return_sims =  transformed_sims