import random
from scipy.stats import norm

def simulation(vec_size, rate_of_return, asset_vol):
    u = [random.random() for i in range(vec_size)]
    return list(norm.ppf(u, loc=rate_of_return, scale=asset_vol))