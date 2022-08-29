import sys
import yfinance as yf
from typing import Dict, List
from datetime import datetime as dt, timedelta as td
from plot_helpers.mth_help import *

class PriceHistory:
    # Ticker, timeframe, and period are required:
    # Ticker - Stock ticker
    # Timeframe (per bar) - Defaults to 1d
    # interval (of all bars) - Defaults to 30d
    def __init__(self, ticker: str, timeframe: str="1d", interval: str="30d", config: Dict = {}):
        self.ticker = ticker
        self.timeframe = timeframe
        self.interval = interval

        yfTicker = yf.Ticker(ticker)
        pandasBars = yfTicker.history(interval, timeframe)

        self.bars = []

        for i in range(len(pandasBars)):
            currBar = {"open": pandasBars["Open"][i], "high": pandasBars["High"][i], "low": pandasBars["Low"][i], "close": pandasBars["Close"][i], "volume": pandasBars["Volume"][i], "datetime": pandasBars.index[i].to_pydatetime()}
            self.bars.append(currBar)
        
        # Support point
        # Defined as a price level where there is support:
        # {price: 69.4, strength: 20}
        # strength is completely arbitrary, maybe it should be the number
        # of times price has hit that point
        self.support_points = []
        self.resistance_points = []

        self.find_support_points()
        
    def __str__(self) -> str:
        return_str = f"-- Price History ({len(self.bars)} bars of {self.ticker}) --\n"
        if len(self.bars) <= 10:
            for bar in self.bars:
                return_str += str(bar)
                return_str += "\n"
        else:
            for bar in self.bars[0:3]:
                return_str += str(bar)
                return_str += "\n"
            return_str += "...\n"
            for bar in self.bars[-4:-1]:
                return_str += str(bar)
                return_str += "\n"
        return return_str

    def __repr__(self) -> str:
        return f"Price History ({len(self.bars)} bars)"
    
    def should_remove_point(self, target_ind, points_list) -> bool:
        num_nearby = 0
        oldest_neighbor = target_ind
        NEIGHBORHOOD_PCT = 0.1
        
        for index, point in enumerate(points_list):
            if index == target_ind:
                continue
                
            diff = pct_diff(point["price"], points_list[target_ind]["price"])

            if diff < NEIGHBORHOOD_PCT:
                num_nearby += 1
                oldest_neighbor = min(oldest_neighbor, index)
        
        if oldest_neighbor < target_ind and num_nearby > 0:
            return True
    
    # works by traversing the price keeping track of highs and lows.
    # low points are probably support, high points are probably resistance
    def find_support_points(self):
        MAX_PCT_DEVIATION = 0.15
        high_points = []
        low_points = []

        curr_high = 0
        curr_high_start = 0
        curr_low = sys.maxsize
        curr_low_start = 0

        for ind, bar in enumerate(self.bars):
            if curr_high > curr_low and (curr_high - curr_low) / curr_high > MAX_PCT_DEVIATION:
                if abs(bar["close"] - curr_low) < abs(bar["close"] - curr_high):
                    high_points.append({"price": curr_high, "strength": 1, "start": curr_high_start})
                    curr_high = curr_low
                    curr_high_start = ind
                else:
                    low_points.append({"price": curr_low, "strength": 1, "start": curr_low_start})
                    curr_low = curr_high
                    curr_low_start = ind

            if curr_low > bar["close"]:
                curr_low = bar["close"]
                curr_low_start = ind
            
            if curr_high < bar["close"]:
                curr_high = bar["close"]
                curr_high_start = ind
        
        ind = len(low_points)-1
        while ind >= 0:
            if self.should_remove_point(ind, low_points):
                low_points.pop(ind)
            ind -= 1

        ind = len(high_points)-1
        while ind >= 0:
            if self.should_remove_point(ind, high_points):
                high_points.pop(ind)
            ind -= 1

        self.support_points = low_points
        self.resistance_points = high_points

    
    def get_bar_list(self) -> List[Dict]:
        return self.bars
    
    def get_sup_points(self) -> List[Dict]:
        return self.support_points

    def get_res_points(self) -> List[Dict]:
        return self.resistance_points
    
    def get_timeframe(self) -> td:
        if self.timeframe[-1] == "m":
            return td(minutes=int(self.timeframe[0:-1]))
        elif self.timeframe[-1] == "h":
            return td(hours=int(self.timeframe[0:-1]))
        elif self.timeframe[-1] == "d":
            return td(days=int(self.timeframe[0:-1]))