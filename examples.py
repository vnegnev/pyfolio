#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

import pdb
st = pdb.set_trace

import pyfolio as pf

def single_option():
    """ You want to see how the unit price of a put on ABC, expiring in a month, evolves as a function of the underlying price and the days until expiry.
    """

    opt = pf.Option('ABC',
                    '2020-10-01', # date of expiry
                    True, # put = True, call = False
                    90, # strike price
                    1, # you bought a single option
                    250, # you paid $250 for the option, including transaction fees
                    2, # your broker charged you $2
                    )

    days = [200, 100, 50, 20, 10, 0.00001] # days till expiry; don't quite use 0 days, since formula diverges at the strike price
    prices = np.linspace(80, 110, 1000) # range of underlying prices
    iv = 20 # implied volatility

    fig, axs = plt.subplots(2, 2, figsize=(14, 10)) # slightly larger figure than normal

    lines = opt.unit_price(prices, iv, days)
    linecloses = opt.cost_to_close(prices, iv, days)
    lineprofits = opt.profit(prices, iv, days)

    axpu = axs[0][0]
    axcc = axs[0][1]
    axpr = axs[1][0]
    
    for k, (lip, lic, lipr) in enumerate(zip(lines, linecloses, lineprofits)):
        axpu.plot(prices, lip)
        axcc.plot(prices, lic)
        axpr.plot(prices, lipr)        


    axpu.grid(True)
    axcc.grid(True)
    axpr.grid(True)    
    
    axpu.set_xlabel('Price of underlying')
    axcc.set_xlabel('Price of underlying')
    axpr.set_xlabel('Price of underlying')        

    axpu.set_ylabel('Option unit price')
    axcc.set_ylabel('Cost to close position (positive = you pay)')
    axpr.set_ylabel('Profit percentage (positive = you gain)')

    axpu.legend( tuple("{:.1f} days left".format(d) for d in days) )
    plt.show()
    
single_option()
