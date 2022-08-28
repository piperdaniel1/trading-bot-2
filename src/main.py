from datatypes.PriceHistory import PriceHistory
from plot_helpers.ph_help import save_ph_plot, save_simple_ind_plot
from datatypes.Indicator import Indicator

def main():
    print(" === Trading Bot 2 === ")
    ph = PriceHistory("SPXL", "1d", "1y")
    ema = Indicator("ema")
    save_simple_ind_plot(ph, [ema])
    
if __name__ == '__main__':
    main()