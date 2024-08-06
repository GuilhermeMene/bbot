"""
Preparing the indicators for the machine learning models
"""

import pandas as pd
import pandas_ta as ta
import sys
import os

class Indicators:

    def __init__(self, filepath, period):

        #Read the file
        self.df = pd.read_csv(filepath, delimiter=',')

        #Set the output filename
        fname = os.path.split(filepath)
        file_out = os.path.join(os.getcwd(), "data", f"Data_{period}_wt_Indicators.csv")

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

        #Export the dataframe
        self.df.to_csv(file_out, index=False)

    def calcDiff(self, period):
        """
        Calculate the difference of the close values
        """

        self.close = self.df['Close']
        self.df = pd.concat([self.df, self.close.diff(period).rename(f'Diff_{period}')], axis=1)

    def createIndicators(self):
        """
        Calculate the indicators using the pandas_ta
        """

        #SMA (5, 10, 20, and 50 periods)
        self.df['SMA_5'] = ta.sma(self.df['Close'], length=5)
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

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Provide the filename and period of candles.")
        sys.exit(1)

    fname = sys.argv[1]
    period = sys.argv[2]

    cwd = os.path.split(os.getcwd())
    base_path = cwd[0]
    data_path = "data"

    Indicators(fname, period)
