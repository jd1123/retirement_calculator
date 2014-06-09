import datetime
import numpy

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
        self.years = self.terminal_age - self.age + 1
        self.sim = sim
        
        self.now = datetime.datetime.now().year
        self.retirement_age = param_dict['retirement_age']
        self.expected_rate_of_return = param_dict['expected_rate_of_return']
        self.asset_volatility = param_dict['asset_volatility']
        self.inflation_rate = param_dict['inflation_rate']
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
        plan_dict = {}
        non_taxable_returns = self.non_taxable_balance*self.sim[0]
        plan_dict[self.now] = {'age' : self.age,
             'SOY_taxable_balance': self.taxable_balance,
             'SOY_non_taxable_balance' : self.non_taxable_balance,
             'yearly_expenses' : 0,
             'return' : self.sim[0],
             'EOY_taxable_balance' : self.taxable_balance*(1+self.sim[0])*(1-self.returns_tax_rate) + self.taxable_contribution,
             'EOY_non_taxable_balance' : self.non_taxable_balance*(1+self.sim[0]) + self.non_taxable_contribution,
             'taxable_contribution' : self.taxable_contribution,
             'non_taxable_contribution' : self.non_taxable_contribution,
             'non_taxable_returns' : non_taxable_returns,
             }
        plan_dict[self.now]['EOY_balance'] = plan_dict[self.now]['EOY_taxable_balance'] + plan_dict[self.now]['EOY_non_taxable_balance']
        
        for i in range(1,self.years):
            year = self.now + i
            last_year_dict = plan_dict[year-1]
            
            age = self.age + i
            SOY_taxable_balance = last_year_dict['EOY_taxable_balance']
            SOY_non_taxable_balance = last_year_dict['EOY_non_taxable_balance']
            rate_of_return = self.sim[i]
            
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
            # how to determine which account to take distributions  from? and what to do with the 
            # account when it runs out?
            if SOY_non_taxable_balance >= 0:
                non_taxable_returns = rate_of_return * SOY_non_taxable_balance
                EOY_non_taxable_balance = SOY_non_taxable_balance + non_taxable_returns + non_taxable_contrib
            else:
                non_taxable_returns = 0
                EOY_non_taxable_balance=SOY_non_taxable_balance
            
            if age > self.retirement_age:
                expenses = self.monthly_retirement_expenses * 12 * (1+self.inflation_rate)**i
            else:
                expenses = 0            
            
            if expenses > 0:
                EOY_non_taxable_balance-=expenses/(1-self.effective_tax_rate)
        
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
             'EOY_balance' : EOY_taxable_balance + EOY_non_taxable_balance,
            }
            
        return plan_dict
    
    def print_path(self):
        print "Average return :" + str(numpy.mean(self.sim))
        print "year : age : return : returns : SOY_balance : contribution : expenses : EOY_balance "
        for k in sorted(self.path_dict.keys()):
            print str(k) + " : " +str(self.path_dict[k]['age']) + " : " + str(self.path_dict[k]['return']) + " : " + str(int(self.path_dict[k]['non_taxable_returns'])) + " : " + str(int(self.path_dict[k]['SOY_non_taxable_balance'])) + " : " + str(self.path_dict[k]['non_taxable_contribution']) + " : " + str(int(self.path_dict[k]['yearly_expenses'])) + " : " + str(int(self.path_dict[k]['EOY_non_taxable_balance']))
        
        #for k,v in self.path_dict.iteritems():
         #   print str(k) + " : " + str(v['SOY_non_taxable_balance']) + " : " + str(v['non_taxable_contribution']) + " : " + str(v['EOY_non_taxable_balance'])
    
    def short(self):
        return "End Balance : " + str(self.end_balance) + " Average return : " + str(numpy.mean(self.sim))
