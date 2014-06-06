import numpy
from scipy.stats import norm
import datetime
import random

class retCalc():
    def old(self):
        self.age = None
        self.retirement_age = None
        self.terminal_age = None
        self.non_taxable_balance = None
        self.taxable_balance = None
        self.effective_tax_rate = 0.3
        self.returns_tax_rate = 0.15
        self.non_taxable_contribution = 17500
        self.taxable_contribution = 0
        self.yearly_retirement_expenses = None
        self.now = datetime.datetime.now().year
        self.years = 0
        #years = self.retirement_age - self.age + 1
        
        
        self.expected_rate_of_return = 0.07
        self.asset_volatility = 0.13
        self.inflation_rate = 0.035
        
        
    def __init__(self, param_dict): 
        try:
            self.age = param_dict['age']
            self.retirement_age = param_dict['retirement_age']
            self.terminal_age = param_dict['terminal_age']
            self.non_taxable_balance = param_dict['non_taxable_balance']
            self.taxable_balance = param_dict['taxable_balance']
            self.effective_tax_rate = param_dict['eff_tax_rate']
            self.returns_tax_rate = param_dict['returns_tax_rate']
            self.non_taxable_contribution = param_dict['non_taxable_contribution']
            self.taxable_contribution = param_dict['taxable_contribution']
            self.monthly_retirement_expenses = param_dict['monthly_retirement_expenses']
            self.years = self.terminal_age - self.age
            
        except KeyError as e:
            print e
                
        self.now = datetime.datetime.now().year
        self.retirement_age = 65
        self.expected_rate_of_return = 0.07
        self.asset_volatility = 0.13
        self.inflation_rate = 0.035
        self.simdata = simData(self.expected_rate_of_return, self.asset_volatility, self.years)
        self.plan_dict = self.run_calc_on_sim(self.simdata.return_sims[0])
        
    
    #format for a year:
    # dict of dicts ->
    # plan[year] -> year_dict -> year_dict
    def run_calc_on_sim(self, sim):
        plan_dict = {}
        p = plan_dict[self.now]
        p = {'age' : self.age,
             'SOY_taxable_balance': self.taxable_balance,
             'SOY_non_taxable_balance' : self.non_taxable_balance,
             'yearly_expenses' : 0,
             }
        p['EOY_taxable_balance'] = p['SOY_taxable_balance']*(1+sim[0])*(1-self.returns_tax_rate) + self.taxable_contribution
        p['EOY_non_taxable_balance'] = p['SOY_non_taxable_balance']*(1+sim[0]) + self.non_taxable_contribution  
        
        for i in range(1,self.years):
            
            rate_of_return = sim[i]
            year = self.now + i
            last_year_dict = plandict[year-1]
            
            if self.age + i > self.retirement_age:
                expenses = self.monthly_retirement_expenses * 12
            else:
                expenses = 0
            
            plan_dict[year] = {'age' : self.age + i,
             'SOY_taxable_balance': last_year_dict['EOY_taxable_balance'],
             'SOY_non_taxable_balance' : last_year_dict['non_taxable_balance'],
             'yearly_expenses' : expenses,
            }
            
            taxable_contrib = 0
            non_taxable_contrib = 0
            if plan_dict[year]['age'] <= self.retirement_age:
                taxable_contrib = self.taxable_contribution
                non_taxable_contrib = self.non_taxable_contribution
            
            if plan_dict[year]['SOY_taxable_balance'] >= 0:
                plan_dict[year]['EOY_taxable_balance'] = plan_dict[year]['SOY_taxable_balance']*(1+rate_of_return)*(1-self.returns_tax_rate) + taxable_contrib
            
            if plan_dict[year]['SOY_non_taxable_balance'] >= 0:
                plan_dict[year]['EOY_non_taxable_balance'] = plan_dict[year]['SOY_non_taxable_balance']*(1+rate_of_return) + non_taxable_contrib
            
            if expenses > 0:
                plan_dict[year]['EOY_non_taxable_balance']-=expenses/self.effective_tax_rate
        
        return plan_dict

## This generatres the random data to run the statistical analysis on your portfolio
class simData():
    def __init__(self, mean, stdev, vec_size, n=1000):
        self.mean = mean
        self.stdev = stdev
        self.vec_size = vec_size
        self.n = n
        self.raw_sims = self.get_simulations()
        self.return_sims = self.transform_sim_data(self.raw_sims)
    
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
        for i in range(self.n):
            sims.append(self.simulation())
        return sims
    
    #will transform the raw uniform dist into
    #normal with mean self.mean and stdev self.stdev
    #this will allow for changing parameters without rerunning the random
    #generator - NEED SCIPY for scipy.stats.norm.ppf()
    def transform_sim_data(self, sims):
        transformed_sims = []
        for s in sims:
                transformed_sims.append([norm.ppf(i, loc=self.mean, scale=self.stdev) for i in s])
        return transformed_sims