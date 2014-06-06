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
                   }
    r = retCalc(sample_dict)
    x = r.plan_dict
    #for p in x:
    #    print p
    r.plan_dict[0].print_path()
    #s = r.simdata.return_sims[0]
    #p = pathOnPortfolio(sample_dict, s)
    #print p.end_balance
    #x = r.run_all_sims()
    #print r.get_final_balance(r.plan_dict[0])
    #print type(r.plan_dict)
    #r.set_params(sample_dict)
    #s = simData(0.07, 0.12, 52)
    #print s.return_sims
    

if __name__ == '__main__':
    status = main()
    sys.exit(status)