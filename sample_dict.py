from retcalc import retCalc, simData, pathOnPortfolio
import sys

def main():
    sample_dict = {'age': 32,
                   'retirement_age' : 65,
                   'terminal_age' : 90,
                   'non_taxable_balance': 100000,
                   'taxable_balance' : 0,
                   'eff_tax_rate' : 0.3,
                   'returns_tax_rate' : 0.3,
                   'non_taxable_contribution' : 21500,
                   'taxable_contribution' : 12500,
                   'monthly_retirement_expenses': 4200,
                   'retirement_age' : 65,
                   'expected_rate_of_return' : 0.07,
                   'asset_volatility' : 0.15,
                   'inflation_rate' : 0.035,
                   }
    r = retCalc(sample_dict)
    x = r.plan_dict
    r.plan_dict[0].print_path()

    

if __name__ == '__main__':
    status = main()
    sys.exit(status)