"""
Preparing the indicators for the machine learning models
"""

import pandas as pd
import pandas_ta as ta

class Indicators:

    def __init__(self, dataframe:pd.DataFrame):

        #Read the file
        self.df = dataframe

        #Default length
        self.length = 5

        #Set the index of the table
        self.df.set_index(self.df['OpenTime'])

        #Calculate the difference
        self.calcDiff(1)
        self.calcDiff(5)
        self.calcDiff(10)

        self.createIndicators()

        #Drop NA rows
        self.df = self.df.dropna(axis=0)
        self.df = self.df.round(2)

        #Return the dataframe
        #self.getIndicators()

    def getIndicators(self):
        """
        Return the dataframe
        """
        return self.df

    def calcDiff(self, period):
        """
        Calculate the difference of the close values
        """

        self.close = self.df['Close']
        self.df = pd.concat([self.df, self.close.diff(period).rename(f'Diff_{period}')], axis=1)

        #Create a label for the dataset

    def label_diff_one(self, row):
        if row['Diff_1'] > 0:
            val = 1
        else:
            val = 0

        return val

    def label_diff_five(self, row):
        if row['Diff_5'] > 0:
            val = 1
        else:
            val = 0

        return val

    def short_trend(self, row):
        if row['Open'] > row['Close']:
            val = 0
        else:
            val = 1

        return val

    def five_period_trend(self, row):
        if row['SMA_5_Open'] > row['SMA_5']:
            val = 0
        else:
            val = 1

        return val

    def SMA_open(self, row):
        if row['SMA_5'] > row['Open'] :
            val = 0
        else:
            val = 1

        return val

    def createIndicators(self):
        """
        Calculate the indicators using the pandas_ta
        """

        #SMA (5, 10, 20, and 50 periods)
        self.df['SMA_5'] = ta.sma(self.df['Close'], length=5)
        self.df['SMA_5_Open'] = ta.sma(self.df['Open'], length=5)
        self.df['SMA_10'] = ta.sma(self.df['Close'], length=10)
        self.df['SMA_20'] = ta.sma(self.df['Close'], length=20)
        self.df['SMA_50'] = ta.sma(self.df['Close'], length=50)

        #RSI (5 and 10 periods)
        self.df['RSI_5'] = ta.rsi(self.df['Close'], length=5)
        self.df['RSI_10'] = ta.rsi(self.df['Close'], length=self.length)

        #BB
        self.bb = ta.bbands(self.df['Close'], length=self.length)
        self.df = pd.concat([self.df, self.bb], axis=1)

        #MACD
        self.macd = ta.macd(self.df['Close'])
        self.df = pd.concat([self.df, self.macd], axis=1)

        #SO
        self.so = ta.stoch(
            self.df['High'],
            self.df['Low'],
            self.df['Close']
        )
        self.df = pd.concat([self.df, self.so], axis=1)

        #FR
        self.df['FR'] = ta.fwma(self.df['Close'], length=self.length)

        #ADI
        self.adi = ta.adx(
            self.df['High'],
            self.df['Low'],
            self.df['Close'],
            length=self.length
        )
        self.df = pd.concat([self.df, self.adi], axis=1)

        #AO
        self.df['AO'] = ta.ao(
            self.df['High'],
            self.df['Low'],
            fast=self.length
        )

        #ATR
        self.df['ATR'] = ta.atr(
            self.df['High'],
            self.df['Low'],
            self.df['Close'],
            length=self.length
        )

        #OBV
        self.df['OBV'] = ta.obv(
            self.df['Close'],
            self.df['Volume']
        )

        #Set short-term trend
        self.df['ShortTrend'] = self.df.apply(self.short_trend, axis=1)

        #SMA-Open short state
        self.df['SMA-Open'] = self.df.apply(self.SMA_open, axis=1)

        #Set the Trend for one period
        self.df['Trend_1'] = self.df.apply(self.label_diff_one, axis=1)

        #Set the tend for five periods
        self.df['Trend_5'] = self.df.apply(self.five_period_trend, axis=1)
