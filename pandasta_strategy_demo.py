
from pandas_ta import rsi
from pandas_ta import macd
from pandas_ta import sma
from pandas_ta import ma
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import _read_file
import pandas as pd
import pathlib
import os.path
import json

import yfinance as yf
import datetime
#from yahoofinancials import YahooFinancials

# Pandas TA
# https://github.com/twopirllc/pandas-ta#trend-18
# https://jasonvan.ca/posts/backtesting-stock-trading-strategies-in-python

# Backtestin Docs
# https://kernc.github.io/backtesting.py/doc/backtesting/#gsc.tab=0

# https://towardsdatascience.com/a-comprehensive-guide-to-downloading-stock-prices-in-python-2cd93ff821d4
# tsla_df = yf.download('TSLA',
#                       start='2019-01-01',
#                       end='2019-12-31',
#                       progress=False)


# https://towardsdatascience.com/making-a-trade-call-using-simple-moving-average-sma-crossover-strategy-python-implementation-29963326da7a
# https://tradewithpython.com/generating-buy-sell-signals-using-python

# print(tsla_df.head())



lastDayMACD = 0.0
lastDayRSI = 0.0
lastMA50 = 0.0
lastMA200 = 0.0
lastPrice = 0.0

def loadRemoteDataset(instrument):
    tod = datetime.datetime.now()
    d = datetime.timedelta(days=300)
    startdate = tod - d
    datestr = startdate.strftime('%Y-%m-%d')
    if(not isCached(instrument, datestr)):
        # yfinance now returns a MultiIndex for columns.
        # We need to flatten it for backtesting.py
        data = yf.download(instrument, start=datestr, interval="1d")
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(1)

        print("download type: "+str(type(data)))

        saveLocally(instrument, datestr, data)
    else:
        data = getCache(instrument, datestr)

    return data

def saveLocally(instrument, date, data):
    # TODO
    return

def isCached(instrument, date):
    # TODO
    return False

def getCache(instrument, date):
    data = []
    filename = cacheName(instrument, date)
    if os.path.isfile(filename):
        f = open(filename, "r", encoding='utf-8')
        data = json.loads(f.read())
    return data

def cacheName(instrument, date):
    return str(instrument)+"-"+date+".csv"

def loadDataset(instrument):
    currentpath = pathlib.Path().resolve()
    return _read_file(str(currentpath) + '/'+instrument+'.csv').dropna()


QQQ = loadRemoteDataset("QQQ")


class RSIandMACD(Strategy):
    positionLongOpen = False
    positionShortOpen = False

    def init(self):
        self.price = self.data.Close

        # self.rsi = self.data.df.ta.rsi()
        # print(self.rsi)
        self.rsi = self.I(rsi, self.data.df.Close, length=14)

        # self.macd = self.data.df.ta.macd()
        # print(self.macd)
        # MACD
        # MACD H : Histogram (trend change)
        # MACD S : Signal
        self.macd = self.I(macd, self.data.df.Close, fast=12,
                           slow=26, signal=9, col_names=("MACD", "MACD_H", "MACD_S"))
        
        self.ma50 = self.I(sma, self.data.df.Close, length=50)
        self.ma200 = self.I(sma, self.data.df.Close, length=200)

    def next(self):
        global lastDayMACD
        global lastDayRSI
        global lastMA50
        global lastMA200
        global lastPrice

        self.positionLongOpen = False
        self.positionShortOpen = False


        data_len = len(self.price) - 3
        for i in range(data_len):
            if ( i < len(self.rsi)):
                rsi_today = self.rsi[i]
                if i - 15 >= 0:
                    rsi_twodaysago =  self.rsi[i-5:i].mean()
                else:
                    rsi_twodaysago = 50

            if ( i < len(self.macd[0])):
                macd_today = self.macd[0][i]
                macdh_today = self.macd[1][i]

#            print( str(i) +" rsi: "+ str(rsi_today) + " rsi X days ago: "+ str(rsi_twodaysago))
            

            if rsi_today > 51 and rsi_twodaysago > 50 and rsi_today > rsi_twodaysago and macd_today < 0 and macdh_today > 0:
                if not self.positionLongOpen:
                    self.positionLongOpen = True
                    # print("Buy: " + str(self.price[i]))
                    self.buy()

            # elif rsi_today < 60 and rsi_twodaysago > 60 and macd_today > 0 and macdh_today < 0:
            #     if self.positionLongOpen:
            #         self.positionLongOpen = False
            #         print("Sell" + str(self.price[i]))
            #         self.sell()

        rsi_today = self.rsi[-1]
        rsi_twodaysago = self.rsi[-3]
        lastDayRSI = rsi_today

        macd_today = self.macd[0][-1]
        macdh_today = self.macd[1][-1]
        macds_today = self.macd[2][-1]

        lastDayMACD = macd_today

        
        ma50_today = self.ma50[-1]
        lastMA50 = ma50_today

        ma200_today = self.ma200[-1]
        lastMA200 = ma200_today

        lastPrice = self.price[-1]


bt = Backtest(QQQ, RSIandMACD, commission=.002,
              exclusive_orders=True)
stats = bt.run()
print(stats)

print("last day MACD: " + str(lastDayMACD))
print("last day RSI: " + str(lastDayRSI))
print("last day SMA50: " + str(lastMA50))
print("last day SMA200: " + str(lastMA200))
print("last day price: " + str(lastPrice))



#bt.plot()
