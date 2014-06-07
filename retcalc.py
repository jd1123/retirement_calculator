import numpy
from scipy.stats import norm
import datetime
import random

### TODO
# I need to refactor this code. It is stupid. do the calcs,
# then create the dict. Don't use the dict directly

class retCalc():
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
            self.param_dict = param_dict
            
        except KeyError as e:
            print e
                
        self.now = datetime.datetime.now().year
        self.retirement_age = 65
        self.expected_rate_of_return = 0.07
        self.asset_volatility = 0.13
        self.inflation_rate = 0.035
        self.simdata = simData(self.expected_rate_of_return, self.asset_volatility, self.years)
        self.plan_dict = self.run_all_sims()
        
    
    def get_final_balance(self, path):
        key = max(path.keys())
        return path[key]['EOY_taxable_balance'] + path[key]['EOY_non_taxable_balance']
    
    # runs all the sims and returns a list of paths sorted by end balance
    def run_all_sims(self):
        all_paths = []
        for sim in self.simdata.return_sims:
            path = pathOnPortfolio(self.param_dict, sim)
            all_paths.append(path)
        all_paths.sort(key=lambda x: x.end_balance)
        return all_paths
    
    def confidence_path(self, confidence = 0.1):
        n_path = int(confidence * len(self.plan_dict))
        self.plan_dict[n_path].print_path()
        return self.plan_dict[n_path]

#each path will be an object with an associated sim
class pathOnPortfolio():
    def __init__(self, param_dict, sim):
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
        self.sim = sim
        
        self.now = datetime.datetime.now().year
        self.retirement_age = 65
        self.expected_rate_of_return = 0.07
        self.asset_volatility = 0.13
        self.inflation_rate = 0.035
        #self.simdata = simData(self.expected_rate_of_return, self.asset_volatility, self.years)
        #self.plan_dict = self.run_all_sims()
        self.path_dict = self.run_calc()
        self.end_balance = self.get_final_balance()
    
    def __repr__(self):
        return str(int(self.end_balance)) + " " + str(sum(self.sim)/float(len(self.sim)))
        
    def path_to_dict(self):
        pass
    
    def get_final_balance(self):
        key = max(self.path_dict.keys())
        return self.path_dict[key]['EOY_taxable_balance'] + self.path_dict[key]['EOY_non_taxable_balance']
    
    def run_calc(self):
        # this can use a refactor....BIGTIME
        plan_dict = {}
        plan_dict[self.now] = {'age' : self.age,
             'SOY_taxable_balance': self.taxable_balance,
             'SOY_non_taxable_balance' : self.non_taxable_balance,
             'yearly_expenses' : 0,
             'return' : self.sim[0]
             }
        plan_dict[self.now]['EOY_taxable_balance'] = plan_dict[self.now]['SOY_taxable_balance']*(1+self.sim[0])*(1-self.returns_tax_rate) + self.taxable_contribution
        plan_dict[self.now]['EOY_non_taxable_balance'] = plan_dict[self.now]['SOY_non_taxable_balance']*(1+self.sim[0]) + self.non_taxable_contribution  
        plan_dict[self.now]['taxable_contribution'] = self.taxable_contribution
        plan_dict[self.now]['non_taxable_contribution'] = self.non_taxable_contribution
        
        for i in range(1,self.years):
            year = self.now + i
            last_year_dict = plan_dict[year-1]
            
            age = self.age + i
            SOY_taxable_balance = last_year_dict['EOY_taxable_balance']
            SOY_non_taxable_balance = last_year_dict['EOY_non_taxable_balance']
            rate_of_return = self.sim[i]
            
            if age > self.retirement_age:
                expenses = self.monthly_retirement_expenses * 12 * (1+self.inflation_rate)**i
            else:
                expenses = 0
            
            taxable_contrib = 0
            non_taxable_contrib = 0
            
            if age <= self.retirement_age:
                taxable_contrib = self.taxable_contribution                
                non_taxable_contrib = self.non_taxable_contribution
            else:
                taxable_contrib = 0
                non_taxable_contrib = 0
                
            # this logic needs work ->
            # how to determine which account to deduce from? and what to do with the account when it runs out?
            if SOY_taxable_balance >= 0:
                taxable_returns = SOY_taxable_balance*(rate_of_return)*(1-self.returns_tax_rate)
                EOY_taxable_balance = SOY_taxable_balance + taxable_returns + taxable_contrib
            
            # this logic needs work ->
            # how to determine which account to deduce from? and what to do with the account when it runs out?
            if SOY_non_taxable_balance >= 0:
                non_taxable_returns = (1+rate_of_return)
                EOY_non_taxable_balance = SOY_non_taxable_balance*(1+rate_of_return) + non_taxable_contrib
            else:
                EOY_non_taxable_balance=0
            
            if expenses > 0:
                EOY_non_taxable_balance-=expenses/self.effective_tax_rate
        
            plan_dict[year] = {'age' : self.age + i,
             'SOY_taxable_balance': SOY_taxable_balance,
             'SOY_non_taxable_balance' : SOY_non_taxable_balance,
             'yearly_expenses' : expenses,
             'return' : rate_of_return,
             'non_taxable_contribution' : non_taxable_contrib,
             'taxable_contribution' : taxable_contrib,
             'EOY_taxable_balance' : EOY_taxable_balance,
             'EOY_non_taxable_balance' : EOY_non_taxable_balance,
             'taxable_returns' : taxable_returns,
             'non_taxable_returns' : non_taxable_returns,
            }
            
        return plan_dict
    
    def print_path(self):
        print "Average return :" + str(numpy.mean(self.sim))
        print "year : return : SOY_balance : contribution : expenses : EOY_balance "
        for k in sorted(self.path_dict.keys()):
            print str(k) + " : " + str(self.path_dict[k]['return']) + " : " + str(int(self.path_dict[k]['SOY_non_taxable_balance'])) + " : " + str(self.path_dict[k]['non_taxable_contribution']) + " : " + str(int(self.path_dict[k]['yearly_expenses'])) + " : " + str(int(self.path_dict[k]['EOY_non_taxable_balance']))
        
        #for k,v in self.path_dict.iteritems():
         #   print str(k) + " : " + str(v['SOY_non_taxable_balance']) + " : " + str(v['non_taxable_contribution']) + " : " + str(v['EOY_non_taxable_balance'])

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