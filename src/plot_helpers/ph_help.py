from typing import List
from datatypes.Indicator import Indicator
from datatypes.PriceHistory import PriceHistory
from matplotlib import pyplot as plt
from datetime import timedelta as td

def to_day_float(time_diff: td):
    days = 0
    days += time_diff.days
    days += time_diff.seconds / 86400
    days += time_diff.microseconds / 86400000000
    
    return days

def plot_basic_ph(ph: PriceHistory):
    bar_list = ph.get_bar_list()
    plt.rcParams.update({'font.size': 5})

    bar_width = 0.9
    for ind, bar in enumerate(bar_list):
        x_ind = ind
        # plot an upwards bar
        if bar["open"] < bar["close"]:
            plt.bar(x_ind, abs(bar["open"] - bar["close"]), bottom=bar["open"], align="center", color="green", width=bar_width)
            plt.vlines(x_ind, bar["low"], bar["high"], linestyles="dotted", color="green", linewidth=bar_width/3)
        # plot a downwards bar
        else:
            plt.bar(x_ind, abs(bar["open"] - bar["close"]), bottom=bar["close"], align="center", color="blue", width=bar_width)
            plt.vlines(x_ind, bar["low"], bar["high"], linestyles="dotted", color="blue", linewidth=bar_width/3)

def save_simple_ind_plot(ph: PriceHistory, indicators: List[Indicator] = [], file: str = None):
    plot_basic_ph(ph)

    for indicator in indicators:
        ind_plot_dict = indicator.gen_values(ph.get_bar_list())

        if indicator.render_on_graph:
            for line in ind_plot_dict["lines"]:
                plt.plot(line, linewidth=0.5)

    if file == None:
        file = "./figures/" + ph.ticker + "-" + ph.timeframe + "-" + ph.interval
        for ind in indicators:
            file += "-" + ind.indicator_type
        file += ".jpg"
    
    plt.savefig(file, dpi=1000)

def save_ph_plot(ph: PriceHistory, file: str = None):
    plot_basic_ph(ph)

    if file == None:
        file = "./figures/" + ph.ticker + "-" + ph.timeframe + "-" + ph.interval + ".jpg"
    
    plt.savefig(file, dpi=1000)
