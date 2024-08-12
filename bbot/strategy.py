"""
Strategy based on the indicators to make long or short order
"""

from bbot.calc_indicators import Indicators
import pandas as pd

def getStrategy(klines:pd.DataFrame):
    """
    Method to calculate the stragegy of trading and
    return the type of order: SELL or BUY
    """

    #get the indicators
    ind = Indicators(klines)
    ind_df = ind.getIndicators()

    ind_list = []


    """
    TODO
    1. create a list for indicators (0: sell and 1: buy)
    2. get the TA indicators:
        1. MA 5 cross Ma 10
        2. MA 5 cross MA 20
        3. BBands
        4. SO
        5. RSI
        6. ADX
        7. OBV
        8. Awesome Oscillator
        9. MACD
        10. ATR
    3. get the Machine learning indicators
        1. Gradient Boosting
        2. Histogram-Based Gradient Boosting
    4. count the list indicators
    5. return sell or buy string
    """


