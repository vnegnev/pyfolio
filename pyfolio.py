#!/usr/bin/env python3
#
# PyFolio: a way for me to keep track of my portfolio, and be able to forecast what happens in the case of different price moves.

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import datetime

import pdb
st = pdb.set_trace

def is_iterable(obj):
    try:
        iter(obj)
    except Exception:
        return False
    else:
        return True

class Option:
    """ Class describing a single option transaction, and allowing you to calculate the predicted option price in the future. """

    def __init__(self, underlying, expiry, put, strike, increase_in_position, net_cost, transaction_fees, ratio=100, underlying_price=None):
        """ underlying: underlying ticker string, eg 'SPY'
        expiry: date string, YYYY-MM-DD, e.g. "2019-11-28"
        put: true if a put, false if a call
        strike: option strike price
        increase_in_position: how many options you bought: positive if you bought, negative if you sold
        net_cost: how much money the entire transaction cost you; positive if you bought, negative if you sold (i.e. gained money)
        transaction_fees: what the fees were for the entire transaction (always positive, presumably)
        ratio: option ratio on exercise, usually 10 or 100
        """
        self.underlying = underlying
        self.expiry = expiry
        self.put = put
        self.strike = strike
        self.increase_in_position = increase_in_position
        self.net_cost = net_cost
        self.transaction_fees = transaction_fees
        self.ratio = ratio

        # Internal calculation
        self.expiry_date = datetime.date.fromisoformat(expiry)
        if underlying_price:
            self.calculate_iv(underlying_price)

        # self.unit_price = np.vectorize(self.unit_price, otypes=[float], excluded=('underlying_price', 'iv')) #, signature='(),(1?),(1?)->(1?)')#, signature='(),(n?),(m?)->(k?)')#, excluded=('underlying_price', 'iv'))
        # self.unit_price = np.vectorize(self.unit_price, otypes=[float], excluded=[1])
        
        self.unit_price = np.vectorize(self.unit_price, otypes=[np.ndarray], excluded=[0, 1])
        self.cost_to_close = np.vectorize(self.cost_to_close, otypes=[np.ndarray], excluded=[0, 1])        

    def __repr__(self):
        pc = "p" if put else "c"
        return "{:s} {:.1f}{s} {:s}".format(underlying, strike, expiry_date)

    def calculate_iv(self, underlying_price):
        # calculate the IV at the time of the transaction

        print("NOT DONE YET")

    def unit_price(self, underlying_price, iv, date, interest_rate=0):
        """ Return the unit price of the options.
        underlying_price: price of underlying; single value or numpy array
        iv: implied volatility: single value or numpy array. Must be a percentage value.
        date: date string to calculate the price at; e.g. '2020-01-19'; alternatively you can manually specify the number of days until expiry, e.g. 3.5 . Accepts array-like as well.
        interest_rate: interest rate for Black-Scholes calculation; near-zero for the next decade in most of the developed world! Only relevant for options with many months or longer to expiry.
        """
        # vectorise inputs, to be safe
        underlying_price = np.asarray(underlying_price)
        iv = np.asarray(iv)
        # time remaining, in years
        if type(date) is str:
            tau = (self.expiry_date - datetime.date.fromisoformat(date)).days / 365 # approximate; ignores weekends etc!
        else:
            tau = date / 365 # presumably an int/double
        ivr = iv / 100

        d1 = (np.log(underlying_price/self.strike) + tau*(interest_rate + ivr**2/2)) / (ivr * np.sqrt(tau) )
        d2 = d1 - ivr * np.sqrt(tau)
        discounted_strike = self.strike * np.exp(-interest_rate*tau)

        call_price = norm.cdf(d1) * underlying_price - norm.cdf(d2) * discounted_strike
        
        if self.put:
            price = discounted_strike - underlying_price + call_price
        else:
            price = call_price

        return price

    def cost_to_close(self, *args, add_transaction_fees=True, **kwargs):
        """ Return how much the position would cost to liquidate. Negative if you're long (you originally bought the option), positive if you're short (you originally sold the option). 
        Arguments are the same as for unit_price().
        """
        up = self.unit_price(*args, **kwargs)
        raw_cost = -up * self.ratio * self.increase_in_position
        if add_transaction_fees:
            raw_cost += self.transaction_fees # assume closing fees are the same as opening fees

        return raw_cost

    def profit(self, *args, percentage=True, **kwargs):
        """ Return the profit from liquidating the position. Arguments are the same as for unit_price. """
        prof = -self.net_cost - self.cost_to_close(*args, **kwargs)
        if percentage:
            return prof / np.abs(self.net_cost) * 100
            

class Portfolio:
    """ Contains a list of transactions. Can be used to estimate the value of your portfolio in the future if you were to close all your positions (by selling stocks and selling-to-close or buying-to-close options).
    """

    def __init__(self):
        transaction_list = []

    def add_transaction(self, tr):
        transaction_list.append(tr)

    def cost_to_close(self, underlying, price, iv, date, add_transaction_fees=True, interest_rate=0):
        """ underlying: string like 'SPY'
        price: a value or array of prices.
        iv: a value or array of implied volatilities.
        date: date or range of dates to calculate this for your portfolio
        add_transaction_fees: add transaction fees (based on the opening transaction/transactions) to the cost to close.
        interest_rate: interest rate for Black-Scholes calculations on the options; near-zero for the next decade in most of the developed world! Only relevant for options with many months or longer to expiry.

        You can make either price or iv a range, but not both. Date can always be a range; in this case if both date and prices/ivs are ranges, then a 2D array of costs is returned.
        Rows are date-indexed; columns are price- or IV-indexed.
        """

        prices_vector = is_iterable(price)
        ivs_vector = is_iterable(iv)
        
        assert not (prices_vector and ivs_vector), "Only the prices or the IVs can be vectors, not both! Run Portfolio.cost_to_close_portfolio() in a loop."
        
        for tr in transaction_list:
            if tr.underlying == underlying: # strings match
                cost = tr.cost_to_close(date, price, iv, add_transaction_fees, interest_rate)
                try:
                    costs += cost
                except IOError:
                    st()

    def cost_to_close_portfolio(self, prices, ivs, date, add_transaction_fees=True, interest_rate=0):
        """prices: a dictionary in the form of {underlying : price}, e.g. {'SPY':250, 'IWM': 120, 'VXX':45}. Each value can be a single number or a Numpy array, but in the latter case all the other values have to be the same shape.        
        ivs: a dictionary in the form of {underlying: iv}, e.g. {'SPY':35, 'IWM':60, 'VXX': 100}. Each value can be a single number or a Numpy array, but in the latter case all the other values have to be the same shape.
        date: date or range of dates to calculate this for your portfolio
        add_transaction_fees: add transaction fees (based on the opening transaction/transactions) to the cost to close
        interest_rate: interest rate for Black-Scholes calculations on the options; near-zero for the next decade in most of the developed world! Only relevant for options with many months or longer to expiry.

        You can make either prices or ivs a range, but not both. Date can always be a range; in this case if both date and prices/ivs are ranges, then a 2D array of costs is returned.
        Rows are date-indexed; columns are price- or IV-indexed.
        """

        prices_vector = False
        ivs_vector = False
        x_axis = None
        if is_iterable(prices[0]):
            prices_vector = True
            x_axis = prices[0][0]
        elif is_iterable(ivs[0]):
            ivs_vector = True

        assert not (prices_vector and ivs_vector), "Only the prices or the IVs can be vectors, not both! Run Portfolio.cost_to_close_portfolio() in a loop."
        
        
