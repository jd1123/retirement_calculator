import datetime
import numpy
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
        #self.simdata = simData(self.expected_rate_of_return, self.asset_volatility, self.years)
        self.n = 5000
        self.plan_dict = self.run_all_sims()
        
    
    def get_final_balance(self, path):
        key = max(path.keys())
        return path[key]['EOY_taxable_balance'] + path[key]['EOY_non_taxable_balance']
    
    # runs all the sims and returns a list of paths sorted by end balance
    def run_all_sims(self):
        all_paths = []
        for i in range(self.n):
            path = pathOnPortfolio(self.param_dict)
            all_paths.append(path)
        all_paths.sort(key=lambda x: x.end_balance)
        return all_paths
    
    def confidence_path(self, confidence = 0.1):
        n_path = int(confidence * len(self.plan_dict))
        self.plan_dict[n_path].print_path()
        return self.plan_dict[n_path]
    
    def get_confidence_path(self, confidence = 0.1):
        n_path = int(confidence * len(self.plan_dict))
        path = self.plan_dict[n_path].path_dict
        years = sorted([int(k) for k in path.keys()])
        balances = [path[k]['EOY_balance'] for k in years]
        ages = [path[k]['age'] for k in years]
        flows = [(-path[k]['yearly_expenses'] + path[k]['non_taxable_contribution'] + path[k]['taxable_contribution']) for k in years]
        #plt.plot(years, flows)
        #plt.savefig('balance.png')
        return (years, ages, balances, flows)
    
    def plot_confidence(self, confidence = 0.1, x_axis = 'years'):
        (years, ages, balances, flows) = self.get_confidence_path(confidence)
        if (x_axis == 'years'):
            plt.plot(years, balances)
        else:
            plt.plot(ages, balances)
        plt.savefig('balance.png')
        
    def plot_bar(self, confidence=0.1):
        (years, ages, balances, flows) = self.get_confidence_path(confidence)
        fig = plt.figure()
        ax1 = plt.subplot()
        ax1.bar(ages, flows, width=1)
        
        ax2 = ax1.twinx()
        #ax2 = plt.subplot(111)
        ax2.plot(ages, balances, color='black')
        
        plt.savefig('flows.png')
        
    def histo(self):
        end_balances = [self.plan_dict[i].end_balance for i in range(len(self.plan_dict))]
        hist = numpy.histogram(end_balances, bins=350)
        print "num\t\tCum Prob\t\tEnd Balance"
        t = 0
        for i in range(len(hist[0])):
            t += hist[0][i]
            print str(hist[0][i]) + "\t\t" + str(float(t)/float(self.n))+ "\t\t" + str(hist[1][i])
        
        bins = [-20000000+1000000*i for i in range(41)]
        # the histogram of the data
        num_bins = 30
        plt.hist(end_balances, bins=bins, normed=False, facecolor='green', alpha=0.5)
        
        plt.savefig('histo.png')