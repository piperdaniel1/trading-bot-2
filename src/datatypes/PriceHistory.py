import yfinance as yf
from typing import Dict, List
from datetime import datetime as dt, timedelta as td

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

    def get_bar_list(self) -> List[Dict]:
        return self.bars
    
    def get_timeframe(self) -> td:
        if self.timeframe[-1] == "m":
            return td(minutes=int(self.timeframe[0:-1]))
        elif self.timeframe[-1] == "h":
            return td(hours=int(self.timeframe[0:-1]))
        elif self.timeframe[-1] == "d":
            return td(days=int(self.timeframe[0:-1]))