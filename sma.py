#develop a trading strategy using tBefore moving to the coding part, 
#it’s essential to have a good background on the strategy we’re going to build in this article. 
#Our trading strategy follows the principle of simplicity yet a very effective breakout strategy.
#We enter the market if: the stock’s current high exceeds the 50-week high
#We exit the market if: the stock’s current low sinks below the 40-week low
#We’ll be using the Donchian Channel indicator in order to keep track of the 50-week high and the 40-week low. This strategy is a weekly trading system, so, we’ll be backtesting it on the weekly timeframe.

import pandas as pd
import requests
import pandas_ta as ta
import matplotlib.pyplot as plt
from termcolor import colored as cl
import math 