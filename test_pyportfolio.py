#!/usr/bin/env python3
#
# Tests of PyPortfolio

from pyportfolio import *
import unittest

class OptionTest(unittest.TestCase):
    def setUp(self):
        self.opt_lp = Option('SPY', '2020-04-30', True, 280, 3, 315.0, 6.0)
        self.opt_lc = Option('SPY', '2020-04-30', False, 280, 3, 315.0, 6.0)
        self.opt_sp = Option('SPY', '2020-04-30', True, 280, -3, -327.0, 6.0)
        self.opt_sc = Option('SPY', '2020-04-30', False, 280, -3, -327.0, 6.0)

    def test_unit_price(self):
        self.assertAlmostEqual(self.opt_lp.unit_price(279, 40, '2020-04-29'), 2.868, delta=0.001)
        self.assertAlmostEqual(self.opt_lc.unit_price(279, 40, '2020-04-29'), 1.868, delta=0.001)
        self.assertAlmostEqual(self.opt_sp.unit_price(278, 40, '2020-04-29'), 3.465, delta=0.001)
        self.assertAlmostEqual(self.opt_sc.unit_price(278, 40, '2020-04-29'), 1.465, delta=0.001)

    def test_unit_price_vec(self):
        # Test vectorisation of unit_price (and other functions by association)
        res = self.opt_lp.unit_price([279, 278], 40, '2020-04-29')
        for k, m in zip(res, np.array([2.868, 3.465])):
            self.assertAlmostEqual(k, m, delta=0.001)

        res2 = self.opt_lp.unit_price(279, [40, 45], '2020-04-29')
        for k, m in zip(res2, np.array([2.868, 3.156])):
            self.assertAlmostEqual(k, m, delta=0.001)
            
        res3 = self.opt_lp.unit_price(279, [40, 45], ['2020-04-29', '2020-03-20'])
        for k, m in zip(res3, [np.array([2.868, 3.156]), np.array([15.443, 17.306])]):
            for g, q in zip(k, m):
                self.assertAlmostEqual(g, q, delta=0.001)
            

    def test_cost_to_close(self):
        self.assertAlmostEqual(self.opt_lp.cost_to_close(279, 40, '2020-04-29'), -854.5, delta=0.1)
        self.assertAlmostEqual(self.opt_lc.cost_to_close(279, 40, '2020-04-29'), -554.5, delta=0.1)
        self.assertAlmostEqual(self.opt_sp.cost_to_close(278, 40, '2020-04-29'), 1045.7, delta=0.1)
        self.assertAlmostEqual(self.opt_sc.cost_to_close(278, 40, '2020-04-29'), 445.7, delta=0.1)

    @unittest.skip("Just to test plotting")
    def test_plot(self):
        x = np.linspace(270, 290, 1000)
        plt.plot(x, self.opt_lp.unit_price(x, 5, '2020-04-28'))
        plt.show()

    # def test_cost_to_close(self):
    #     price_lp = self.opt_lp.cost_to_close('2020-04-29', 279, 0.4)
    #     
            

class PyPortfolioTest(unittest.TestCase):

    def setUp(self):
        self.tr1 = None

unittest.main()        
