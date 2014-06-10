from retcalc import retCalc, pathOnPortfolio
import sys

s = {'age': 22,
                   'retirement_age' : 65,
                   'terminal_age' : 90,
                   'non_taxable_balance': 0,
                   'taxable_balance' : 0,
                   'eff_tax_rate' : 0.2,
                   'returns_tax_rate' : 0.3,
                   'non_taxable_contribution' : 17500,
                   'taxable_contribution' : 2000,
                   'monthly_retirement_expenses': 4200,
                   'retirement_age' : 65,
                   'expected_rate_of_return' : 0.07,
                   'asset_volatility' : 0.15,
                   'inflation_rate' : 0.035,
                   }


def main():
    sample_dict = {'age': 22,
                   'retirement_age' : 65,
                   'terminal_age' : 90,
                   'non_taxable_balance': 0,
                   'taxable_balance' : 0,
                   'eff_tax_rate' : 0.2,
                   'returns_tax_rate' : 0.3,
                   'non_taxable_contribution' : 17500,
                   'taxable_contribution' : 0,
                   'monthly_retirement_expenses': 4200,
                   'retirement_age' : 65,
                   'expected_rate_of_return' : 0.07,
                   'asset_volatility' : 0.15,
                   'inflation_rate' : 0.035,
                   }
    r = retCalc(sample_dict)
    x = r.plan_dict
    r.plot_bar(0.05)
    r.histo()
    #r.confidence_path(0.01)
    #for i in range(len(r.plan_dict)):
    #    print "i : " + str(i) + " short : " + r.plan_dict[i].short() 
    #r.plan_dict[0].print_path()
    #r.sort_paths()
    

if __name__ == '__main__':
    status = main()
    sys.exit(status)