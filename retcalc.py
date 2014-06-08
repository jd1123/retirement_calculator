import datetime
from simulations import simData
from paths import pathOnPortfolio
import matplotlib.pyplot as plt

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
    
    def plot_confidence(self, confidence = 0.1):
        n_path = int(confidence * len(self.plan_dict))
        path = self.plan_dict[n_path].path_dict
        X = sorted([int(k) for k in path.keys()])
        Y = [path[k]['EOY_balance'] for k in X]
        plt.plot(X,Y)
        plt.savefig('balance.png')