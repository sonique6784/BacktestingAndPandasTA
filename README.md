# Backtesting.py and Pandas TA
This project is a simple demonstration of using Backtesting.py and Pandas TA. It implements a few indicators, so you can build on top and fine tune your own strategy.

## Disclaimer
Please remember that trading is serious and only trade with the money you don't need, it is very easy lost everything.

I should highlight that, while the demo strategy I implemented has positive returns, it is far behind Buy & Hold.


## Pre-requisites
 - Python3
 - pip3

## Install
```
$ pip3 install -r requirements.txt 
```

This will install all required packages to run this project

## Run
```
$ python3 pandasta_strategy_demo.py
```

## How does it works?

### Get and load a dataset for Stock, FX, Crypto
#### Download the Dataset
  1. Go to Yahoo Finance.
  2. Enter a quote into the search field.
  3. Select a quote in the search results to view it.
  4. Click Historical Data.
  5. Select a Time Period, data to Show, and Frequency.
  6. Click Apply.
  7. To use the data offline, click Download.
  9. Save the file with INSTRUMENT_NAME.csv 
#### Load the Dataset
```
INSTRUMENT_NAME = loadDataset("INSTRUMENT_NAME")
```

### Implement a strategy
This is based on Backtesting so you can also refer to the official documentation.
  1. Give a name to the strategy

```
class StrategyName(Strategy):

```

  2. Implement `init`, where you load all your indicators and prepare the data
   ```
   def init(self):
       self.rsi = self.I(rsi, self.data.df.Close, length=14)
   ```
  3. Implement `next`, this is where you implement your strategy, all the condition that will lead to BUY or SELL.
   ```
   def next(self):
        # Get data for the current iteration
        rsi_today = self.rsi[-1]

        # Process this data with if statements or other functions and trigger a buy or sell.
        if rsi_today > 50:
            self.buy()
        if rsi_today < 50:
            self.sell()
   ```

`-1` means today

`-2` means yesterday and so on.

### Run the strategy
Now we can load and run our strategy into backtesting

```
bt = Backtest(INSTRUMENT_NAME, StrategyName, commission=.002,
              exclusive_orders=True)
stats = bt.run()
print(stats)
```

It is possible to plot data by running `bt.plot()`