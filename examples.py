#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

import pdb
st = pdb.set_trace

import pyportfolio as pf

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

    days = [200, 100, 50, 20, 10, 0] # days till expiry
    prices = np.linspace(80, 110, 1000) # range of underlying prices
    iv = 30 # implied volatility

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
    
def strangle_portfolio():
    """ You bought two sets of options and are long a strangle, and you'd like to see how it performs as a function of the underlying price and the days until expiry.
    Manual calculation.
    """

    oa = pf.Option('ABC', '2020-06-30', True, 80, 3, 300, 6)
    ob = pf.Option('ABC', '2020-06-30', False, 120, 3, 300, 6)

    days = [60, 40, 20, 10, 0]
    prices = np.linspace(70, 130, 1000)
    iv = 30

    fig, ax = plt.subplots(1, 1, figsize=(14, 10)) # slightly larger figure than normal

    lines = oa.profit(prices, iv, days) + ob.profit(prices, iv, days)
    for k, l in enumerate(lines):
        ax.plot(prices, l)

    ax.grid(True)
    ax.set_xlabel('Price of underlying')
    ax.set_ylabel('Profit percentage (positive = you gain)')
    ax.legend( tuple("{:.1f} days left".format(d) for d in days) )
    plt.show()

def straddle_portfolio():
    """ You sold two sets of options and are short a straddle, and you'd like to see how it performs as a function of the underlying price and the days until expiry.
    Manual calculation.
    """

    # Exactly ATM
    # oa = pf.Option('SPY', '2020-05-08', True, 283, -1, -533, 2)
    # ob = pf.Option('SPY', '2020-05-08', False, 283, -1, -479, 2)
    # dates = ['2020-05-04', '2020-05-05', '2020-05-06', '2020-05-07', '2020-05-08']    

    # A bit OTM
    oa = pf.Option('SPY', '2020-05-08', True, 280, -1, -417, 2)
    ob = pf.Option('SPY', '2020-05-08', False, 286, -1, -322, 2)
    dates = ['2020-05-04', '2020-05-05', '2020-05-06', '2020-05-07', '2020-05-08']    

    # A bit ITM
    # oa = pf.Option('SPY', '2020-05-08', True, 286, -1, -675, 2)
    # ob = pf.Option('SPY', '2020-05-08', False, 280, -1, -663, 2)    
    # dates = ['2020-05-04', '2020-05-05', '2020-05-06', '2020-05-07', '2020-05-08']
    
    prices = np.linspace(250, 310, 1000)
    iv = 45

    fig, ax = plt.subplots(1, 1, figsize=(14, 10)) # slightly larger figure than normal

    lines = oa.profit(prices, iv, dates) + ob.profit(prices, iv, dates)
    for k, l in enumerate(lines):
        ax.plot(prices, l)

    ax.grid(True)
    ax.set_xlabel('Price of underlying')
    ax.set_ylabel('Profit percentage (positive = you gain)')
    ax.legend( tuple("{:s}".format(d) for d in dates) )
    plt.show()    

def short_portfolio():
    """ You bought a put and sold a call at the same strike, creating an effective short position, and you'd like to see how it performs as a function of the underlying price and the implied volatility (due to put-call parity, it should be insensitive to IV and expiry time).
    Manual calculation.
    """

    oa = pf.Option('VXX', '2020-06-05', True, 41.5, 1, 537, 2)
    ob = pf.Option('VXX', '2020-06-05', False, 41.5, -1, -443, 2)

    days = 30
    # prices = np.linspace(70, 130, 1000)
    prices = np.linspace(20, 60, 1000)
    iv = [80, 100, 120, 150]

    fig, ax = plt.subplots(1, 1, figsize=(14, 10)) # slightly larger figure than normal

    lines = oa.profit(prices, iv, days, percentage=False) + ob.profit(prices, iv, days, percentage=False)
    for k, l in enumerate(lines):
        ax.plot(prices, l)

    ax.grid(True)
    ax.set_xlabel('Price of underlying')
    ax.set_ylabel('Profit (positive = you gain)')
    ax.legend( tuple("{:.1f}% IV".format(i) for i in iv) )
    plt.show()

def reverse_calendar_spread_portfolio():
    """ You bought two sets of options at the same strike and different expiry dates, and are long the near-expiry one and short the far-expiry one. You'd like to see how it performs as a function of the underlying price and the days until expiry.
    Manual calculation.
    """

    oa = pf.Option('SPY', '2020-06-30', False, 100, 3, 136, 6)
    ob = pf.Option('SPY', '2020-08-30', False, 100, -3, -150, 6)

    dates = ['2020-04-30', '2020-05-30', '2020-06-15']
    prices = np.linspace(70, 130, 1000)
    iv = 20

    fig, ax = plt.subplots(1, 1, figsize=(14, 10)) # slightly larger figure than normal

    lines = oa.profit(prices, iv, dates) + ob.profit(prices, iv, dates)
    for k, l in enumerate(lines):
        ax.plot(prices, l)

    ax.grid(True)
    ax.set_xlabel('Price of underlying')
    ax.set_ylabel('Profit percentage (positive = you gain)')
    ax.legend( tuple("Profit on {:s}".format(d) for d in dates) )
    plt.show()    
    
# single_option()
# strangle_portfolio()
straddle_portfolio()
# short_portfolio()
# reverse_calendar_spread_portfolio()
