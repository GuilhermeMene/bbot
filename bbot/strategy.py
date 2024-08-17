"""
Strategy based on the indicators to make long or short order
"""

from bbot import logger as log
from bbot.calc_indicators import Indicators
import pandas as pd
import os
import pickle
import numpy as np

def get_trend(data:list):
    """
    Calculate the trend based on the last three records
    """

    if len(data) < 3:
        log.logger("Strategy: The length of the data is lower than 3.")

    elif len(data) > 3:
        new_data = []
        for i in len(0, 2):
            new_data.append(data[i])
        if new_data[0] < new_data[1] and new_data[1] < new_data[2]:
            trend_signal = 'Up'
        elif new_data[0] > new_data[1] and new_data[1] > new_data[2]:
            trend_signal = 'Down'

        return trend_signal

    elif len(data) == 3:
        if new_data[0] < new_data[1] and new_data[1] < new_data[2]:
            trend_signal = 'Up'
        elif new_data[0] > new_data[1] and new_data[1] > new_data[2]:
            trend_signal = 'Down'

        return trend_signal

def get_cross(fast:list, slow:list):
    """
    Calculate if the line cross another
    """

    if len(fast) != len(slow):
        log.logger("Strategy: The length of the fast and slow is different.")
        return 'Neutral'
    else:
        if fast[0] > slow[0] and fast[-1] < slow[-1]:
            return 'Down'
        elif fast[0] < slow[0] and fast[-1] > slow[-1]:
            return 'Up'

def get_bb_ind(dataframe:pd.DataFrame):
    """
    Method to get the Bollinger Bands indicator
    """
    bb_list = []
    down = 0
    up = 0
    neutral = 0
    try:
        for i, row in dataframe.iterrows():
            if row['Low'] > row['BBM_5_2.0'] and row['High'] > row['BBU_5_2.0']:
                bb_list.append('Down')
            elif row['High'] < row['BBM_5_2.0'] and row['Low'] < row['BBL_5_2.0']:
                bb_list.append('Up')
            else:
                bb_list.append('Neutral')

        for i in range(0, len(bb_list)):
            if bb_list[i] == 'Down':
                down += 1
            elif bb_list[i] == 'Up':
                up += 1
            else:
                neutral += 1

        if down > up:
            return 'Down'
        elif up > down:
            return 'Up'
        else:
            return 'Neutral'

    except Exception as e:
        log.logger(e)

def getStrategy(klines:pd.DataFrame):
    """
    Method to calculate the stragegy of trading and
    return the type of order: SELL or BUY
    """

    #get the indicators
    ind = Indicators(klines)
    ind_df = ind.getIndicators()

    ind_list = []

    #get the last records from table
    last_rec = ind_df
    last_rec = last_rec.sort_values(by=['OpenTime'])
    last_rec = last_rec.tail(5) #get last 5 records

    tail_df = last_rec.tail(1)

    try:
        sig_five_ten = get_cross(last_rec['SMA_5'].to_list(), last_rec['SMA_10'].to_list())
        ind_list.append(sig_five_ten) #Append twice due the weight of this indicator
        ind_list.append(sig_five_ten)
        sig_five_twenty = get_cross(last_rec['SMA_5'].to_list(), last_rec['SMA_20'].to_list())
        ind_list.append(sig_five_twenty) #Append twice due the weight of this indicator
        ind_list.append(sig_five_twenty)

        #BBands
        bb_ind = get_bb_ind(ind_df.tail(10))
        ind_list.append(bb_ind) #Append twice due the weight of this indicator
        ind_list.append(bb_ind)

        #SO
        if tail_df['STOCHk_14_3_3'] < 20 and tail_df['STOCHd_14_3_3'] < 20:
            ind_list.append('Up')
        elif tail_df['STOCHk_14_3_3'] > 80 and tail_df['STOCHd_14_3_3'] > 80:
            ind_list.append('Down')
        else:
            pass

        #RSI
        if tail_df['RSI_5'] < 30:
            ind_list.append('Up')
        elif tail_df['RSI_5'] > 70:
            ind_list.append('Down')
        else:
            pass

        #AO
        ao = get_trend(last_rec['AO'].tail(3).to_list())
        if ao == 'Down':
            ind_list.append('Down')
        elif ao == 'Up':
            ind_list.append('Up')
        else:
            pass

    except Exception as e:
        log.logger(e)


    #get the machine learning indicators
    try:

        last = last_rec.drop(labels=['Trend_1'])
        last = np.array(last.values)
        last = last.reshape(1, -1)

        gbfile = os.environ.get('GB_MODEL')
        hgbfile = os.environ.get('HGB_MODEL')

        #Get using Gradient Boosting
        with open(gbfile, 'rb') as gb:
            gbmodel = pickle.load(gb)
            gb.close()
        gb_ind = gbmodel.predict(last)

        if gb_ind[0] == 0:
            ind_list.append('Down')
        elif gb_ind[0] == 1:
            ind_list.append('Up')
        else:
            pass

        #Get using Histogram-based Gradient Boosting
        with open(hgbfile, 'rb') as hgb:
            hgbmodel = pickle.load(hgb)
            hgb.close()
        hgb_ind = hgbmodel.predict(last)

        if hgb_ind[0] == 0:
            ind_list.append('Down')
        elif hgb_ind[0] == 1:
            ind_list.append('Up')
        else:
            pass

    except Exception as e:
        log.logger(e)


    try:
        if len(ind_list) <= 0:
            log.logger("Strategy, a error occurred with strategy.")

            return 'Neutral'
        else:
            up = 0
            down = 0
            for ind in ind_list:
                if ind == 'Down':
                    down += 1
                else:
                    up += 1
            if up > down:
                return 'BUY'
            elif up == down:
                return 'Neutral'
            else:
                return 'SELL'
    except Exception as e:
        log.logger(e)
