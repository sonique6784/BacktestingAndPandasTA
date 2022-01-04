
from pandas_ta import rsi
from pandas_ta import macd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import _read_file
import pathlib

# Pandas TA
# https://github.com/twopirllc/pandas-ta#trend-18
# https://jasonvan.ca/posts/backtesting-stock-trading-strategies-in-python

# Backtestin Docs
# https://kernc.github.io/backtesting.py/doc/backtesting/#gsc.tab=0



def loadDataset(instrument):
    currentpath = pathlib.Path().resolve()
    return _read_file(str(currentpath) + '/'+instrument+'.csv').dropna()


QQQ = loadDataset("QQQ")

class RSIandMACD(Strategy):
    positionLongOpen = False
    positionShortOpen = False

    def init(self):
        price = self.data.Close

        # self.rsi = self.data.df.ta.rsi()
        # print(self.rsi)
        self.rsi = self.I(rsi, self.data.df.Close, length=14)

        # self.macd = self.data.df.ta.macd()
        #print(self.macd)
        self.macd = self.I(macd, self.data.df.Close, fast=12,
                           slow=26, signal=9, col_names=("MACD", "MACD_H", "MACD_S"))

        

    def next(self):
        rsi_today = self.rsi[-1]
        rsi_twodaysago = self.rsi[-3]

        macd_today = self.macd[0][-1]
        macdh_today = self.macd[1][-1]
        macds_today = self.macd[2][-1]


        if rsi_today > 50 and rsi_twodaysago < 50 and macd_today < 0 and macdh_today > 0:
            if not self.positionLongOpen:
                self.positionLongOpen = True
                self.buy()

        
        elif rsi_today < 50 and rsi_twodaysago > 50 and macd_today > 0 and macdh_today < 0:

            if self.positionLongOpen:
                self.positionLongOpen = False
                self.sell()

bt = Backtest(QQQ, RSIandMACD, commission=.002,
              exclusive_orders=True)
stats = bt.run()
print(stats)
# bt.plot()
