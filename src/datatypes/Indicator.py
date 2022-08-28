from typing import Dict, List
import talib
import numpy as np

# Wrapper for the TA Lib indicators
# We need this because it will allow us to translate the TA lib format to an easily plottable format
class Indicator:
    def __init__(self, indicator_type: str, ind_config: dict = {}):
        self.indicator_type = indicator_type
        if self.indicator_type.lower() == "ema":
            self.__init_EMA(ind_config)
    
    def __init_EMA(self, ind_config):
        if "period" in ind_config:
            self.period = ind_config["period"]
        else:
            self.period = 20
        
        if "pref_bar" in ind_config:
            self.pref_bar = ind_config["pref_bar"].lower() if ind_config["pref_bar"].lower() in ["open", "close", "high", "low", "volume"] else "close"
        else:
            self.pref_bar = "close"
        
        self.render_on_graph = True

    def __conv_barlist(self, bar_list: List[Dict]) -> List[float]:
        out = []
        for bar in bar_list:
            out.append(bar[self.pref_bar])
        return out

    def __gen_EMA(self, bar_list: List[Dict]):
        pricelist = self.__conv_barlist(bar_list)
        output = talib.EMA(np.array(pricelist), timeperiod=self.period)

        return output
    
    def gen_values(self, bar_list: List[Dict]) -> dict:
        if self.indicator_type == "ema":
            return {"lines": [self.__gen_EMA(bar_list)]}
        